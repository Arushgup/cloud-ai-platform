import logging
import time
from app.agents.cold_email.schemas import ColdEmailResult
from app.agents.resume_parser.schemas import ParsedResume
from app.agents.jd_analyzer.schemas import AnalyzedJD
from app.agents.ats_scorer.schemas import ATSScoreResult
from app.core.config import settings

logger = logging.getLogger(__name__)


def _extract_key_achievement(resume: ParsedResume) -> str:
    """
    Pull the strongest quantified achievement from work experience.
    This becomes the hook in the cold email.
    """
    for exp in resume.work_experience:
        for resp in exp.responsibilities:
            # Look for responsibilities with numbers — those are achievements
            if any(char.isdigit() for char in resp):
                return resp
    # Fallback if no quantified achievements found
    if resume.work_experience:
        exp = resume.work_experience[0]
        return f"{exp.title} at {exp.company}"
    return "building scalable systems"


def _get_current_title(resume: ParsedResume) -> str:
    """Extract most recent job title."""
    if resume.work_experience:
        return resume.work_experience[0].title
    return resume.full_name or "Software Engineer"


def _get_matching_skills(
        resume: ParsedResume,
        analyzed_jd: AnalyzedJD,
) -> list[str]:
    """
    Find skills that appear in BOTH the resume and the JD required skills.
    These are the strongest talking points for the email.
    """
    resume_skills = set(
        s.lower() for s in
        resume.programming_languages + resume.frameworks_and_tools + resume.skills
    )
    matching = [
        skill for skill in analyzed_jd.required_skills
        if skill.lower() in resume_skills
    ]
    # Return top 4 matches
    return matching[:4] if matching else analyzed_jd.required_skills[:3]


class ColdEmailAgent:
    """
    Generates personalized cold emails using full context from previous phases.

    The key insight: this agent is the most context-rich in the system.
    It receives output from Phase 2 (who the candidate is),
    Phase 4 (what the job needs), and Phase 6 (how well they match).
    The more context, the more personalized the email.
    """

    async def generate(
            self,
            resume: ParsedResume,
            analyzed_jd: AnalyzedJD,
            ats_result: ATSScoreResult,
            job_id: str,
    ) -> ColdEmailResult:

        if settings.MOCK_LLM:
            logger.info(
                "MOCK MODE — returning fake cold email for job_id=%s", job_id
            )
            return self._get_mock_result(resume, analyzed_jd)

        from app.agents.cold_email.chain import get_cold_email_chain
        chain = get_cold_email_chain()
        start = time.monotonic()

        try:
            matching_skills = _get_matching_skills(resume, analyzed_jd)
            key_achievement = _extract_key_achievement(resume)
            current_title   = _get_current_title(resume)

            logger.info(
                "Generating cold email job_id=%s candidate=%s matching_skills=%d",
                job_id, resume.full_name, len(matching_skills),
            )

            result: ColdEmailResult = await chain.ainvoke({
                "full_name":          resume.full_name or "Candidate",
                "current_title":      current_title,
                "experience_years":   str(resume.total_experience_years or 0),
                "matching_skills":    ", ".join(matching_skills),
                "key_achievement":    key_achievement,
                "ats_score":          str(round(ats_result.overall_ats_score)),
                "job_title":          analyzed_jd.job_title,
                "company_name":       analyzed_jd.company_name or "your company",
                "required_skills":    ", ".join(analyzed_jd.required_skills[:5]),
                "key_responsibilities": "\n".join(
                    f"- {r}" for r in analyzed_jd.key_responsibilities[:3]
                ),
                "domain":             analyzed_jd.domain or "tech",
            })

            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.info(
                "Cold email generated job_id=%s duration_ms=%d",
                job_id, elapsed_ms,
            )
            return result

        except Exception as exc:
            elapsed_ms = round((time.monotonic() - start) * 1000)
            logger.error(
                "Cold email generation failed job_id=%s duration_ms=%d error=%s",
                job_id, elapsed_ms, str(exc),
                exc_info=True,
            )
            raise

    def _get_mock_result(
            self,
            resume: ParsedResume,
            analyzed_jd: AnalyzedJD,
    ) -> ColdEmailResult:
        from app.agents.cold_email.schemas import EmailVariant, EmailTone
        name = resume.full_name or "Candidate"
        title = analyzed_jd.job_title
        company = analyzed_jd.company_name or "your company"

        return ColdEmailResult(
            professional_variant=EmailVariant(
                tone=EmailTone.PROFESSIONAL,
                subject_line=f"Senior Data Engineer — Python/Kafka/Spark — {name}",
                body=(
                    f"Hi [Recruiter Name],\n\n"
                    f"I came across the {title} role at {company} and wanted to reach out directly.\n\n"
                    f"I have 5 years building real-time data pipelines at Flipkart, "
                    f"processing 10M+ events/day using the exact stack you require — "
                    f"Python, Apache Kafka, and Spark. Most recently I reduced data "
                    f"latency from 1 hour to 30 seconds on a critical pipeline.\n\n"
                    f"Would you have 15 minutes this week to discuss the role?\n\n"
                    f"Best regards,\n{name}"
                ),
                word_count=85,
            ),
            conversational_variant=EmailVariant(
                tone=EmailTone.CONVERSATIONAL,
                subject_line=f"Data Engineer with Kafka + Spark experience — quick intro",
                body=(
                    f"Hi [Recruiter Name],\n\n"
                    f"Saw the {title} opening at {company} — looks like a great fit.\n\n"
                    f"Quick background: I have been building real-time data pipelines "
                    f"for 5 years, most recently at Flipkart where I handled 10M events/day "
                    f"with Kafka and Spark. Cut latency by 96% on one project which I am "
                    f"proud of.\n\n"
                    f"Happy to jump on a quick call if useful. What does your calendar look like?\n\n"
                    f"Thanks,\n{name}"
                ),
                word_count=80,
            ),
            confident_variant=EmailVariant(
                tone=EmailTone.CONFIDENT,
                subject_line=f"5 years Kafka + Spark — built pipelines at 10M events/day",
                body=(
                    f"Hi [Recruiter Name],\n\n"
                    f"I build real-time data pipelines. At Flipkart I processed "
                    f"10M events/day with Kafka and Spark, and reduced latency from "
                    f"1 hour to 30 seconds.\n\n"
                    f"Your {title} role matches exactly what I do. "
                    f"Python, Kafka, Spark, AWS — I have been doing this for 5 years.\n\n"
                    f"15 minutes this week?\n\n"
                    f"{name}"
                ),
                word_count=65,
            ),
            key_hooks=[
                "10M events/day real-time pipeline experience",
                "96% latency reduction achievement",
                "Exact stack match: Python, Kafka, Spark, AWS",
            ],
            skills_highlighted=["Python", "Apache Kafka", "Apache Spark", "AWS"],
            personalization_tips=[
                "Replace [Recruiter Name] with the actual name — find it on LinkedIn",
                "Add one sentence about why this specific company interests you",
                "If you have a mutual connection, mention them in the first line",
                "Send Tuesday-Thursday 9-11am for highest open rates",
            ],
            follow_up_subject=f"Re: {title} — following up",
            follow_up_body=(
                f"Hi [Recruiter Name],\n\n"
                f"Just following up on my note from last week about the {title} role. "
                f"Still very interested — happy to connect if timing works better now.\n\n"
                f"{name}"
            ),
        )


cold_email_agent = ColdEmailAgent()