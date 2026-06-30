from pydantic import BaseModel, Field
from typing import Optional


class JobMatchRequest(BaseModel):
    """
    Input to the job matcher.
    A job description is all we need — the vector search does the rest.
    """
    job_id:          str  = Field(description="Unique ID for this job")
    job_title:       str  = Field(description="e.g. Senior Backend Engineer")
    job_description: str  = Field(description="Full job description text")
    n_results:       int  = Field(default=5, ge=1, le=20, description="How many resumes to return")


class ResumeMatch(BaseModel):
    """
    A single resume match result.
    distance = how similar the resume is to the job.
    0.0 = perfect match, 1.0 = completely unrelated.
    """
    resume_id:        str            = Field(description="ID of the matched resume")
    full_name:        str            = Field(description="Candidate name")
    user_email:       str            = Field(description="Candidate email")
    experience_years: float          = Field(description="Years of experience")
    top_skills:       str            = Field(description="Comma separated top skills")
    match_score:      float          = Field(description="Match score 0-100. Higher is better.")
    distance:         float          = Field(description="Raw cosine distance. Lower is better.")


class JobMatchResponse(BaseModel):
    """
    Full response from the job matcher.
    """
    job_id:       str              = Field(description="The job that was matched against")
    job_title:    str
    total_found:  int              = Field(description="How many resumes were searched")
    matches:      list[ResumeMatch] = Field(description="Ranked list of matching resumes")