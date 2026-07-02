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


# =====================================================================
# THỬ NGHIỆM BẢNG 1: student_profile_meta
# =====================================================================

def test_student_profile_meta_valid():
    """Kiểm thử dữ liệu hợp lệ cho student_profile_meta: Trim chuỗi, làm sạch mảng và ép kiểu ngày tháng"""
    raw_data = {
        "profile_id": "   PROF_STUDENT_99   ",
        "display_preferences": {
            "theme": "  dark  ",
            "language": " vi ",
            "timezone": " Asia/Ho_Chi_Minh "
        },
        "privacy_settings": {
            "show_avatar": "  FRIENDS_ONLY  ",
            "show_bio": "public",
            "show_interests": "private"
        },
        "onboarding": {
            "is_completed": "True",  # Ép boolean
            "steps_done": [
                "  intro  ",
                "   ",  # Sẽ bị loại bỏ do rỗng
                "upload_avatar"
            ],
            "last_step_at": "2026-06-19T10:00:00Z"
        },
        "tags": [
            "  active  ",
            "   ",  # Sẽ bị loại bỏ do rỗng
            "premium"
        ],
        "ai_summary": "  Học sinh xuất sắc  ",
        "ai_summary_at": "2026-06-19 10:00:00"
    }

    cleaned = normalize_data("student_profile_meta", raw_data)

    assert cleaned is not None
    assert cleaned["profile_id"] == "PROF_STUDENT_99"
    assert cleaned["display_preferences"]["theme"] == "dark"
    assert cleaned["display_preferences"]["language"] == "vi"
    assert cleaned["display_preferences"]["timezone"] == "Asia/Ho_Chi_Minh"
    assert cleaned["privacy_settings"]["show_avatar"] == "friends_only"
    assert cleaned["privacy_settings"]["show_bio"] == "public"
    assert cleaned["privacy_settings"]["show_interests"] == "private"
    assert cleaned["onboarding"]["is_completed"] is True
    assert cleaned["onboarding"]["steps_done"] == ["intro", "upload_avatar"]
    assert isinstance(cleaned["onboarding"]["last_step_at"], datetime)
    assert cleaned["tags"] == ["active", "premium"]
    assert cleaned["ai_summary"] == "Học sinh xuất sắc"
    assert isinstance(cleaned["ai_summary_at"], datetime)


def test_student_profile_meta_defaults():
    """Kiểm thử giá trị mặc định cho student_profile_meta"""
    raw_data = {
        "profile_id": "PROF_111"
    }

    cleaned = normalize_data("student_profile_meta", raw_data)

    assert cleaned is not None
    assert cleaned["profile_id"] == "PROF_111"
    assert cleaned["display_preferences"]["theme"] is None
    assert cleaned["privacy_settings"]["show_avatar"] == "public"
    assert cleaned["privacy_settings"]["show_bio"] == "public"
    assert cleaned["privacy_settings"]["show_interests"] == "public"
    assert cleaned["onboarding"]["is_completed"] is False
    assert cleaned["onboarding"]["steps_done"] == []
    assert cleaned["onboarding"]["last_step_at"] is None
    assert cleaned["tags"] == []
    assert cleaned["ai_summary"] is None
    assert cleaned["ai_summary_at"] is None


def test_student_profile_meta_invalid_privacy():
    """Kiểm thử vi phạm enum cho privacy_settings"""
    raw_data = {
        "profile_id": "PROF_111",
        "privacy_settings": {
            "show_avatar": "only_me"  # Không hợp lệ, phải thuộc: public, friends_only, private
        }
    }

    cleaned = normalize_data("student_profile_meta", raw_data)
    assert cleaned is None


def test_student_profile_meta_missing_required():
    """Kiểm thử thiếu trường bắt buộc profile_id"""
    raw_data = {
        "display_preferences": {
            "theme": "dark"
        }
    }

    cleaned = normalize_data("student_profile_meta", raw_data)
    assert cleaned is None


# =====================================================================
# THỬ NGHIỆM BẢNG 7: user_interest_meta
# =====================================================================

def test_user_interest_meta_valid():
    """Kiểm thử dữ liệu hợp lệ cho user_interest_meta: Trim chuỗi, dọn dẹp mảng và ép kiểu số, ngày tháng"""
    raw_data = {
        "interest_id": "   INT_READING_88   ",
        "raw_input": "  Tôi thích đọc sách  ",
        "ai_tags": [
            "  đọc sách  ",
            "   ",  # Sẽ bị loại bỏ do rỗng
            "giải trí"
        ],
        "ai_processed_at": "2026-06-19 11:00:00",
        "mapping_attempts": "3"  # Sẽ ép sang kiểu số nguyên int
    }

    cleaned = normalize_data("user_interest_meta", raw_data)

    assert cleaned is not None
    assert cleaned["interest_id"] == "INT_READING_88"
    assert cleaned["raw_input"] == "Tôi thích đọc sách"
    assert cleaned["ai_tags"] == ["đọc sách", "giải trí"]
    assert isinstance(cleaned["ai_processed_at"], datetime)
    assert cleaned["mapping_attempts"] == 3
    assert isinstance(cleaned["mapping_attempts"], int)


def test_user_interest_meta_defaults():
    """Kiểm thử giá trị mặc định cho user_interest_meta"""
    raw_data = {
        "interest_id": "INT_111"
    }

    cleaned = normalize_data("user_interest_meta", raw_data)

    assert cleaned is not None
    assert cleaned["interest_id"] == "INT_111"
    assert cleaned["raw_input"] is None
    assert cleaned["ai_tags"] == []
    assert cleaned["ai_processed_at"] is None
    assert cleaned["mapping_attempts"] == 0


def test_user_interest_meta_invalid_attempts():
    """Kiểm thử vi phạm ràng buộc số lần mapping không âm"""
    raw_data = {
        "interest_id": "INT_111",
        "mapping_attempts": -1  # Số âm không hợp lệ
    }

    cleaned = normalize_data("user_interest_meta", raw_data)
    assert cleaned is None


def test_user_interest_meta_missing_required():
    """Kiểm thử thiếu trường bắt buộc interest_id"""
    raw_data = {
        "raw_input": "Đọc sách"
    }

    cleaned = normalize_data("user_interest_meta", raw_data)
    assert cleaned is None


# =====================================================================
# THỬ NGHIỆM BẢNG 8: post_meta
# =====================================================================

def test_post_meta_valid():
    raw_data = {
        "post_id": "  POST_1234567890 ",
        "rich_content": "  <p>Hello world</p>  ",
        "media": [
            {"type": " image ", "url": " https://img.com/1.jpg ", "order": 1}
        ],
        "tags": ["  education  ", "  ", "tech"],
        "stats_cache": {
            "like_count": "15",
            "comment_count": 5,
            "share_count": 0,
            "cached_at": "2026-06-19T10:00:00Z"
        },
        "moderation": {
            "status": " APPROVED ",
            "reviewed_by": " admin_01 ",
            "reviewed_at": "2026-06-19 10:05:00"
        }
    }
    cleaned = normalize_data("post_meta", raw_data)
    assert cleaned is not None
    assert cleaned["post_id"] == "POST_1234567890"
    assert cleaned["rich_content"] == "<p>Hello world</p>"
    assert cleaned["media"][0]["type"] == "image"
    assert cleaned["media"][0]["url"] == "https://img.com/1.jpg"
    assert cleaned["tags"] == ["education", "tech"]
    assert cleaned["stats_cache"]["like_count"] == 15
    assert isinstance(cleaned["stats_cache"]["cached_at"], datetime)
    assert cleaned["moderation"]["status"] == "approved"
    assert cleaned["moderation"]["reviewed_by"] == "admin_01"
    assert isinstance(cleaned["moderation"]["reviewed_at"], datetime)


def test_post_meta_invalid_moderation():
    raw_data = {
        "post_id": "POST_123",
        "moderation": {
            "status": "in_review"  # Không hợp lệ, phải thuộc approved/hidden/removed
        }
    }
    cleaned = normalize_data("post_meta", raw_data)
    assert cleaned is None


def test_post_meta_missing_required():
    raw_data = {
        "rich_content": "No ID"
    }
    cleaned = normalize_data("post_meta", raw_data)
    assert cleaned is None


# =====================================================================
# THỬ NGHIỆM BẢNG 9: comment_meta
# =====================================================================

def test_comment_meta_valid():
    raw_data = {
        "comment_id": "COMM_123",
        "rich_content": "Nice post",
        "edit_history": [
            {"content": f"edit_{i}", "edited_at": "2026-06-19T10:00:00Z"} for i in range(15)
        ]
    }
    cleaned = normalize_data("comment_meta", raw_data)
    assert cleaned is not None
    assert len(cleaned["edit_history"]) == 10  # Phải bị giới hạn tối đa 10 phần tử
    assert cleaned["edit_history"][0]["content"] == "edit_5"
    assert cleaned["edit_history"][-1]["content"] == "edit_14"


# =====================================================================
# THỬ NGHIỆM BẢNG 10: group_membership_meta
# =====================================================================

def test_group_membership_meta_valid():
    raw_data = {
        "group_id": " G_123 ",
        "profile_id": " P_456 ",
        "contribution_score": "120",
        "badges_in_group": [" top_commenter ", ""],
        "last_active_at": "2026-06-19T10:00:00Z"
    }
    cleaned = normalize_data("group_membership_meta", raw_data)
    assert cleaned is not None
    assert cleaned["group_id"] == "G_123"
    assert cleaned["profile_id"] == "P_456"
    assert cleaned["contribution_score"] == 120
    assert cleaned["badges_in_group"] == ["top_commenter"]
    assert cleaned["notification_settings"]["new_post"] is True  # Default value


def test_group_membership_meta_negative_score():
    raw_data = {
        "group_id": "G_123",
        "profile_id": "P_456",
        "contribution_score": -10  # Điểm âm không hợp lệ
    }
    cleaned = normalize_data("group_membership_meta", raw_data)
    assert cleaned is None


# =====================================================================
# THỬ NGHIỆM BẢNG 11: message_meta
# =====================================================================

def test_message_meta_valid():
    raw_data = {
        "message_id": " MSG_111 ",
        "rich_content": "Hello",
        "read_by": [
            {"profile_id": " P_1 ", "read_at": "2026-06-19T10:00:00Z"}
        ],
        "is_deleted": "True",
        "deleted_at": "2026-06-19T10:05:00Z"
    }
    cleaned = normalize_data("message_meta", raw_data)
    assert cleaned is not None
    assert cleaned["message_id"] == "MSG_111"
    assert cleaned["read_by"][0]["profile_id"] == "P_1"
    assert cleaned["is_deleted"] is True
    assert isinstance(cleaned["deleted_at"], datetime)


# =====================================================================
# THỬ NGHIỆM BẢNG 12: poll_meta
# =====================================================================

def test_poll_meta_valid():
    raw_data = {
        "poll_id": " POLL_999 ",
        "description": " Favorite color? ",
        "settings": {
            "allow_multiple_votes": "True",
            "show_results_before_close": False
        },
        "stats_cache": {
            "total_votes": "250",
            "cached_at": "2026-06-19T10:00:00Z"
        }
    }
    cleaned = normalize_data("poll_meta", raw_data)
    assert cleaned is not None
    assert cleaned["poll_id"] == "POLL_999"
    assert cleaned["description"] == "Favorite color?"
    assert cleaned["settings"]["allow_multiple_votes"] is True
    assert cleaned["settings"]["show_results_before_close"] is False
    assert cleaned["stats_cache"]["total_votes"] == 250



