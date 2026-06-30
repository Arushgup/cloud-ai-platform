from typing import Optional, TypedDict
from app.agents.resume_parser.schemas import ParsedResume
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.agents.resume_optimizer.schemas import ResumeOptimizationResult
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.agents.cold_email.schemas import ColdEmailResult


class AgentState(TypedDict):
    """
    Shared state that flows through every node in the graph.

    Each node reads what it needs and writes its output back.
    This is how LangGraph agents communicate — through state,
    not through direct function calls.

    Think of it as a baton passed in a relay race.
    Each runner (agent) picks it up, does their job, passes it forward.
    """
    # Inputs — provided by the user
    resume_id:    str
    job_id:       str
    resume_text:  str
    jd_text:      str

    # Phase 2 output
    parsed_resume: Optional[ParsedResume]

    # Phase 4 output
    analyzed_jd:   Optional[AnalyzedJD]

    # Phase 3 output
    match_score:   Optional[float]

    # Phase 5 output
    optimization:  Optional[ResumeOptimizationResult]

    # Phase 6 output — scored twice (before and after optimization)
    ats_score_original:   Optional[ATSScoreResult]
    ats_score_optimized:  Optional[ATSScoreResult]

    # Phase 7 output
    cold_emails:   Optional[ColdEmailResult]

    # Control flow
    should_optimize:  bool    # set by router node
    error:            Optional[str]
    completed_nodes:  list[str]