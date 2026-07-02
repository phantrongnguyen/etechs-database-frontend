from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class PollSettings(BaseModel):
    allow_multiple_votes: bool = False
    show_results_before_close: bool = True
    anonymous_votes: bool = False


class PollStatsCache(BaseModel):
    total_votes: Optional[int] = 0
    cached_at: Optional[datetime] = None

    @field_validator("total_votes")
    @classmethod
    def validate_total_votes(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError("total_votes không được phép âm")
        return v

    @field_validator("cached_at", mode="before")
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


class PollMetaModel(BaseModel):
    poll_id: str = Field(..., min_length=1, max_length=16)
    description: Optional[str] = None
    settings: PollSettings = Field(default_factory=PollSettings)
    stats_cache: PollStatsCache = Field(default_factory=PollStatsCache)
    closed_at: Optional[datetime] = None

    @field_validator("poll_id")
    @classmethod
    def clean_poll_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("poll_id không được để trống")
        if len(v) > 16:
            raise ValueError("poll_id không được vượt quá 16 ký tự")
        return v

    @field_validator("description")
    @classmethod
    def clean_description(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("closed_at", mode="before")
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
