from pydantic import BaseModel, Field
from typing import Optional


class KeywordMatch(BaseModel):
    """A single keyword analysis result."""
    keyword:    str   = Field(description="The keyword from the JD")
    found:      bool  = Field(description="Whether it appears in the resume")
    frequency:  int   = Field(description="How many times it appears", default=0)
    importance: str   = Field(description="critical / important / minor")


class SectionScore(BaseModel):
    """ATS score breakdown for one resume section."""
    section:     str   = Field(description="summary / skills / experience / education")
    score:       float = Field(description="Section score 0-100")
    feedback:    str   = Field(description="Specific feedback for this section")
    fixes:       list[str] = Field(
        default_factory=list,
        description="Exact changes to improve this section's ATS score"
    )


class ATSScoreResult(BaseModel):
    """
    Complete ATS scoring result.

    This is the most honest feedback a candidate gets —
    a machine's view of their resume before any human sees it.
    Phase 7 cold email generator uses the score to personalize outreach.
    Phase 8 orchestrator uses it to decide if optimization is needed.
    """
    # Overall scores
    overall_ats_score:      float = Field(
        description="Overall ATS score 0-100. Below 70 = likely rejected by ATS."
    )
    keyword_match_score:    float = Field(
        description="How many JD keywords appear in resume. 0-100."
    )
    format_score:           float = Field(
        description="Resume format compatibility with ATS parsers. 0-100."
    )
    relevance_score:        float = Field(
        description="How relevant the experience is to this specific role. 0-100."
    )

    # Verdict
    will_pass_ats:          bool  = Field(
        description="True if score is high enough to pass automated screening"
    )
    verdict:                str   = Field(
        description="One sentence verdict on ATS compatibility"
    )

    # Keyword analysis
    keyword_matches:        list[KeywordMatch] = Field(
        default_factory=list,
        description="Analysis of each important JD keyword"
    )
    missing_critical_keywords: list[str] = Field(
        default_factory=list,
        description="Must-have keywords completely absent from resume"
    )
    matched_keywords:       list[str] = Field(
        default_factory=list,
        description="JD keywords successfully found in resume"
    )

    # Section breakdown
    section_scores:         list[SectionScore] = Field(
        default_factory=list,
        description="Score and feedback for each resume section"
    )

    # Action items
    critical_fixes:         list[str] = Field(
        default_factory=list,
        description="Must-fix issues that will cause ATS rejection"
    )
    recommended_fixes:      list[str] = Field(
        default_factory=list,
        description="Improvements that will significantly boost score"
    )

    # Comparison
    before_optimization_score: Optional[float] = Field(
        default=None,
        description="Score before Phase 5 optimization if available"
    )
    score_improvement:      Optional[float] = Field(
        default=None,
        description="How much the score improved after optimization"
    )