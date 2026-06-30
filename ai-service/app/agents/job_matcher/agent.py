import logging
import time
from app.agents.job_matcher.schemas import JobMatchRequest, JobMatchResponse, ResumeMatch
from app.embeddings.embedder import generate_embedding
from app.vectorstore.chroma_store import query_similar, get_collection

logger = logging.getLogger(__name__)


class JobMatcherAgent:
    """
    Matches a job description against all stored resumes using vector similarity.

    How it works:
    1. Convert job description text into a vector (same embedder as resumes)
    2. Query ChromaDB for the N closest resume vectors
    3. Convert cosine distances into human-readable match scores
    4. Return ranked list of candidates

    No LLM needed here — pure math.
    This is the fastest and most scalable part of the system.
    """

    async def match(self, request: JobMatchRequest) -> JobMatchResponse:
        start = time.monotonic()

        logger.info(
            "Job matching started job_id=%s title=%s n_results=%d",
            request.job_id, request.job_title, request.n_results,
        )

        # Step 1: Check how many resumes exist
        collection = get_collection()
        total_resumes = collection.count()

        if total_resumes == 0:
            logger.warning("No resumes in ChromaDB — returning empty matches")
            return JobMatchResponse(
                job_id=request.job_id,
                job_title=request.job_title,
                total_found=0,
                matches=[],
            )

        # Step 2: Build embedding text from job description
        # We clean it the same way we clean resume text —
        # consistent embedding space = better similarity scores
        embedding_text = self._build_job_embedding_text(
            request.job_title,
            request.job_description,
        )

        # Step 3: Convert job description to vector
        job_vector = generate_embedding(embedding_text)

        # Step 4: Query ChromaDB — find closest resume vectors
        # n_results capped at actual collection size to avoid ChromaDB error
        n = min(request.n_results, total_resumes)
        raw_results = query_similar(
            query_embedding=job_vector,
            n_results=n,
        )

        # Step 5: Convert raw results into typed ResumeMatch objects
        matches = self._parse_results(raw_results)

        elapsed_ms = round((time.monotonic() - start) * 1000)
        logger.info(
            "Job matching complete job_id=%s matches=%d duration_ms=%d",
            request.job_id, len(matches), elapsed_ms,
        )

        return JobMatchResponse(
            job_id=request.job_id,
            job_title=request.job_title,
            total_found=total_resumes,
            matches=matches,
        )

    def _build_job_embedding_text(self, title: str, description: str) -> str:
        """
        Build a clean embedding text from the job posting.

        Key insight: we embed job descriptions and resumes in the
        SAME format so their vectors live in the same semantic space.
        Consistent format = meaningful similarity scores.
        """
        # Take first 2000 chars of description to stay within model limits
        cleaned = description.strip()[:2000]
        return f"Job Title: {title}\n{cleaned}"

    def _parse_results(self, raw_results: dict) -> list[ResumeMatch]:
        """
        Convert ChromaDB raw query results into ResumeMatch objects.

        ChromaDB returns parallel lists:
            ids[0]        = list of matched resume IDs
            distances[0]  = list of cosine distances (0=identical, 1=opposite)
            metadatas[0]  = list of metadata dicts we stored in Phase 2

        We convert distance → match_score so humans can read it:
            match_score = (1 - distance) * 100
            distance 0.05 → score 95  (excellent match)
            distance 0.30 → score 70  (good match)
            distance 0.60 → score 40  (weak match)
        """
        matches = []

        ids        = raw_results.get("ids", [[]])[0]
        distances  = raw_results.get("distances", [[]])[0]
        metadatas  = raw_results.get("metadatas", [[]])[0]

        for resume_id, distance, metadata in zip(ids, distances, metadatas):
            # Convert cosine distance to a 0-100 match score
            match_score = round((1 - distance) * 100, 1)

            matches.append(ResumeMatch(
                resume_id=resume_id,
                full_name=metadata.get("full_name", "Unknown"),
                user_email=metadata.get("user_email", ""),
                experience_years=float(metadata.get("experience_years", 0)),
                top_skills=metadata.get("top_skills", ""),
                match_score=match_score,
                distance=round(distance, 4),
            ))

        # Sort by match_score descending — best match first
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches


# Module-level singleton
job_matcher_agent = JobMatcherAgent()