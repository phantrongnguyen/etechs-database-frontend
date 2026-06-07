from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, HttpUrl


class AssetSource(BaseModel):
    ref_type: Optional[str] = None
    ref_id: Optional[str] = None

    @field_validator("ref_type", "ref_id")
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None


class WalletAssetMetaModel(BaseModel):
    asset_id: str = Field(..., min_length=1, max_length=16)
    display_name: Optional[str] = None
    icon_url: Optional[str] = None
    description: Optional[str] = None
    earned_at: Optional[datetime] = None
    source: AssetSource = Field(default_factory=AssetSource)
    is_tradable: bool = False

    @field_validator("asset_id")
    @classmethod
    def clean_asset_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("asset_id không được để trống")
        if len(v) > 16:
            raise ValueError("asset_id không được vượt quá 16 ký tự")
        return v

    @field_validator("display_name", "icon_url", "description")
    @classmethod
    def clean_optional_strings(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("earned_at", mode="before")
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