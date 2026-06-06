from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AssetSource(BaseModel):
    ref_type: str = Field(..., description="Loại nguồn phát sinh: assessment, event,...")
    ref_id: str = Field(..., description="Mã tham chiếu kết nối hệ thống")

    @field_validator('ref_type', 'ref_id')
    @classmethod
    def clean_strings(cls, v):
        return v.strip() if isinstance(v, str) else v

class WalletAssetMetaModel(BaseModel):
    asset_id: str = Field(..., description="Mã tài sản số - Khóa ngoại sang Postgres")
    display_name: str
    icon_url: str
    description: Optional[str] = None
    earned_at: datetime
    source: AssetSource
    is_tradable: bool = False

    @field_validator('asset_id', 'display_name')
    @classmethod
    def clean_required_strings(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Trường này bắt buộc, không được để trống")
        return v

    @field_validator('earned_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        return v