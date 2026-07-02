from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class MessageMediaItem(BaseModel):
    type: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = None

    @field_validator("type", "url", "name")
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None


class MessageReadByItem(BaseModel):
    profile_id: Optional[str] = None
    read_at: Optional[datetime] = None

    @field_validator("profile_id")
    @classmethod
    def clean_profile_id(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("read_at", mode="before")
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


class MessageReactionItem(BaseModel):
    profile_id: Optional[str] = None
    emoji: Optional[str] = None

    @field_validator("profile_id", "emoji")
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None


class MessageMetaModel(BaseModel):
    message_id: str = Field(..., min_length=1, max_length=16)
    rich_content: Optional[str] = None
    media: List[MessageMediaItem] = Field(default_factory=list)
    read_by: List[MessageReadByItem] = Field(default_factory=list)
    reactions: List[MessageReactionItem] = Field(default_factory=list)
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None

    @field_validator("message_id")
    @classmethod
    def clean_message_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("message_id không được để trống")
        if len(v) > 16:
            raise ValueError("message_id không được vượt quá 16 ký tự")
        return v

    @field_validator("rich_content")
    @classmethod
    def clean_rich_content(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("deleted_at", mode="before")
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
