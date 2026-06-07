from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class DisplayPreferences(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

    @field_validator("theme", "language", "timezone")
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        v_clean = v.strip()
        return v_clean or None


class PrivacySettings(BaseModel):
    show_avatar: Optional[str] = "public"
    show_bio: Optional[str] = "public"
    show_interests: Optional[str] = "public"

    @field_validator("show_avatar", "show_bio", "show_interests")
    @classmethod
    def validate_privacy(cls, v):
        if v is None:
            return "public"
        v_clean = v.strip().lower()
        allowed = ["public", "friends_only", "private"]
        if v_clean not in allowed:
            raise ValueError(f"Quyền riêng tư phải thuộc các giá trị: {allowed}")
        return v_clean


class Onboarding(BaseModel):
    is_completed: bool = False
    steps_done: List[str] = Field(default_factory=list)
    last_step_at: Optional[datetime] = None

    @field_validator("steps_done")
    @classmethod
    def clean_steps_done(cls, v):
        if v is None:
            return []
        return [step.strip() for step in v if step and step.strip()]

    @field_validator("last_step_at", mode="before")
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


class StudentProfileMetaModel(BaseModel):
    profile_id: str = Field(..., min_length=1, max_length=16)
    display_preferences: DisplayPreferences = Field(default_factory=DisplayPreferences)
    privacy_settings: PrivacySettings = Field(default_factory=PrivacySettings)
    onboarding: Onboarding = Field(default_factory=Onboarding)
    tags: List[str] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    ai_summary_at: Optional[datetime] = None

    @field_validator("profile_id")
    @classmethod
    def clean_profile_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("profile_id không được để trống")
        if len(v) > 16:
            raise ValueError("profile_id không được vượt quá 16 ký tự")
        return v

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v):
        if v is None:
            return []
        return [tag.strip() for tag in v if tag and tag.strip()]

    @field_validator("ai_summary")
    @classmethod
    def clean_summary(cls, v):
        if v is None:
            return None
        v_clean = v.strip()
        return v_clean or None

    @field_validator("ai_summary_at", mode="before")
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
