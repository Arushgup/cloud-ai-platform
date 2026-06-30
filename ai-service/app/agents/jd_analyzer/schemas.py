from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SeniorityLevel(str, Enum):
    INTERN     = "intern"
    JUNIOR     = "junior"
    MID        = "mid"
    SENIOR     = "senior"
    LEAD       = "lead"
    PRINCIPAL  = "principal"
    MANAGER    = "manager"


class EmploymentType(str, Enum):
    FULL_TIME  = "full_time"
    PART_TIME  = "part_time"
    CONTRACT   = "contract"
    FREELANCE  = "freelance"


class AnalyzedJD(BaseModel):
    """
    Structured analysis of a job description.
    This is the canonical JD object consumed by all downstream agents.

    Phase 3 uses it for better semantic matching.
    Phase 5 uses it to optimize resumes against exact requirements.
    Phase 6 uses it to score ATS compatibility.
    Phase 7 uses it to generate targeted cold emails.
    """
    # Role basics
    job_title:          str                    = Field(description="Cleaned job title")
    company_name:       Optional[str]          = Field(default=None)
    seniority_level:    SeniorityLevel         = Field(description="Detected seniority")
    employment_type:    EmploymentType         = Field(default=EmploymentType.FULL_TIME)
    location:           Optional[str]          = Field(default=None, description="Location or Remote")

    # Experience
    min_experience_years: Optional[float]      = Field(default=None, description="Minimum years required")
    max_experience_years: Optional[float]      = Field(default=None, description="Maximum years if mentioned")

    # Skills — split by priority
    required_skills:      list[str]            = Field(
        default_factory=list,
        description="Must-have skills explicitly required"
    )
    preferred_skills:     list[str]            = Field(
        default_factory=list,
        description="Nice-to-have skills mentioned"
    )
    programming_languages: list[str]           = Field(default_factory=list)
    frameworks_and_tools:  list[str]           = Field(default_factory=list)
    cloud_platforms:       list[str]           = Field(default_factory=list)

    # Role details
    key_responsibilities:  list[str]           = Field(
        default_factory=list,
        description="Main responsibilities extracted from JD"
    )
    domain:               Optional[str]        = Field(
        default=None,
        description="Industry domain e.g. fintech, ecommerce, healthcare"
    )

    # Insights
    summary:              str                  = Field(
        description="2 sentence summary of what this role is really about"
    )
    red_flags:            list[str]            = Field(
        default_factory=list,
        description="Unusual or concerning requirements e.g. 10 years React when React is 11 years old"
    )

    # Audit
    raw_jd_length:        int                  = Field(default=0)