import logging
from app.agents.resume_parser.agent import resume_parser_agent
from app.agents.resume_parser.schemas import ParsedResume
from app.embeddings.embedder import generate_embedding
from app.vectorstore.chroma_store import upsert_resume

logger = logging.getLogger(__name__)


class ResumeService:
    """
    Orchestrates the full resume processing pipeline:
    1. Parse raw text with LLM → ParsedResume
    2. Generate embedding from structured content
    3. Store in ChromaDB with rich metadata
    """

    async def process(
            self,
            resume_id: str,
            user_id: str,
            user_email: str,
            resume_text: str,
            file_name: str,
    ) -> ParsedResume:

        # Step 1: Parse with LLM
        parsed = await resume_parser_agent.parse(
            resume_text=resume_text,
            resume_id=resume_id,
        )

        # Step 2: Generate embedding from structured content
        # We embed the structured text, not raw resume text.
        # Structured text produces much better embeddings for job matching.
        embedding_text = self._build_embedding_text(parsed)
        embedding = generate_embedding(embedding_text)

        # Step 3: Store in ChromaDB
        metadata = {
            "resume_id":        resume_id,
            "user_id":          user_id,
            "user_email":       user_email,
            "file_name":        file_name,
            "full_name":        parsed.full_name or "unknown",
            "experience_years": parsed.total_experience_years or 0,
            "top_skills":       ", ".join(parsed.skills[:15]),
            "languages":        ", ".join(parsed.programming_languages[:10]),
        }

        upsert_resume(
            resume_id=resume_id,
            text=embedding_text,
            embedding=embedding,
            metadata=metadata,
        )

        logger.info(
            "Resume processing complete resume_id=%s name=%s",
            resume_id, parsed.full_name,
        )
        return parsed

    def _build_embedding_text(self, parsed: ParsedResume) -> str:
        """
        Build a clean structured text for embedding.

        Why not embed raw resume text?
        Raw resumes have formatting noise, repeated headers, and inconsistent
        structure. This clean representation focuses on the signal — skills,
        roles, education — giving much better semantic search in Phase 3.
        """
        parts = []

        if parsed.summary:
            parts.append(f"Summary: {parsed.summary}")
        if parsed.programming_languages:
            parts.append(f"Languages: {', '.join(parsed.programming_languages)}")
        if parsed.frameworks_and_tools:
            parts.append(f"Frameworks and tools: {', '.join(parsed.frameworks_and_tools)}")
        if parsed.skills:
            parts.append(f"Skills: {', '.join(parsed.skills)}")
        for exp in parsed.work_experience:
            line = f"Role: {exp.title} at {exp.company}"
            if exp.technologies:
                line += f" — {', '.join(exp.technologies)}"
            parts.append(line)
        for edu in parsed.education:
            parts.append(f"Education: {edu.degree} at {edu.institution}")
        if parsed.certifications:
            parts.append(f"Certifications: {', '.join(parsed.certifications)}")

        return "\n".join(parts)


# Module-level singleton
resume_service = ResumeService()