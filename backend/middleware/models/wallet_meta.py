from typing import Optional
from pydantic import BaseModel, Field, field_validator 
from datetime import datetime 

class SpendingSummary(BaseModel):
    total_earned: Optional[int] = 0
    total_spent: Optional[int] = 0
    last_tx_at: Optional[datetime] = None
    
    @field_validator("total_earned", "total_spent")
    @classmethod
    def validate_amounts(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError("Tổng thu chi trong spending summary không được âm")
        return v

class AutoTopup(BaseModel):
    enabled: Optional[bool] = False
    threshold: Optional[int] = None
    amount: Optional[int] = None
    
    @field_validator("threshold", "amount")
    @classmethod
    def validate_topup_amounts(cls, v):
        if v is None:
            return None
        if v < 0:
            raise ValueError("Ngưỡng threshold và số tiền topup trong auto topup không được âm")
        return v 

class WalletMeta(BaseModel):
    wallets_id: str = Field(..., min_length=1, max_length=16)
    wallet_label: Optional[str] = "Ví chính"
    spending_summary: SpendingSummary = Field(default_factory=SpendingSummary)
    auto_topup: AutoTopup = Field(default_factory=AutoTopup)
    
    @field_validator("wallets_id")
    @classmethod 
    def clean_wallets_id(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("wallets_id không được để trống")
        if len(v) > 16:
            raise ValueError("wallets_id không được vượt quá 16 ký tự")
        return v 
    
    @field_validator("wallet_label")
    @classmethod
    def clean_wallet_label(cls, v):
        if v is None:
            return "Ví chính"
        v = v.strip()
        return v or "Ví chính"
    