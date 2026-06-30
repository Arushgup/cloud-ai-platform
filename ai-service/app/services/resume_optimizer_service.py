import logging
from app.agents.resume_optimizer.schemas import ResumeOptimizationResult
from app.agents.resume_parser.schemas import ParsedResume
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.agents.resume_optimizer.agent import resume_optimizer_agent
from app.agents.jd_analyzer.agent import jd_analyzer_agent
from app.agents.resume_parser.agent import resume_parser_agent

logger = logging.getLogger(__name__)


class ResumeOptimizerService:
    """
    Orchestrates the full optimization workflow.

    Two modes:
    1. Full mode:  raw resume text + raw JD text → parse both → optimize
    2. Structured: already parsed resume + analyzed JD → optimize directly

    Mode 2 is used in Phase 8 orchestration where previous agents
    have already done the parsing.
    """

    async def optimize_from_raw(
            self,
            resume_text: str,
            jd_text: str,
            resume_id: str,
            job_id: str,
    ) -> ResumeOptimizationResult:
        """
        Full pipeline: parse resume + analyze JD + optimize.
        Used by the REST endpoint.
        """
        logger.info(
            "Full optimization pipeline resume_id=%s job_id=%s",
            resume_id, job_id,
        )

        # Step 1: Parse resume (calls Groq)
        parsed_resume = await resume_parser_agent.parse(
            resume_text=resume_text,
            resume_id=resume_id,
        )

        # Step 2: Analyze JD (calls Groq)
        analyzed_jd = await jd_analyzer_agent.analyze(
            jd_text=jd_text,
            job_id=job_id,
        )

        # Step 3: Optimize (calls Groq with both as context)
        return await resume_optimizer_agent.optimize(
            resume=parsed_resume,
            analyzed_jd=analyzed_jd,
            job_id=job_id,
        )

    async def optimize_from_structured(
            self,
            resume: ParsedResume,
            analyzed_jd: AnalyzedJD,
            job_id: str,
    ) -> ResumeOptimizationResult:
        """
        Structured pipeline: already parsed objects → optimize directly.
        Used by Phase 8 multi-agent orchestrator to avoid redundant LLM calls.
        """
        return await resume_optimizer_agent.optimize(
            resume=resume,
            analyzed_jd=analyzed_jd,
            job_id=job_id,
        )


resume_optimizer_service = ResumeOptimizerService()