import logging
import time
from typing import Optional
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.core.config import settings

logger = logging.getLogger(__name__)


class ATSScorerAgent:
    """
    Scores a resume against a job description using ATS simulation.

    Two inputs:
    - resume_text: the raw or optimized resume text
    - analyzed_jd: structured JD from Phase 4 (already parsed)

    Two modes:
    - Score original resume → get baseline
    - Score optimized resume → see improvement
    Both scores stored so candidate sees before/after improvement.
    """

    async def score(
            self,
            resume_text: str,
            analyzed_jd: AnalyzedJD,
            job_id: str,
            before_score: Optional[float] = None,
    ) -> ATSScoreResult:

        if not resume_text or not resume_text.strip():
            raise ValueError(f"Empty resume_text for job_id={job_id}")

        if settings.MOCK_LLM:
            logger.info("MOCK MODE — returning fake ATS score for job_id=%s", job_id)
            return self._get_mock_result(before_score)

        from app.agents.ats_scorer.chain import get_ats_scorer_chain
        chain = get_ats_scorer_chain()
        start = time.monotonic()

        try:
            logger.info(
                "ATS scoring started job_id=%s resume_length=%d",
                job_id, len(resume_text),
            )

            result: ATSScoreResult = await chain.ainvoke({
                "resume_text":         resume_text,
                "job_title":           analyzed_jd.job_title,
                "required_skills":     ", ".join(analyzed_jd.required_skills),
                "preferred_skills":    ", ".join(analyzed_jd.preferred_skills),
                "min_experience_years": str(analyzed_jd.min_experience_years or 0),
                "key_responsibilities": "\n".join(
                    f"- {r}" for r in analyzed_jd.key_responsibilities
                ),
            })

            # Attach before/after comparison if baseline provided
            if before_score is not None:
                result.before_optimization_score = before_score
                result.score_improvement = round(
                    result.overall_ats_score - before_score, 1
                )

            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.info(
                "ATS scoring complete job_id=%s score=%s pass=%s duration_ms=%d",
                job_id, result.overall_ats_score,
                result.will_pass_ats, elapsed_ms,
            )
            return result

        except Exception as exc:
            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.error(
                "ATS scoring failed job_id=%s duration_ms=%d error=%s",
                job_id, elapsed_ms, str(exc),
                exc_info=True,
            )
            raise

    def _get_mock_result(
            self, before_score: Optional[float] = None
    ) -> ATSScoreResult:
        from app.agents.ats_scorer.schemas import KeywordMatch, SectionScore
        result = ATSScoreResult(
            overall_ats_score=74.0,
            keyword_match_score=80.0,
            format_score=70.0,
            relevance_score=72.0,
            will_pass_ats=True,
            verdict=(
                "Resume will pass ATS screening. Strong keyword match on "
                "core skills. Minor improvements to summary and formatting "
                "will push score above 80."
            ),
            keyword_matches=[
                KeywordMatch(keyword="Python",         found=True,  frequency=3, importance="critical"),
                KeywordMatch(keyword="Apache Kafka",   found=True,  frequency=2, importance="critical"),
                KeywordMatch(keyword="Apache Spark",   found=True,  frequency=2, importance="critical"),
                KeywordMatch(keyword="SQL",            found=True,  frequency=1, importance="critical"),
                KeywordMatch(keyword="AWS",            found=True,  frequency=2, importance="critical"),
                KeywordMatch(keyword="Airflow",        found=True,  frequency=1, importance="important"),
                KeywordMatch(keyword="dbt",            found=False, frequency=0, importance="minor"),
                KeywordMatch(keyword="Terraform",      found=False, frequency=0, importance="minor"),
            ],
            missing_critical_keywords=[],
            matched_keywords=["Python", "Apache Kafka", "Apache Spark", "SQL", "AWS", "Airflow"],
            section_scores=[
                SectionScore(
                    section="skills",
                    score=85.0,
                    feedback="Strong skills section with most required keywords present",
                    fixes=["Add dbt and Terraform to skills section"],
                ),
                SectionScore(
                    section="experience",
                    score=75.0,
                    feedback="Good experience but needs more quantifiable achievements",
                    fixes=[
                        "Add specific metrics to every bullet point",
                        "Mention fintech or financial domain experience",
                    ],
                ),
                SectionScore(
                    section="summary",
                    score=65.0,
                    feedback="Summary is too generic — ATS cannot detect role alignment",
                    fixes=[
                        "Add job title 'Senior Data Engineer' in first sentence",
                        "Mention 'real-time pipelines' and 'fintech' explicitly",
                    ],
                ),
                SectionScore(
                    section="education",
                    score=80.0,
                    feedback="Education section is clear and ATS-parseable",
                    fixes=[],
                ),
            ],
            critical_fixes=[
                "Add job title 'Senior Data Engineer' to resume summary",
                "Ensure 'Apache Kafka' and 'Apache Spark' appear as full names not abbreviations",
            ],
            recommended_fixes=[
                "Add dbt to skills — it appears in preferred skills",
                "Quantify all experience bullets with numbers and percentages",
                "Add 'fintech' or 'financial services' to summary",
            ],
        )
        if before_score is not None:
            result.before_optimization_score = before_score
            result.score_improvement = round(result.overall_ats_score - before_score, 1)
        return result


ats_scorer_agent = ATSScorerAgent()