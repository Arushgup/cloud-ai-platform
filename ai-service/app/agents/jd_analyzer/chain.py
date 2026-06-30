import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSerializable

from app.agents.jd_analyzer.prompt import JD_ANALYZER_PROMPT_V1
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.core.config import settings

logger = logging.getLogger(__name__)

_chain: Optional[RunnableSerializable] = None


def get_jd_analyzer_chain() -> RunnableSerializable:
    """
    Same pattern as resume parser chain.
    Groq + structured output + versioned prompt.
    Changing the LLM provider only requires changing this file.
    """
    global _chain
    if _chain is None:
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0,
            max_retries=2,
        )

        structured_llm = llm.with_structured_output(
            AnalyzedJD,
            method="function_calling",
        )

        _chain = JD_ANALYZER_PROMPT_V1 | structured_llm
        logger.info("JD analyzer chain built with model: %s", settings.GROQ_MODEL)

    return _chain