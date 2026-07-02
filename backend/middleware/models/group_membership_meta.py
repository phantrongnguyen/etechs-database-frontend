from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class GroupNotificationSettings(BaseModel):
    new_post: bool = True
    new_poll: bool = True
    mention: bool = True


class GroupMembershipMetaModel(BaseModel):
    group_id: str = Field(..., min_length=1, max_length=16)
    profile_id: str = Field(..., min_length=1, max_length=16)
    contribution_score: Optional[int] = 0
    badges_in_group: List[str] = Field(default_factory=list)
    last_active_at: Optional[datetime] = None
    notification_settings: GroupNotificationSettings = Field(default_factory=GroupNotificationSettings)

    @field_validator("group_id")
    @classmethod
    def clean_group_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("group_id không được để trống")
        if len(v) > 16:
            raise ValueError("group_id không được vượt quá 16 ký tự")
        return v

    @field_validator("profile_id")
    @classmethod
    def clean_profile_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("profile_id không được để trống")
        if len(v) > 16:
            raise ValueError("profile_id không được vượt quá 16 ký tự")
        return v

    @field_validator("contribution_score")
    @classmethod
    def validate_contribution_score(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError("contribution_score không được phép âm")
        return v

    @field_validator("badges_in_group")
    @classmethod
    def clean_badges(cls, v):
        if not v:
            return []
        return [badge.strip() for badge in v if isinstance(badge, str) and badge.strip()]

    @field_validator("last_active_at", mode="before")
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
