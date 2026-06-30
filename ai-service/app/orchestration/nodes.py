import logging
from app.orchestration.state import AgentState
from app.agents.resume_parser.agent import resume_parser_agent
from app.agents.jd_analyzer.agent import jd_analyzer_agent
from app.agents.job_matcher.agent import job_matcher_agent
from app.agents.job_matcher.schemas import JobMatchRequest
from app.agents.resume_optimizer.agent import resume_optimizer_agent
from app.agents.ats_scorer.agent import ats_scorer_agent
from app.agents.cold_email.agent import cold_email_agent

logger = logging.getLogger(__name__)


async def parse_resume_node(state: AgentState) -> dict:
    """
    Node 1: Parse the raw resume text into a structured ParsedResume.
    Writes: parsed_resume
    """
    logger.info("Graph node: parse_resume resume_id=%s", state["resume_id"])
    try:
        parsed = await resume_parser_agent.parse(
            resume_text=state["resume_text"],
            resume_id=state["resume_id"],
        )
        return {
            "parsed_resume": parsed,
            "completed_nodes": state.get("completed_nodes", []) + ["parse_resume"],
        }
    except Exception as exc:
        logger.error("parse_resume_node failed: %s", exc)
        return {"error": f"Resume parsing failed: {str(exc)}"}


async def analyze_jd_node(state: AgentState) -> dict:
    """
    Node 2: Analyze the job description into structured AnalyzedJD.
    Reads:  jd_text
    Writes: analyzed_jd
    """
    logger.info("Graph node: analyze_jd job_id=%s", state["job_id"])
    try:
        analyzed = await jd_analyzer_agent.analyze(
            jd_text=state["jd_text"],
            job_id=state["job_id"],
        )
        return {
            "analyzed_jd": analyzed,
            "completed_nodes": state.get("completed_nodes", []) + ["analyze_jd"],
        }
    except Exception as exc:
        logger.error("analyze_jd_node failed: %s", exc)
        return {"error": f"JD analysis failed: {str(exc)}"}


async def match_job_node(state: AgentState) -> dict:
    """
    Node 3: Get initial match score between resume and JD.
    Reads:  jd_text, analyzed_jd
    Writes: match_score
    """
    logger.info("Graph node: match_job job_id=%s", state["job_id"])
    try:
        request = JobMatchRequest(
            job_id=state["job_id"],
            job_title=state["analyzed_jd"].job_title,
            job_description=state["jd_text"],
            n_results=1,
        )
        result = await job_matcher_agent.match(request)
        score = result.matches[0].match_score if result.matches else 0.0
        return {
            "match_score": score,
            "completed_nodes": state.get("completed_nodes", []) + ["match_job"],
        }
    except Exception as exc:
        logger.error("match_job_node failed: %s", exc)
        return {"match_score": 0.0, "error": f"Job matching failed: {str(exc)}"}


async def score_original_ats_node(state: AgentState) -> dict:
    """
    Node 4: Score original resume with ATS — get baseline.
    Reads:  resume_text, analyzed_jd
    Writes: ats_score_original, should_optimize
    """
    logger.info("Graph node: score_original_ats job_id=%s", state["job_id"])
    try:
        score = await ats_scorer_agent.score(
            resume_text=state["resume_text"],
            analyzed_jd=state["analyzed_jd"],
            job_id=f"{state['job_id']}-original",
        )
        # Smart routing: only optimize if score is below 85
        # Above 85 = already strong enough, skip expensive LLM call
        should_optimize = score.overall_ats_score < 85.0

        logger.info(
            "Original ATS score=%.1f should_optimize=%s",
            score.overall_ats_score, should_optimize,
        )
        return {
            "ats_score_original": score,
            "should_optimize": should_optimize,
            "completed_nodes": state.get("completed_nodes", []) + ["score_original_ats"],
        }
    except Exception as exc:
        logger.error("score_original_ats_node failed: %s", exc)
        return {"error": f"ATS scoring failed: {str(exc)}", "should_optimize": True}


async def optimize_resume_node(state: AgentState) -> dict:
    """
    Node 5: Optimize resume against JD (only runs if score < 85).
    Reads:  parsed_resume, analyzed_jd
    Writes: optimization
    """
    logger.info("Graph node: optimize_resume job_id=%s", state["job_id"])
    try:
        result = await resume_optimizer_agent.optimize(
            resume=state["parsed_resume"],
            analyzed_jd=state["analyzed_jd"],
            job_id=state["job_id"],
        )
        return {
            "optimization": result,
            "completed_nodes": state.get("completed_nodes", []) + ["optimize_resume"],
        }
    except Exception as exc:
        logger.error("optimize_resume_node failed: %s", exc)
        return {"error": f"Optimization failed: {str(exc)}"}


async def score_optimized_ats_node(state: AgentState) -> dict:
    """
    Node 6: Score the optimized resume — show improvement.
    Reads:  optimization, analyzed_jd, ats_score_original
    Writes: ats_score_optimized
    """
    logger.info("Graph node: score_optimized_ats job_id=%s", state["job_id"])
    try:
        # Build optimized resume text from optimization result
        optimization = state["optimization"]
        optimized_text = (
                f"{optimization.optimized_summary}\n"
                f"Skills: {', '.join(optimization.optimized_skills)}\n"
                + "\n".join(optimization.optimized_experience)
        )

        before_score = (
            state["ats_score_original"].overall_ats_score
            if state.get("ats_score_original") else None
        )

        score = await ats_scorer_agent.score(
            resume_text=optimized_text,
            analyzed_jd=state["analyzed_jd"],
            job_id=f"{state['job_id']}-optimized",
            before_score=before_score,
        )
        return {
            "ats_score_optimized": score,
            "completed_nodes": state.get("completed_nodes", []) + ["score_optimized_ats"],
        }
    except Exception as exc:
        logger.error("score_optimized_ats_node failed: %s", exc)
        return {"error": f"Optimized ATS scoring failed: {str(exc)}"}


async def generate_email_node(state: AgentState) -> dict:
    """
    Node 7: Generate cold emails using all context accumulated so far.
    Reads:  parsed_resume, analyzed_jd, ats_score_optimized OR ats_score_original
    Writes: cold_emails
    """
    logger.info("Graph node: generate_email job_id=%s", state["job_id"])
    try:
        # Use optimized score if available, otherwise use original
        ats_result = (
                state.get("ats_score_optimized") or
                state.get("ats_score_original")
        )

        result = await cold_email_agent.generate(
            resume=state["parsed_resume"],
            analyzed_jd=state["analyzed_jd"],
            ats_result=ats_result,
            job_id=state["job_id"],
        )
        return {
            "cold_emails": result,
            "completed_nodes": state.get("completed_nodes", []) + ["generate_email"],
        }
    except Exception as exc:
        logger.error("generate_email_node failed: %s", exc)
        return {"error": f"Email generation failed: {str(exc)}"}