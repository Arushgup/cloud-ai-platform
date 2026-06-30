from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
import uuid


class ResumeUploadedEvent(BaseModel):
    """
    The Kafka event contract for resume-uploaded topic.
    The Spring Boot Application Service will produce this exact shape.
    This is the single source of truth for this event.
    """
    eventId: str      = Field(description="Unique event ID for deduplication")
    resumeId: str     = Field(description="Unique ID of the resume")
    userId: str       = Field(description="ID of the user who uploaded")
    userEmail: str    = Field(description="Email of the user")
    resumeText: str   = Field(description="Full extracted text of the resume")
    fileName: str     = Field(description="Original filename e.g. john_cv.pdf")
    uploadedAt: str   = Field(description="ISO timestamp of upload")