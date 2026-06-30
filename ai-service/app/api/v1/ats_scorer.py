import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.services.ats_scorer_service import ats_scorer_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/ats", tags=["ats-scorer"])


class ScoreSingleRequest(BaseModel):
    job_id:      str           = Field(description="Unique job ID")
    resume_text: str           = Field(description="Resume text to score")
    jd_text:     str           = Field(description="Job description text")


class ScoreComparisonRequest(BaseModel):
    job_id:                str = Field(description="Unique job ID")
    original_resume_text:  str = Field(description="Original resume before optimization")
    optimized_resume_text: str = Field(description="Optimized resume from Phase 5")
    jd_text:               str = Field(description="Job description text")


class ScoreSingleResponse(BaseModel):
    job_id: str
    score:  ATSScoreResult


class ScoreComparisonResponse(BaseModel):
    job_id:      str
    original:    ATSScoreResult
    optimized:   ATSScoreResult
    improvement: float = Field(description="Score improvement after optimization")


@router.post(
    "/score",
    response_model=ScoreSingleResponse,
    summary="Score a single resume against a job description",
)
async def score_resume(body: ScoreSingleRequest) -> ScoreSingleResponse:
    try:
        score = await ats_scorer_service.score_single(
            resume_text=body.resume_text,
            jd_text=body.jd_text,
            job_id=body.job_id,
        )
        return ScoreSingleResponse(job_id=body.job_id, score=score)
    except Exception as exc:
        logger.error("ATS score endpoint error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"ATS scoring failed: {str(exc)}")


@router.post(
    "/score/compare",
    response_model=ScoreComparisonResponse,
    summary="Compare ATS scores before and after optimization",
    description=(
            "Scores both original and optimized resume against the same JD. "
            "Shows exactly how much Phase 5 optimization improved ATS compatibility."
    ),
)
async def compare_scores(body: ScoreComparisonRequest) -> ScoreComparisonResponse:
    try:
        result = await ats_scorer_service.score_with_comparison(
            original_resume_text=body.original_resume_text,
            optimized_resume_text=body.optimized_resume_text,
            jd_text=body.jd_text,
            job_id=body.job_id,
        )
        return ScoreComparisonResponse(
            job_id=body.job_id,
            original=result["original"],
            optimized=result["optimized"],
            improvement=result["improvement"],
        )
    except Exception as exc:
        logger.error("ATS compare endpoint error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"ATS comparison failed: {str(exc)}")