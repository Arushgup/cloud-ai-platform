from pydantic import BaseModel, Field
from enum import Enum


class EmailTone(str, Enum):
    PROFESSIONAL  = "professional"
    CONVERSATIONAL = "conversational"
    CONFIDENT     = "confident"


class EmailVariant(BaseModel):
    """
    A single email variant.
    We generate 3 variants per request — different tones, same content.
    Candidate picks the one that feels most natural to them.
    """
    tone:          EmailTone = Field(description="Tone of this variant")
    subject_line:  str       = Field(description="Email subject line")
    body:          str       = Field(description="Full email body")
    word_count:    int        = Field(description="Approximate word count")


class ColdEmailResult(BaseModel):
    """
    Complete cold email generation result.

    Three variants because different candidates have different communication styles.
    The hooks and talking points are extracted so the candidate can
    customize further if needed.
    """
    # Three variants — different tones
    professional_variant:    EmailVariant = Field(
        description="Formal, polished tone for traditional companies"
    )
    conversational_variant:  EmailVariant = Field(
        description="Warm, friendly tone for startups and tech companies"
    )
    confident_variant:       EmailVariant = Field(
        description="Direct, achievement-focused tone for competitive roles"
    )

    # Supporting content
    key_hooks:          list[str] = Field(
        default_factory=list,
        description="The strongest talking points used in the emails"
    )
    skills_highlighted: list[str] = Field(
        default_factory=list,
        description="Skills from resume that match the JD, used in emails"
    )
    personalization_tips: list[str] = Field(
        default_factory=list,
        description="Tips to further personalize before sending"
    )

    # Follow up
    follow_up_subject:  str = Field(
        description="Subject line for a follow-up email if no response in 1 week"
    )
    follow_up_body:     str = Field(
        description="Short follow-up email body"
    )