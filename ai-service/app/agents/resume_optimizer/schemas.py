from pydantic import BaseModel, Field
from typing import Optional


class SkillGap(BaseModel):
    """A single skill gap between resume and job requirements."""
    skill:       str  = Field(description="The missing or weak skill")
    priority:    str  = Field(description="critical / important / nice-to-have")
    suggestion:  str  = Field(description="Specific advice on how to address this gap")


class OptimizationSuggestion(BaseModel):
    """A single improvement suggestion for the resume."""
    section:     str  = Field(description="Which section: summary, experience, skills, education")
    issue:       str  = Field(description="What is weak or missing")
    suggestion:  str  = Field(description="Exactly what to change or add")
    impact:      str  = Field(description="high / medium / low impact on ATS and recruiter")


class ResumeOptimizationResult(BaseModel):
    """
    Complete optimization result.
    Contains gap analysis, suggestions, and fully rewritten resume.
    All downstream agents — ATS Scorer, Cold Email Generator — use this.
    """
    # Match analysis
    overall_match_score:    float          = Field(
        description="How well the resume matches the JD. 0-100."
    )
    match_summary:          str            = Field(
        description="2 sentence summary of how well the candidate fits"
    )

    # Gap analysis
    skill_gaps:             list[SkillGap] = Field(
        default_factory=list,
        description="Skills required by JD but missing or weak in resume"
    )
    strong_matches:         list[str]      = Field(
        default_factory=list,
        description="Skills and experiences that strongly match the JD"
    )

    # Improvement suggestions
    suggestions:            list[OptimizationSuggestion] = Field(
        default_factory=list,
        description="Specific actionable improvements ordered by impact"
    )

    # Rewritten resume sections
    optimized_summary:      str            = Field(
        description="Rewritten professional summary tailored to this job"
    )
    optimized_skills:       list[str]      = Field(
        default_factory=list,
        description="Reordered and optimized skills list for this job"
    )
    optimized_experience:   list[str]      = Field(
        default_factory=list,
        description="Rewritten bullet points for each work experience"
    )

    # Keywords
    ats_keywords_added:     list[str]      = Field(
        default_factory=list,
        description="Keywords from JD injected into the optimized resume"
    )
    keywords_to_add:        list[str]      = Field(
        default_factory=list,
        description="Important JD keywords still missing — candidate should address"
    )