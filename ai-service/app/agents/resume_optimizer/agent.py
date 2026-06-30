import logging
import time
from app.agents.resume_optimizer.schemas import ResumeOptimizationResult
from app.agents.resume_parser.schemas import ParsedResume
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.core.config import settings

logger = logging.getLogger(__name__)


def _format_work_experience(resume: ParsedResume) -> str:
    """Format work experience into clean text for the prompt."""
    lines = []
    for exp in resume.work_experience:
        lines.append(
            f"- {exp.title} at {exp.company} "
            f"({exp.start_date or '?'} - {exp.end_date or '?'})"
        )
        for resp in exp.responsibilities:
            lines.append(f"  * {resp}")
        if exp.technologies:
            lines.append(f"  Technologies: {', '.join(exp.technologies)}")
    return "\n".join(lines) if lines else "Not provided"


def _format_education(resume: ParsedResume) -> str:
    """Format education into clean text for the prompt."""
    lines = []
    for edu in resume.education:
        lines.append(
            f"- {edu.degree} at {edu.institution} "
            f"({edu.graduation_year or '?'})"
        )
    return "\n".join(lines) if lines else "Not provided"


class ResumeOptimizerAgent:
    """
    Optimizes a resume against a specific job description.

    This is RAG in action:
    - Retrieval: structured resume data (Phase 2) + structured JD (Phase 4)
    - Augmentation: both fed into the prompt as rich context
    - Generation: LLM rewrites and optimizes with full context

    The key insight: we don't ask the LLM to optimize blindly.
    We give it the exact requirements from Phase 4 and the exact
    candidate profile from Phase 2. The output is targeted, not generic.
    """

    async def optimize(
            self,
            resume: ParsedResume,
            analyzed_jd: AnalyzedJD,
            job_id: str,
    ) -> ResumeOptimizationResult:

        if settings.MOCK_LLM:
            logger.info("MOCK MODE — returning fake optimization for job_id=%s", job_id)
            return self._get_mock_result()

        from app.agents.resume_optimizer.chain import get_optimizer_chain
        chain = get_optimizer_chain()
        start = time.monotonic()

        try:
            logger.info(
                "Optimizing resume for job_id=%s candidate=%s",
                job_id, resume.full_name,
            )

            # Build the prompt variables from structured objects
            # This is the RAG step — structured retrieval feeding generation
            result: ResumeOptimizationResult = await chain.ainvoke({
                # Resume fields
                "full_name":           resume.full_name or "Unknown",
                "summary":             resume.summary or "Not provided",
                "experience_years":    str(resume.total_experience_years or 0),
                "programming_languages": ", ".join(resume.programming_languages),
                "frameworks_and_tools":  ", ".join(resume.frameworks_and_tools),
                "skills":              ", ".join(resume.skills),
                "work_experience":     _format_work_experience(resume),
                "education":           _format_education(resume),
                "certifications":      ", ".join(resume.certifications) or "None",

                # JD fields
                "job_title":           analyzed_jd.job_title,
                "seniority_level":     analyzed_jd.seniority_level.value,
                "min_experience_years": str(analyzed_jd.min_experience_years or 0),
                "required_skills":     ", ".join(analyzed_jd.required_skills),
                "preferred_skills":    ", ".join(analyzed_jd.preferred_skills),
                "key_responsibilities": "\n".join(
                    f"- {r}" for r in analyzed_jd.key_responsibilities
                ),
                "domain":              analyzed_jd.domain or "tech",
                "job_summary":         analyzed_jd.summary,
            })

            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.info(
                "Optimization complete job_id=%s match_score=%s duration_ms=%d",
                job_id, result.overall_match_score, elapsed_ms,
            )
            return result

        except Exception as exc:
            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.error(
                "Optimization failed job_id=%s duration_ms=%d error=%s",
                job_id, elapsed_ms, str(exc),
                exc_info=True,
            )
            raise

    def _get_mock_result(self) -> ResumeOptimizationResult:
        from app.agents.resume_optimizer.schemas import (
            SkillGap, OptimizationSuggestion
        )
        return ResumeOptimizationResult(
            overall_match_score=72.0,
            match_summary=(
                "Strong match on core data engineering skills — Python, Kafka, "
                "Spark, and AWS align well. Main gaps are dbt and Terraform "
                "which are preferred but not required."
            ),
            skill_gaps=[
                SkillGap(
                    skill="dbt",
                    priority="nice-to-have",
                    suggestion="Add a personal project using dbt for data transformation"
                ),
                SkillGap(
                    skill="Terraform",
                    priority="nice-to-have",
                    suggestion="Complete HashiCorp Terraform Associate certification"
                ),
            ],
            strong_matches=[
                "Python — 5 years, strong match",
                "Apache Kafka — production experience at scale",
                "Apache Spark — real-time pipeline experience",
                "AWS — cloud platform match",
                "Real-time pipeline experience — direct match to role",
            ],
            suggestions=[
                OptimizationSuggestion(
                    section="summary",
                    issue="Current summary is too generic",
                    suggestion="Rewrite to mention real-time pipelines, scale, and fintech domain",
                    impact="high",
                ),
                OptimizationSuggestion(
                    section="experience",
                    issue="Responsibilities lack quantifiable metrics",
                    suggestion="Add specific numbers: pipeline throughput, latency improvements, team size",
                    impact="high",
                ),
            ],
            optimized_summary=(
                "Senior Data Engineer with 5+ years building mission-critical "
                "real-time data pipelines processing millions of events daily. "
                "Deep expertise in Python, Apache Kafka, Spark, and AWS with "
                "proven track record of reducing data latency and scaling "
                "infrastructure in high-growth environments."
            ),
            optimized_skills=[
                "Python", "Apache Kafka", "Apache Spark", "SQL",
                "AWS", "Airflow", "Docker", "PostgreSQL", "Scala"
            ],
            optimized_experience=[
                "Architected and built real-time event streaming pipelines "
                "processing 10M+ events/day using Kafka and Spark, reducing "
                "data latency from 1 hour to under 30 seconds",
                "Led migration from on-premise Hadoop cluster to AWS EMR, "
                "cutting infrastructure costs by 40% and improving reliability",
                "Mentored 3 junior data engineers, conducting code reviews "
                "and establishing team best practices for pipeline development",
            ],
            ats_keywords_added=[
                "real-time data pipelines", "Apache Kafka", "Apache Spark",
                "AWS", "data engineering", "fintech", "batch processing"
            ],
            keywords_to_add=["dbt", "Terraform", "feature engineering"],
        )


resume_optimizer_agent = ResumeOptimizerAgent()