import logging
from app.agents.cold_email.schemas import ColdEmailResult
from app.agents.cold_email.agent import cold_email_agent
from app.agents.resume_parser.agent import resume_parser_agent
from app.agents.jd_analyzer.agent import jd_analyzer_agent
from app.agents.ats_scorer.agent import ats_scorer_agent

logger = logging.getLogger(__name__)


class ColdEmailService:
    """
    Full pipeline: parse resume → analyze JD → score ATS → generate email.
    All context flows through automatically.
    """

    async def generate_from_raw(
            self,
            resume_text: str,
            jd_text: str,
            resume_id: str,
            job_id: str,
    ) -> ColdEmailResult:

        logger.info(
            "Cold email full pipeline resume_id=%s job_id=%s",
            resume_id, job_id,
        )

        # Step 1: Parse resume
        parsed_resume = await resume_parser_agent.parse(
            resume_text=resume_text,
            resume_id=resume_id,
        )

        # Step 2: Analyze JD
        analyzed_jd = await jd_analyzer_agent.analyze(
            jd_text=jd_text,
            job_id=job_id,
        )

        # Step 3: Score ATS — gives the email a credibility hook
        ats_result = await ats_scorer_agent.score(
            resume_text=resume_text,
            analyzed_jd=analyzed_jd,
            job_id=job_id,
        )

        # Step 4: Generate email with full context
        return await cold_email_agent.generate(
            resume=parsed_resume,
            analyzed_jd=analyzed_jd,
            ats_result=ats_result,
            job_id=job_id,
        )


cold_email_service = ColdEmailService()