import logging
from typing import Optional
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.agents.ats_scorer.agent import ats_scorer_agent
from app.agents.jd_analyzer.agent import jd_analyzer_agent

logger = logging.getLogger(__name__)


class ATSScorerService:
    """
    Two modes:

    1. score_with_comparison — scores BOTH original and optimized resume.
       Shows candidate exactly how much Phase 5 optimization improved their score.
       This is the most useful mode for the end user.

    2. score_single — scores one resume text against a JD.
       Used by Phase 8 orchestrator when it needs a quick score check.
    """

    async def score_with_comparison(
            self,
            original_resume_text: str,
            optimized_resume_text: str,
            jd_text: str,
            job_id: str,
    ) -> dict:
        """
        Score original resume, then optimized resume.
        Return both so user sees the improvement clearly.
        """
        logger.info("ATS comparison scoring job_id=%s", job_id)

        # Step 1: Analyze JD once — reuse for both scoring runs
        analyzed_jd = await jd_analyzer_agent.analyze(
            jd_text=jd_text,
            job_id=job_id,
        )

        # Step 2: Score original resume — get baseline
        original_score = await ats_scorer_agent.score(
            resume_text=original_resume_text,
            analyzed_jd=analyzed_jd,
            job_id=f"{job_id}-original",
        )

        # Step 3: Score optimized resume — pass original as baseline
        optimized_score = await ats_scorer_agent.score(
            resume_text=optimized_resume_text,
            analyzed_jd=analyzed_jd,
            job_id=f"{job_id}-optimized",
            before_score=original_score.overall_ats_score,
        )

        return {
            "original":  original_score,
            "optimized": optimized_score,
            "improvement": round(
                optimized_score.overall_ats_score - original_score.overall_ats_score, 1
            ),
        }

    async def score_single(
            self,
            resume_text: str,
            jd_text: str,
            job_id: str,
            before_score: Optional[float] = None,
    ) -> ATSScoreResult:
        analyzed_jd = await jd_analyzer_agent.analyze(
            jd_text=jd_text,
            job_id=job_id,
        )
        return await ats_scorer_agent.score(
            resume_text=resume_text,
            analyzed_jd=analyzed_jd,
            job_id=job_id,
            before_score=before_score,
        )


ats_scorer_service = ATSScorerService()