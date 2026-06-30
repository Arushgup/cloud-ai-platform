import logging
import time
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.core.config import settings

logger = logging.getLogger(__name__)


class JDAnalyzerAgent:
    """
    Analyzes a raw job description and returns a structured AnalyzedJD object.
    Stateless — safe to use as a module-level singleton.
    """

    async def analyze(self, jd_text: str, job_id: str) -> AnalyzedJD:
        if not jd_text or not jd_text.strip():
            raise ValueError(f"Empty jd_text for job_id={job_id}")

        # Mock mode — same pattern as resume parser
        if settings.MOCK_LLM:
            logger.info("MOCK MODE — returning fake JD analysis for job_id=%s", job_id)
            return self._get_mock_analysis()

        from app.agents.jd_analyzer.chain import get_jd_analyzer_chain
        chain = get_jd_analyzer_chain()
        start = time.monotonic()

        try:
            logger.info(
                "Analyzing JD job_id=%s text_length=%d",
                job_id, len(jd_text)
            )

            result: AnalyzedJD = await chain.ainvoke({"jd_text": jd_text})
            result.raw_jd_length = len(jd_text)

            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.info(
                "JD analysis complete job_id=%s duration_ms=%d required_skills=%d",
                job_id, elapsed_ms, len(result.required_skills),
            )
            return result

        except Exception as exc:
            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.error(
                "JD analysis failed job_id=%s duration_ms=%d error=%s",
                job_id, elapsed_ms, str(exc),
                exc_info=True,
            )
            raise

    def _get_mock_analysis(self) -> AnalyzedJD:
        from app.agents.jd_analyzer.schemas import SeniorityLevel, EmploymentType
        return AnalyzedJD(
            job_title="Senior Data Engineer",
            company_name="TechCorp",
            seniority_level=SeniorityLevel.SENIOR,
            employment_type=EmploymentType.FULL_TIME,
            location="Bangalore, India / Remote",
            min_experience_years=5.0,
            max_experience_years=8.0,
            required_skills=["Python", "Apache Kafka", "Apache Spark", "SQL", "AWS"],
            preferred_skills=["Airflow", "dbt", "Terraform", "Kubernetes"],
            programming_languages=["Python", "SQL", "Scala"],
            frameworks_and_tools=["Apache Spark", "Kafka", "Airflow", "Docker"],
            cloud_platforms=["AWS", "GCP"],
            key_responsibilities=[
                "Design and build real-time data pipelines",
                "Optimize existing batch processing workflows",
                "Collaborate with ML team on feature engineering",
                "Mentor junior engineers",
            ],
            domain="data engineering",
            summary=(
                "This is a senior individual contributor role focused on "
                "real-time data infrastructure at scale. Strong Python and "
                "Kafka experience is non-negotiable."
            ),
            red_flags=[],
            raw_jd_length=850,
        )


jd_analyzer_agent = JDAnalyzerAgent()