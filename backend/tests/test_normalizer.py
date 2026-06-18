import pytest
from datetime import datetime
from middleware.normalizer import normalize_data


# =====================================================================
# THỬ NGHIỆM BẢNG 4: wallet_meta
# =====================================================================

def test_wallet_meta_valid():
    """Kiểm thử dữ liệu hợp lệ: Phải chuẩn hóa thành công và làm sạch chuỗi"""
    raw_data = {
        "wallets_id": "   WALLET_123   ",  # Khoảng trắng thừa
        "wallet_label": "  Ví phụ  ",
        "spending_summary": {
            "total_earned": 100000,
            "total_spent": 50000,
            "last_tx_at": "2026-06-06T17:00:00Z"
        },
        "auto_topup": {
            "enabled": True,
            "threshold": 10000,
            "amount": 50000
        }
    }
    
    cleaned = normalize_data("wallet_meta", raw_data)
    
    assert cleaned is not None
    assert cleaned["wallets_id"] == "WALLET_123"          # Đã trim khoảng trắng
    assert cleaned["wallet_label"] == "Ví phụ"           # Đã trim khoảng trắng
    assert isinstance(cleaned["spending_summary"]["last_tx_at"], datetime)  # Đã ép sang kiểu ngày tháng
    assert cleaned["auto_topup"]["enabled"] is True      # Đã giữ nguyên kiểu Boolean

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
# THỬ NGHIỆM BẢNG 3: identity_meta
# =====================================================================

def test_identity_meta_valid():
    """Kiểm thử dữ liệu hợp lệ cho identity_meta: Trim chuỗi, gán mặc định"""
    raw_data = {
        "indentity_id": "   ID_DOC_777   ",
        "scan_urls": [
            "  https://storage.cloud.com/docs/front.jpg  ",
            "https://storage.cloud.com/docs/back.jpg"
        ],
        "ocr_extracted": {
            "full_name": "Nguyen Van A",
            "dob": "1999-01-01"
        },
        "verification_status": "  VERIFIED  ",
        "review_note": "   Giấy tờ hợp lệ   "
    }

    cleaned = normalize_data("identity_meta", raw_data)

    assert cleaned is not None
    assert cleaned["indentity_id"] == "ID_DOC_777"
    assert cleaned["scan_urls"][0] == "https://storage.cloud.com/docs/front.jpg"
    assert cleaned["ocr_extracted"]["full_name"] == "Nguyen Van A"
    assert cleaned["verification_status"] == "verified"
    assert cleaned["review_note"] == "Giấy tờ hợp lệ"


def test_identity_meta_defaults():
    """Kiểm thử giá trị mặc định của identity_meta khi không truyền trường tùy chọn"""
    raw_data = {
        "indentity_id": "ID_DOC_888"
    }

    cleaned = normalize_data("identity_meta", raw_data)

    assert cleaned is not None
    assert cleaned["indentity_id"] == "ID_DOC_888"
    assert cleaned["scan_urls"] == []
    assert cleaned["ocr_extracted"] == {}
    assert cleaned["verification_status"] == "pending"
    assert cleaned["review_note"] is None


def test_identity_meta_invalid_status():
    """Kiểm thử vi phạm enum của verification_status"""
    raw_data = {
        "indentity_id": "ID_DOC_888",
        "verification_status": "approved"  # Không nằm trong: pending, verified, rejected
    }

    cleaned = normalize_data("identity_meta", raw_data)
    assert cleaned is None


def test_identity_meta_missing_required():
    """Kiểm thử thiếu trường indentity_id"""
    raw_data = {
        "verification_status": "verified"
    }

    cleaned = normalize_data("identity_meta", raw_data)
    assert cleaned is None


# =====================================================================
# THỬ NGHIỆM BẢNG 2: education_meta
# =====================================================================

def test_education_meta_valid():
    """Kiểm thử dữ liệu hợp lệ cho education_meta: Trim chuỗi, làm sạch mảng và ép kiểu ngày tháng"""
    raw_data = {
        "education_id": "   EDU_MATH_123   ",
        "description": "  Học sinh giỏi Toán  ",
        "achievements": [
            "  Giải nhất  ",
            "   ",  # Sẽ bị loại bỏ do rỗng
            "Huy chương Vàng"
        ],
        "document_urls": [
            "https://storage.cloud.com/1.pdf",
            "  "  # Sẽ bị loại bỏ do rỗng
        ],
        "verification_status": "  VERIFIED  ",
        "verified_at": "2026-06-18T12:00:00Z"
    }

    cleaned = normalize_data("education_meta", raw_data)

    assert cleaned is not None
    assert cleaned["education_id"] == "EDU_MATH_123"
    assert cleaned["description"] == "Học sinh giỏi Toán"
    assert cleaned["achievements"] == ["Giải nhất", "Huy chương Vàng"]
    assert cleaned["document_urls"] == ["https://storage.cloud.com/1.pdf"]
    assert cleaned["verification_status"] == "verified"
    assert isinstance(cleaned["verified_at"], datetime)


def test_education_meta_defaults():
    """Kiểm thử giá trị mặc định cho education_meta"""
    raw_data = {
        "education_id": "EDU_111"
    }

    cleaned = normalize_data("education_meta", raw_data)

    assert cleaned is not None
    assert cleaned["education_id"] == "EDU_111"
    assert cleaned["description"] is None
    assert cleaned["achievements"] == []
    assert cleaned["document_urls"] == []
    assert cleaned["verification_status"] == "pending"
    assert cleaned["verified_at"] is None


def test_education_meta_invalid_enum():
    """Kiểm thử vi phạm enum cho verification_status"""
    raw_data = {
        "education_id": "EDU_111",
        "verification_status": "approved"  # Không hợp lệ, phải thuộc: pending, verified, rejected
    }

    cleaned = normalize_data("education_meta", raw_data)
    assert cleaned is None


def test_education_meta_missing_required():
    """Kiểm thử thiếu trường bắt buộc education_id"""
    raw_data = {
        "description": "Học sinh giỏi",
        "verification_status": "verified"
    }

    cleaned = normalize_data("education_meta", raw_data)
    assert cleaned is None
