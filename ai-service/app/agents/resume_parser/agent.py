import logging
import time
from typing import Optional
from app.agents.resume_parser.chain import get_parser_chain
from app.agents.resume_parser.schemas import ParsedResume

logger = logging.getLogger(__name__)


class ResumeParserAgent:
    """
    Stateless agent wrapping the Gemini parsing chain.
    """

    async def parse(self, resume_text: str, resume_id: str) -> ParsedResume:
        if not resume_text or not resume_text.strip():
            raise ValueError(f"Empty resume_text for resume_id={resume_id}")

        chain = get_parser_chain()
        start = time.monotonic()

        try:
            logger.info(
                "Parsing resume resume_id=%s text_length=%d",
                resume_id, len(resume_text)
            )

            result: ParsedResume = await chain.ainvoke({"resume_text": resume_text})
            result.raw_text_length = len(resume_text)

            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.info(
                "Parse complete resume_id=%s duration_ms=%d skills=%d experience_years=%s",
                resume_id, elapsed_ms, len(result.skills), result.total_experience_years,
            )
            return result

        except Exception as exc:
            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.error(
                "Parse failed resume_id=%s duration_ms=%d error=%s",
                resume_id, elapsed_ms, str(exc),
                exc_info=True,
            )
            raise


resume_parser_agent = ResumeParserAgent()