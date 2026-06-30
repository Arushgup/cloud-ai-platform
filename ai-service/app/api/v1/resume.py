import logging
import traceback
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.agents.resume_parser.schemas import ParsedResume
from app.services.resume_service import resume_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/resume", tags=["resume"])


class ParseResumeRequest(BaseModel):
    resume_id:   str
    user_id:     str
    user_email:  str
    resume_text: str
    file_name:   str = "manual_upload.pdf"


class ParseResumeResponse(BaseModel):
    resume_id: str
    parsed:    ParsedResume


@router.post(
    "/parse",
    response_model=ParseResumeResponse,
    status_code=status.HTTP_200_OK,
)
async def parse_resume(body: ParseResumeRequest) -> ParseResumeResponse:
    try:
        parsed = await resume_service.process(
            resume_id=body.resume_id,
            user_id=body.user_id,
            user_email=body.user_email,
            resume_text=body.resume_text,
            file_name=body.file_name,
        )
        return ParseResumeResponse(resume_id=body.resume_id, parsed=parsed)

    except Exception as exc:
        # Print the FULL traceback to terminal so we can see the real error
        logger.error("Parse endpoint error: %s", traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(exc)}"
        )
