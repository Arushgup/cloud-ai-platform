import logging
from fastapi import APIRouter, HTTPException
from app.agents.job_matcher.schemas import JobMatchRequest, JobMatchResponse
from app.services.job_match_service import job_match_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/jobs", tags=["job-matching"])


@router.post(
    "/match",
    response_model=JobMatchResponse,
    summary="Match a job description against all stored resumes",
    description=(
            "Converts the job description into a vector and finds the "
            "most semantically similar resumes in ChromaDB. "
            "Returns candidates ranked by match score."
    ),
)
async def match_job(body: JobMatchRequest) -> JobMatchResponse:
    try:
        return await job_match_service.match_job(body)
    except Exception as exc:
        logger.error("Job match endpoint error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(exc)}")