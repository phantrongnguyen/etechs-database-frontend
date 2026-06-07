import pytest
from datetime import datetime
from middleware.normalizer import normalize_data

# =====================================================================
# THỬ NGHIỆM BẢNG 5: wallet_asset_meta
# =====================================================================

def test_wallet_asset_meta_valid():
    """Kiểm thử dữ liệu hợp lệ: Phải chuẩn hóa thành công và làm sạch chuỗi"""
    raw_data = {
        "asset_id": "    ASSET_MATH_101   ",  # Khoảng trắng thừa
        "display_name": "  Huy hiệu Toán Học  ",
        "icon_url": "https://storage.cloud.com/icons/math.png",
        "description": "Đạt điểm tối đa",
        "earned_at": "2026-06-06T17:00:00Z",  # Chuỗi ngày tháng ISO
        "source": {
            "ref_type": "   assessment   ",
            "ref_id": "KT_01"
        },
        "is_tradable": "True"  # Chuỗi Boolean
    }
    
    cleaned = normalize_data("wallet_asset_meta", raw_data)
    
    assert cleaned is not None
    assert cleaned["asset_id"] == "ASSET_MATH_101"        # Đã trim khoảng trắng
    assert cleaned["display_name"] == "Huy hiệu Toán Học"  # Đã trim khoảng trắng
    assert isinstance(cleaned["earned_at"], datetime)     # Đã ép sang kiểu ngày tháng
    assert cleaned["source"]["ref_type"] == "assessment"  # Đã trim object con
    assert cleaned["is_tradable"] is True                 # Đã ép về kiểu Boolean chuẩn


def test_wallet_asset_meta_missing_required():
    """Kiểm thử dữ liệu thiếu trường bắt buộc: Hệ thống phải phát hiện và trả về None"""
    raw_bad_data = {
        "display_name": "Huy hiệu thiếu ID",
        "earned_at": "2026-06-06T17:00:00Z",
        "source": {"ref_type": "event", "ref_id": "EV_01"}
    }
    
    cleaned = normalize_data("wallet_asset_meta", raw_bad_data)
    assert cleaned is None  # Phải chặn lại vì thiếu 'asset_id' và 'icon_url'


# =====================================================================
# THỬ NGHIỆM BẢNG 6: wallet_transaction_meta
# =====================================================================

def test_wallet_transaction_meta_valid():
    """Kiểm thử giao dịch hợp lệ: Ép kiểu dữ liệu số và kiểm tra enum"""
    raw_data = {
        "tx_id": "TX_99999",
        "note": "Học sinh nạp tiền",
        "triggered_by": "   USER   ",  # Chữ in hoa và khoảng trắng
        "snapshot": {
            "balance_before": "50000",   # Ép từ chuỗi số sang int
            "balance_after": 250000
        },
        "receipt_url": "https://receipts.com/1.pdf"
    }
    
    cleaned = normalize_data("wallet_transaction_meta", raw_data)
    
    assert cleaned is not None
    assert cleaned["triggered_by"] == "user"  # Tự động đưa về chữ thường và cắt khoảng trắng
    assert cleaned["snapshot"]["balance_before"] == 50000  # Đã chuyển thành kiểu số nguyên int
    assert isinstance(cleaned["snapshot"]["balance_before"], int)


def test_wallet_transaction_meta_invalid_enum():
    """Kiểm thử vi phạm luật giá trị giới hạn (Enum): triggered_by không hợp lệ"""
    raw_bad_enum = {
        "tx_id": "TX_ERR_01",
        "triggered_by": "giao_vien",  # Không thuộc list: system_auto, admin, user, marketplace
        "snapshot": {
            "balance_before": 100,
            "balance_after": 200
        }
    }
    
    cleaned = normalize_data("wallet_transaction_meta", raw_bad_enum)
    assert cleaned is None  # Phải từ chối xử lý và trả về None


def test_wallet_transaction_meta_negative_balance():
    """Kiểm thử ràng buộc logic nghiệp vụ: Số dư tài khoản không được là số âm"""
    raw_negative_data = {
        "tx_id": "TX_ERR_02",
        "triggered_by": "admin",
        "snapshot": {
            "balance_before": -5000,  # Số âm vô lý
            "balance_after": 20000
        }
    }
    
    cleaned = normalize_data("wallet_transaction_meta", raw_negative_data)
    assert cleaned is None  # Phải chặn đứng do vi phạm điều kiện số tiền >= 0


# =====================================================================
# THỬ NGHIỆM BẢNG: student_profile_meta
# =====================================================================

def test_student_profile_meta_valid():
    """Kiểm thử thông tin profile hợp lệ: Trimming chuỗi, ép kiểu boolean, parse ngày tháng"""
    raw_data = {
        "profile_id": "   PROFILE_KT_001   ",
        "display_preferences": {
            "theme": "   dark   ",
            "language": "vi",
            "timezone": "Asia/Ho_Chi_Minh"
        },
        "privacy_settings": {
            "show_avatar": "public",
            "show_bio": "   friends_only   ",
            "show_interests": "private"
        },
        "onboarding": {
            "is_completed": "True",
            "steps_done": ["  step_1  ", "step_2"],
            "last_step_at": "2026-06-07T12:00:00Z"
        },
        "tags": ["   active   ", "premium"],
        "ai_summary": "   Học sinh chăm chỉ.   ",
        "ai_summary_at": "2026-06-07T18:00:00Z"
    }

    cleaned = normalize_data("student_profile_meta", raw_data)

    assert cleaned is not None
    assert cleaned["profile_id"] == "PROFILE_KT_001"
    assert cleaned["display_preferences"]["theme"] == "dark"
    assert cleaned["privacy_settings"]["show_bio"] == "friends_only"
    assert cleaned["onboarding"]["is_completed"] is True
    assert cleaned["onboarding"]["steps_done"] == ["step_1", "step_2"]
    assert isinstance(cleaned["onboarding"]["last_step_at"], datetime)
    assert cleaned["tags"] == ["active", "premium"]
    assert cleaned["ai_summary"] == "Học sinh chăm chỉ."
    assert isinstance(cleaned["ai_summary_at"], datetime)


def test_student_profile_meta_invalid_privacy_enum():
    """Kiểm thử giá trị enum privacy_settings sai quy định"""
    raw_bad_data = {
        "profile_id": "PROFILE_KT_001",
        "privacy_settings": {
            "show_avatar": "everybody"  # Không hợp lệ (chỉ chấp nhận public, friends_only, private)
        }
    }

    cleaned = normalize_data("student_profile_meta", raw_bad_data)
    assert cleaned is None


def test_student_profile_meta_missing_required():
    """Kiểm thử thiếu profile_id bắt buộc"""
    raw_bad_data = {
        "display_preferences": {"theme": "dark"}
    }

    cleaned = normalize_data("student_profile_meta", raw_bad_data)
    assert cleaned is None


# =====================================================================
# THỬ NGHIỆM BẢNG: education_meta
# =====================================================================

def test_education_meta_valid():
    """Kiểm thử thông tin học vấn hợp lệ: Trimming, chuẩn hóa enum, parse ngày tháng"""
    raw_data = {
        "education_id": "   EDU_KT_999   ",
        "description": "   Trường THPT Chuyên Lê Hồng Phong   ",
        "achievements": ["   Giải Nhì   ", "Học sinh giỏi"],
        "document_urls": ["https://storage.etechs.vn/diploma/edu_kt_999.pdf"],
        "verification_status": "   VERIFIED   ",  # In hoa và có khoảng trắng
        "verified_at": "2026-06-08T00:00:00Z"
    }

    cleaned = normalize_data("education_meta", raw_data)

    assert cleaned is not None
    assert cleaned["education_id"] == "EDU_KT_999"
    assert cleaned["description"] == "Trường THPT Chuyên Lê Hồng Phong"
    assert cleaned["achievements"] == ["Giải Nhì", "Học sinh giỏi"]
    assert cleaned["verification_status"] == "verified"  # Tự động về chữ thường
    assert isinstance(cleaned["verified_at"], datetime)


def test_education_meta_invalid_status_enum():
    """Kiểm thử verification_status sai giá trị enum quy định"""
    raw_bad_data = {
        "education_id": "EDU_KT_999",
        "verification_status": "approved"  # Sai enum (chỉ chấp nhận pending, verified, rejected)
    }

    cleaned = normalize_data("education_meta", raw_bad_data)
    assert cleaned is None


def test_education_meta_missing_required():
    """Kiểm thử thiếu education_id bắt buộc"""
    raw_bad_data = {
        "verification_status": "pending"
    }

    cleaned = normalize_data("education_meta", raw_bad_data)
    assert cleaned is None