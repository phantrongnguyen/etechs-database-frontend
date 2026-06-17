from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class IdentityMetaModel(BaseModel):
    indentity_id: str = Field(..., min_length=1, max_length=16)
    scan_urls: List[str] = Field(default_factory=list)
    ocr_extracted: Dict[str, Any] = Field(default_factory=dict)
    verification_status: Optional[str] = "pending"
    review_note: Optional[str] = None

    @field_validator("indentity_id")
    @classmethod
    def clean_indentity_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("indentity_id không được để trống")
        if len(v) > 16:
            raise ValueError("indentity_id không được vượt quá 16 ký tự")
        return v

    @field_validator("verification_status")
    @classmethod
    def validate_verification_status(cls, v):
        if v is None:
            return "pending"
        
        allowed = ["pending", "verified", "rejected"]
        v_clean = v.strip().lower()

        if v_clean not in allowed:
            raise ValueError(f"verification_status phải thuộc một trong các giá trị: {allowed}")

        return v_clean

    @field_validator("review_note")
    @classmethod
    def clean_review_note(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None
