from typing import Optional
from pydantic import BaseModel, Field, field_validator


class BalanceSnapshot(BaseModel):
    balance_before: Optional[int] = None
    balance_after: Optional[int] = None

    @field_validator("balance_before", "balance_after")
    @classmethod
    def validate_amounts(cls, v):
        if v is None:
            return None
        if v < 0:
            raise ValueError("Số dư ví trong snapshot không được âm")
        return v


class WalletTransactionMetaModel(BaseModel):
    tx_id: str = Field(..., min_length=1, max_length=16)
    note: Optional[str] = None
    triggered_by: Optional[str] = None
    snapshot: BalanceSnapshot = Field(default_factory=BalanceSnapshot)
    receipt_url: Optional[str] = None

    @field_validator("tx_id")
    @classmethod
    def clean_tx_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("tx_id không được để trống")
        if len(v) > 16:
            raise ValueError("tx_id không được vượt quá 16 ký tự")
        return v

    @field_validator("note", "receipt_url")
    @classmethod
    def clean_optional_strings(cls, v):
        if v is None:
            return None
        v = v.strip()
        return v or None

    @field_validator("triggered_by")
    @classmethod
    def validate_enum_triggered(cls, v):
        if v is None:
            return None

        allowed = ["system_auto", "admin", "user", "marketplace"]
        v_clean = v.strip().lower()

        if v_clean not in allowed:
            raise ValueError(f"triggered_by phải thuộc một trong các giá trị: {allowed}")

        return v_clean