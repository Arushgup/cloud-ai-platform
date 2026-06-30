import logging
from langgraph.graph import StateGraph, END

from app.orchestration.state import AgentState
from app.orchestration.nodes import (
    parse_resume_node,
    analyze_jd_node,
    match_job_node,
    score_original_ats_node,
    optimize_resume_node,
    score_optimized_ats_node,
    generate_email_node,
)

logger = logging.getLogger(__name__)


def should_optimize_router(state: AgentState) -> str:
    """
    Conditional edge — decides which node to run next.

    If ATS score < 85: run optimizer → score again → generate email
    If ATS score >= 85: skip optimizer → go straight to email

    This is the intelligence of the graph.
    Not every resume needs optimization — strong resumes skip expensive LLM calls.
    """
    if state.get("error"):
        logger.warning("Error detected in state — routing to END")
        return "end"

    if state.get("should_optimize", True):
        logger.info("Routing to optimizer — ATS score below threshold")
        return "optimize"
    else:
        logger.info("Skipping optimizer — ATS score already strong")
        return "skip_optimize"


def build_graph() -> StateGraph:
    """
    Build the complete multi-agent graph.

    Flow:
        parse_resume ──┐
        analyze_jd  ──┤→ match_job → score_original_ats
                                            │
                          score < 85 ───────┤
                               │            │ score >= 85
                        optimize_resume     │
                               │            │
                        score_optimized_ats │
                               └────────────┘
                                      │
                               generate_email
                                      │
                                     END
    """
    graph = StateGraph(AgentState)

    # Add all nodes
    graph.add_node("parse_resume",        parse_resume_node)
    graph.add_node("analyze_jd",          analyze_jd_node)
    graph.add_node("match_job",           match_job_node)
    graph.add_node("score_original_ats",  score_original_ats_node)
    graph.add_node("optimize_resume",     optimize_resume_node)
    graph.add_node("score_optimized_ats", score_optimized_ats_node)
    graph.add_node("generate_email",      generate_email_node)

    # Entry point — two nodes run first (parse resume + analyze JD)
    graph.set_entry_point("parse_resume")

    # Linear edges — always run in this order
    graph.add_edge("parse_resume",       "analyze_jd")
    graph.add_edge("analyze_jd",         "match_job")
    graph.add_edge("match_job",          "score_original_ats")

    # Conditional edge — router decides optimize vs skip
    graph.add_conditional_edges(
        "score_original_ats",
        should_optimize_router,
        {
            "optimize":      "optimize_resume",
            "skip_optimize": "generate_email",
            "end":           END,
        },
    )

    # After optimization — always score again then email
    graph.add_edge("optimize_resume",     "score_optimized_ats")
    graph.add_edge("score_optimized_ats", "generate_email")

    # Final node → END
    graph.add_edge("generate_email", END)

    return graph.compile()


# Module-level compiled graph — built once, reused for every request
compiled_graph = build_graph()
logger.info("LangGraph multi-agent graph compiled successfully")