import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSerializable

from app.agents.resume_optimizer.prompt import RESUME_OPTIMIZER_PROMPT_V1
from app.agents.resume_optimizer.schemas import ResumeOptimizationResult
from app.core.config import settings

logger = logging.getLogger(__name__)

_chain: Optional[RunnableSerializable] = None


def get_optimizer_chain() -> RunnableSerializable:
    global _chain
    if _chain is None:
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.2,   # slight creativity for rewriting — not zero
            max_retries=2,
        )

        structured_llm = llm.with_structured_output(
            ResumeOptimizationResult,
            method="function_calling",
        )

        _chain = RESUME_OPTIMIZER_PROMPT_V1 | structured_llm
        logger.info("Resume optimizer chain built with model: %s", settings.GROQ_MODEL)

    return _chain