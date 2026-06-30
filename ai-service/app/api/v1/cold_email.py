import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.agents.cold_email.schemas import ColdEmailResult
from app.services.cold_email_service import cold_email_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/email", tags=["cold-email"])


class GenerateEmailRequest(BaseModel):
    resume_id:   str = Field(description="Unique resume ID")
    job_id:      str = Field(description="Unique job ID")
    resume_text: str = Field(description="Full resume text")
    jd_text:     str = Field(description="Full job description text")


class GenerateEmailResponse(BaseModel):
    resume_id: str
    job_id:    str
    emails:    ColdEmailResult


@router.post(
    "/generate",
    response_model=GenerateEmailResponse,
    summary="Generate cold email variants for a job application",
    description=(
            "Runs the full pipeline: parses resume, analyzes JD, scores ATS, "
            "then generates 3 personalized cold email variants plus a follow-up. "
            "Uses all previous phase outputs as context for maximum personalization."
    ),
)
async def generate_email(body: GenerateEmailRequest) -> GenerateEmailResponse:
    try:
        result = await cold_email_service.generate_from_raw(
            resume_text=body.resume_text,
            jd_text=body.jd_text,
            resume_id=body.resume_id,
            job_id=body.job_id,
        )
        return GenerateEmailResponse(
            resume_id=body.resume_id,
            job_id=body.job_id,
            emails=result,
        )
    except Exception as exc:
        logger.error("Cold email endpoint error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Email generation failed: {str(exc)}"
        )