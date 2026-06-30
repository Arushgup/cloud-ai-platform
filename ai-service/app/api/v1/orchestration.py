import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.agents.resume_parser.schemas import ParsedResume
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.agents.resume_optimizer.schemas import ResumeOptimizationResult
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.agents.cold_email.schemas import ColdEmailResult
from app.orchestration.runner import run_pipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/pipeline", tags=["orchestration"])


class RunPipelineRequest(BaseModel):
    resume_id:   str = Field(description="Unique resume ID")
    job_id:      str = Field(description="Unique job ID")
    resume_text: str = Field(description="Full resume text")
    jd_text:     str = Field(description="Full job description text")


class PipelineResponse(BaseModel):
    """
    Complete pipeline result — everything in one response.
    This is what the frontend receives from a single API call.
    """
    resume_id:    str
    job_id:       str

    # All agent outputs
    parsed_resume:        Optional[ParsedResume]           = None
    analyzed_jd:          Optional[AnalyzedJD]             = None
    match_score:          Optional[float]                  = None
    optimization:         Optional[ResumeOptimizationResult] = None
    ats_score_original:   Optional[ATSScoreResult]         = None
    ats_score_optimized:  Optional[ATSScoreResult]         = None
    cold_emails:          Optional[ColdEmailResult]        = None

    # Pipeline metadata
    completed_nodes:      list[str]                        = []
    optimization_skipped: bool                             = False
    error:                Optional[str]                    = None


@router.post(
    "/run",
    response_model=PipelineResponse,
    summary="Run the complete multi-agent pipeline",
    description=(
            "Single endpoint that runs all 7 AI agents in sequence. "
            "Parses resume → analyzes JD → matches job → scores ATS → "
            "optimizes if needed → rescores → generates cold emails. "
            "Returns everything in one response."
    ),
)
async def run_full_pipeline(body: RunPipelineRequest) -> PipelineResponse:
    try:
        state = await run_pipeline(
            resume_id=body.resume_id,
            job_id=body.job_id,
            resume_text=body.resume_text,
            jd_text=body.jd_text,
        )

        if state.get("error"):
            raise HTTPException(
                status_code=500,
                detail=state["error"]
            )

        return PipelineResponse(
            resume_id=body.resume_id,
            job_id=body.job_id,
            parsed_resume=state.get("parsed_resume"),
            analyzed_jd=state.get("analyzed_jd"),
            match_score=state.get("match_score"),
            optimization=state.get("optimization"),
            ats_score_original=state.get("ats_score_original"),
            ats_score_optimized=state.get("ats_score_optimized"),
            cold_emails=state.get("cold_emails"),
            completed_nodes=state.get("completed_nodes", []),
            optimization_skipped="optimize_resume" not in state.get("completed_nodes", []),
            error=state.get("error"),
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Pipeline endpoint error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline failed: {str(exc)}"
        )