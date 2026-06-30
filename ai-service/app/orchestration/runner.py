import logging
import time
from app.orchestration.state import AgentState
from app.orchestration.graph import compiled_graph

logger = logging.getLogger(__name__)


async def run_pipeline(
        resume_id: str,
        job_id: str,
        resume_text: str,
        jd_text: str,
) -> AgentState:
    """
    Run the full multi-agent pipeline.

    Input:  raw resume text + raw JD text
    Output: fully populated AgentState with all agent results

    The graph handles:
    - Agent sequencing
    - Conditional optimization routing
    - State passing between agents
    - Error propagation
    """
    initial_state: AgentState = {
        "resume_id":           resume_id,
        "job_id":              job_id,
        "resume_text":         resume_text,
        "jd_text":             jd_text,
        "parsed_resume":       None,
        "analyzed_jd":         None,
        "match_score":         None,
        "optimization":        None,
        "ats_score_original":  None,
        "ats_score_optimized": None,
        "cold_emails":         None,
        "should_optimize":     True,
        "error":               None,
        "completed_nodes":     [],
    }

    start = time.monotonic()
    logger.info(
        "Pipeline started resume_id=%s job_id=%s",
        resume_id, job_id,
    )

    final_state: AgentState = await compiled_graph.ainvoke(initial_state)

    elapsed_ms = round((time.monotonic() - start) * 1000)
    logger.info(
        "Pipeline complete resume_id=%s job_id=%s nodes=%s duration_ms=%d error=%s",
        resume_id, job_id,
        final_state.get("completed_nodes", []),
        elapsed_ms,
        final_state.get("error"),
    )

    return final_state