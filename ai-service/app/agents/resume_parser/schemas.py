from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    ASSOCIATE   = "associate"
    BACHELOR    = "bachelor"
    MASTER      = "master"
    PHD         = "phd"
    BOOTCAMP    = "bootcamp"
    OTHER       = "other"


class WorkExperience(BaseModel):
    company:          str            = Field(description="Company name")
    title:            str            = Field(description="Job title")
    start_date:       Optional[str]  = Field(default=None, description="e.g. Jan 2021")
    end_date:         Optional[str]  = Field(default=None, description="e.g. Dec 2023 or Present")
    duration_months:  Optional[int]  = Field(default=None)
    responsibilities: list[str]      = Field(default_factory=list)
    technologies:     list[str]      = Field(default_factory=list)


class Education(BaseModel):
    institution:      str             = Field(description="University or school name")
    degree:           str             = Field(description="e.g. B.Sc. Computer Science")
    field_of_study:   Optional[str]   = Field(default=None)
    graduation_year:  Optional[int]   = Field(default=None)
    level:            EducationLevel  = Field(description="Highest qualification level")


class Project(BaseModel):
    name:         str        = Field(description="Project name")
    description:  str        = Field(description="One sentence summary")
    technologies: list[str]  = Field(default_factory=list)
    url:          Optional[str] = Field(default=None)


class ParsedResume(BaseModel):
    """
    The canonical parsed resume object.
    Every downstream agent reads from this — never from raw text.
    This schema is forward-compatible with all 8 phases.
    """
    # Contact info
    full_name:    Optional[str] = Field(default=None)
    email:        Optional[str] = Field(default=None)
    phone:        Optional[str] = Field(default=None)
    location:     Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)
    github_url:   Optional[str] = Field(default=None)

    # Summary
    summary:                  Optional[str]   = Field(default=None)
    total_experience_years:   Optional[float] = Field(default=None)

    # Skills — separated for precise matching in Phase 3 and Phase 6
    skills:                list[str] = Field(default_factory=list)
    programming_languages: list[str] = Field(default_factory=list)
    frameworks_and_tools:  list[str] = Field(default_factory=list)

    # Experience
    work_experience:  list[WorkExperience] = Field(default_factory=list)
    education:        list[Education]      = Field(default_factory=list)
    projects:         list[Project]        = Field(default_factory=list)
    certifications:   list[str]            = Field(default_factory=list)

    # Audit fields — useful for debugging and Phase 7 feedback loop
    raw_text_length: int = Field(default=0)