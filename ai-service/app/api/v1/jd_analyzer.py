import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.services.jd_analyzer_service import jd_analyzer_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/jobs", tags=["jd-analyzer"])


class AnalyzeJDRequest(BaseModel):
    job_id:  str         = Field(description="Unique ID for this job")
    jd_text: str         = Field(description="Full job description text")


class AnalyzeJDResponse(BaseModel):
    job_id:   str
    analyzed: AnalyzedJD


@router.post(
    "/analyze",
    response_model=AnalyzeJDResponse,
    summary="Analyze a job description",
    description=(
            "Extracts structured requirements from a raw job description. "
            "Returns required skills, seniority, experience, responsibilities, "
            "and red flags. Used by Phase 5 optimizer and Phase 6 ATS scorer."
    ),
)
async def analyze_jd(body: AnalyzeJDRequest) -> AnalyzeJDResponse:
    try:
        analyzed = await jd_analyzer_service.analyze(
            jd_text=body.jd_text,
            job_id=body.job_id,
        )
        return AnalyzeJDResponse(job_id=body.job_id, analyzed=analyzed)
    except Exception as exc:
        logger.error("JD analyzer endpoint error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"JD analysis failed: {str(exc)}")