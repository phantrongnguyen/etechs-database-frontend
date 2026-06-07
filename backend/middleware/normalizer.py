from typing import Dict, Any, Optional
# Import trực tiếp các Model từ thư mục models vừa tách
from .models.wallet_asset_meta import WalletAssetMetaModel
from .models.wallet_transaction_meta import WalletTransactionMetaModel
from .models.student_profile_meta import StudentProfileMetaModel
from .models.education_meta import EducationMetaModel


def _trim_strings(data: Any) -> Any:
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, dict):
        return {k: _trim_strings(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_trim_strings(v) for v in data]
    return data


def normalize_data(collection_name: str, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Hàm điều phối tiếp nhận dữ liệu thô, gọi model tương ứng để chuẩn hóa.
    """
    try:
        cleaned = _trim_strings(raw_data)

        if collection_name == "wallet_asset_meta":
            validated_model = WalletAssetMetaModel(**cleaned)
        elif collection_name == "wallet_transaction_meta":
            validated_model = WalletTransactionMetaModel(**cleaned)
        elif collection_name == "student_profile_meta":
            validated_model = StudentProfileMetaModel(**cleaned)
        elif collection_name == "education_meta":
            validated_model = EducationMetaModel(**cleaned)
        else:
            print(f"⚠️ Collection '{collection_name}' chưa được cấu hình Model.")
            return None
        
        return validated_model.model_dump()
    
    except Exception as e:
        print(f"❌ LỖI CHUẨN HÓA trên [{collection_name}]: {e}")
        return None