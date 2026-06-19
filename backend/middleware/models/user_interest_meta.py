from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class UserInterestMetaModel(BaseModel):
    interest_id: str = Field(..., min_length=1, max_length=16)
    raw_input: Optional[str] = None
    ai_tags: List[str] = Field(default_factory=list)
    ai_processed_at: Optional[datetime] = None
    mapping_attempts: Optional[int] = 0

    @field_validator("interest_id")
    @classmethod
    def clean_interest_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("interest_id không được để trống")
        if len(v) > 16:
            raise ValueError("interest_id không được vượt quá 16 ký tự")
        return v

    @field_validator("raw_input")
    @classmethod
    def clean_raw_input(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("ai_tags")
    @classmethod
    def clean_ai_tags(cls, v):
        if not v:
            return []
        return [tag.strip() for tag in v if isinstance(tag, str) and tag.strip()]

    @field_validator("mapping_attempts")
    @classmethod
    def validate_mapping_attempts(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError("Số lần thử mapping không được là số âm")
        return v

    @field_validator("ai_processed_at", mode="before")
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
