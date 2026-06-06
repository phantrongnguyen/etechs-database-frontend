from typing import Optional
from pydantic import BaseModel, Field, field_validator

class BalanceSnapshot(BaseModel):
    balance_before: int
    balance_after: int

    @field_validator('balance_before', 'balance_after')
    @classmethod
    def validate_amounts(cls, v):
        if v < 0:
            raise ValueError("Số dư ví trong snapshot không được âm")
        return v

class WalletTransactionMetaModel(BaseModel):
    tx_id: str = Field(..., description="Mã giao dịch - Khóa ngoại sang Postgres")
    note: Optional[str] = None
    triggered_by: str
    snapshot: BalanceSnapshot
    receipt_url: Optional[str] = None

    @field_validator('tx_id')
    @classmethod
    def clean_tx_id(cls, v):
        return v.strip()

    @field_validator('triggered_by')
    @classmethod
    def validate_enum_triggered(cls, v):
        allowed = ["system_auto", "admin", "user", "marketplace"]
        v_clean = v.strip().lower()
        if v_clean not in allowed:
            raise ValueError(f"triggered_by phải thuộc một trong các giá trị quy định: {allowed}")
        return v_clean