import logging
from app.agents.job_matcher.schemas import JobMatchRequest, JobMatchResponse
from app.agents.job_matcher.agent import job_matcher_agent

logger = logging.getLogger(__name__)


class JobMatchService:
    """
    Service layer for job matching.
    Thin wrapper around the agent — keeps the architecture consistent.
    In Phase 8 this will also trigger downstream agents:
        match → optimizer → ATS scorer → email generator
    """

    async def match_job(self, request: JobMatchRequest) -> JobMatchResponse:
        logger.info(
            "Job match service called job_id=%s", request.job_id
        )
        return await job_matcher_agent.match(request)


job_match_service = JobMatchService()