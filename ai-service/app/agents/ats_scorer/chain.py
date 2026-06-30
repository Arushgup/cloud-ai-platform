import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSerializable

from app.agents.ats_scorer.prompt import ATS_SCORER_PROMPT_V1
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.core.config import settings

logger = logging.getLogger(__name__)

_chain: Optional[RunnableSerializable] = None


def get_ats_scorer_chain() -> RunnableSerializable:
    global _chain
    if _chain is None:
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0,     # scoring must be deterministic
            max_retries=2,
        )

        structured_llm = llm.with_structured_output(
            ATSScoreResult,
            method="function_calling",
        )

        _chain = ATS_SCORER_PROMPT_V1 | structured_llm
        logger.info("ATS scorer chain built with model: %s", settings.GROQ_MODEL)

    return _chain