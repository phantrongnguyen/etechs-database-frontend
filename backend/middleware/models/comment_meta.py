from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class CommentMediaItem(BaseModel):
    type: Optional[str] = None
    url: Optional[str] = None

    @field_validator("type", "url")
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None


class CommentStatsCache(BaseModel):
    like_count: Optional[int] = 0
    reply_count: Optional[int] = 0
    cached_at: Optional[datetime] = None

    @field_validator("like_count", "reply_count")
    @classmethod
    def validate_non_negative(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError("Chỉ số stats_cache không được âm")
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


class CommentEditHistoryItem(BaseModel):
    content: Optional[str] = None
    edited_at: Optional[datetime] = None

    @field_validator("content")
    @classmethod
    def clean_content(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("edited_at", mode="before")
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


class CommentModeration(BaseModel):
    status: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return None
        v_clean = v.strip().lower()
        allowed = ["approved", "hidden", "removed"]
        if v_clean not in allowed:
            raise ValueError(f"status phải thuộc một trong các giá trị: {allowed}")
        return v_clean

    @field_validator("reviewed_by")
    @classmethod
    def clean_reviewed_by(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("reviewed_at", mode="before")
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


class CommentMetaModel(BaseModel):
    comment_id: str = Field(..., min_length=1, max_length=16)
    rich_content: Optional[str] = None
    media: List[CommentMediaItem] = Field(default_factory=list)
    stats_cache: CommentStatsCache = Field(default_factory=CommentStatsCache)
    edit_history: List[CommentEditHistoryItem] = Field(default_factory=list)
    moderation: CommentModeration = Field(default_factory=CommentModeration)

    @field_validator("comment_id")
    @classmethod
    def clean_comment_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("comment_id không được để trống")
        if len(v) > 16:
            raise ValueError("comment_id không được vượt quá 16 ký tự")
        return v

    @field_validator("rich_content")
    @classmethod
    def clean_rich_content(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("edit_history")
    @classmethod
    def limit_edit_history(cls, v):
        if not v:
            return []
        # Giữ tối đa 10 bản chỉnh sửa gần nhất
        return v[-10:]
