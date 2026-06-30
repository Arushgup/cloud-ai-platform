import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSerializable

from app.agents.cold_email.prompt import COLD_EMAIL_PROMPT_V1
from app.agents.cold_email.schemas import ColdEmailResult
from app.core.config import settings

logger = logging.getLogger(__name__)

_chain: Optional[RunnableSerializable] = None


def get_cold_email_chain() -> RunnableSerializable:
    global _chain
    if _chain is None:
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.4,   # some creativity for natural writing
            max_retries=2,
        )

        structured_llm = llm.with_structured_output(
            ColdEmailResult,
            method="function_calling",
        )

        _chain = COLD_EMAIL_PROMPT_V1 | structured_llm
        logger.info("Cold email chain built with model: %s", settings.GROQ_MODEL)

    return _chain