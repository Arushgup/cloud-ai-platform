import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSerializable

from app.agents.resume_parser.prompt import RESUME_PARSER_PROMPT_V1
from app.agents.resume_parser.schemas import ParsedResume
from app.core.config import settings

logger = logging.getLogger(__name__)

_chain: Optional[RunnableSerializable] = None


def get_parser_chain() -> RunnableSerializable:
    """
    Builds the LangChain chain using Groq.

    Why Groq?
    - Genuinely free tier, no credit card
    - Fastest LLM inference available (runs on custom LPU hardware)
    - llama-3.3-70b is excellent at structured extraction tasks
    - Same LangChain interface — zero changes outside this file
    """
    global _chain
    if _chain is None:
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0,        # deterministic output for extraction
            max_retries=2,
        )

        # with_structured_output forces the model to return
        # a valid ParsedResume object — cannot return malformed JSON
        structured_llm = llm.with_structured_output(
            ParsedResume,
            method="function_calling",
        )

        _chain = RESUME_PARSER_PROMPT_V1 | structured_llm
        logger.info(
            "Resume parser chain built with Groq model: %s", settings.GROQ_MODEL
        )

    return _chain