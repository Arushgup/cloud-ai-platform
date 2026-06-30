import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.agents.resume_optimizer.schemas import ResumeOptimizationResult
from app.services.resume_optimizer_service import resume_optimizer_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/resume", tags=["resume-optimizer"])


class OptimizeResumeRequest(BaseModel):
    resume_id:   str = Field(description="Unique ID for this resume")
    job_id:      str = Field(description="Unique ID for this job")
    resume_text: str = Field(description="Full resume text")
    jd_text:     str = Field(description="Full job description text")


class OptimizeResumeResponse(BaseModel):
    resume_id: str
    job_id:    str
    result:    ResumeOptimizationResult


@router.post(
    "/optimize",
    response_model=OptimizeResumeResponse,
    summary="Optimize a resume for a specific job",
    description=(
            "Parses the resume, analyzes the JD, then generates gap analysis, "
            "improvement suggestions, and a fully rewritten resume tailored "
            "to the job. This is the RAG pipeline."
    ),
)
async def optimize_resume(body: OptimizeResumeRequest) -> OptimizeResumeResponse:
    try:
        result = await resume_optimizer_service.optimize_from_raw(
            resume_text=body.resume_text,
            jd_text=body.jd_text,
            resume_id=body.resume_id,
            job_id=body.job_id,
        )
        return OptimizeResumeResponse(
            resume_id=body.resume_id,
            job_id=body.job_id,
            result=result,
        )
    except Exception as exc:
        logger.error("Optimizer endpoint error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Resume optimization failed: {str(exc)}"
        )