from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class EducationMetaModel(BaseModel):
    education_id: str = Field(..., min_length=1, max_length=16)
    description: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)
    document_urls: List[str] = Field(default_factory=list)
    verification_status: str = "pending"
    verified_at: Optional[datetime] = None

    @field_validator("education_id")
    @classmethod
    def clean_education_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("education_id không được để trống")
        if len(v) > 16:
            raise ValueError("education_id không được vượt quá 16 ký tự")
        return v

    @field_validator("description")
    @classmethod
    def clean_description(cls, v):
        if v is None:
            return None
        v_clean = v.strip()
        return v_clean or None

    @field_validator("achievements")
    @classmethod
    def clean_achievements(cls, v):
        if v is None:
            return []
        return [ach.strip() for ach in v if ach and ach.strip()]

    @field_validator("document_urls")
    @classmethod
    def clean_document_urls(cls, v):
        if v is None:
            return []
        return [url.strip() for url in v if url and url.strip()]

    @field_validator("verification_status")
    @classmethod
    def validate_verification_status(cls, v):
        if v is None:
            return "pending"
        v_clean = v.strip().lower()
        allowed = ["pending", "verified", "rejected"]
        if v_clean not in allowed:
            raise ValueError(f"verification_status phải thuộc một trong các giá trị: {allowed}")
        return v_clean

    @field_validator("verified_at", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        if v in (None, ""):
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        return v
