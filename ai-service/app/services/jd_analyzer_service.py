import logging
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.agents.jd_analyzer.agent import jd_analyzer_agent

logger = logging.getLogger(__name__)


class JDAnalyzerService:
    """
    Orchestrates JD analysis.
    In Phase 8 this will chain directly into job matching:
        analyze JD → build better embedding → match resumes
    """

    async def analyze(self, jd_text: str, job_id: str) -> AnalyzedJD:
        logger.info("JD analyzer service called job_id=%s", job_id)
        return await jd_analyzer_agent.analyze(jd_text=jd_text, job_id=job_id)


jd_analyzer_service = JDAnalyzerService()