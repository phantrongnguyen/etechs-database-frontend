import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

MODEL_SCHEMAS = {
    "wallet_meta": {
        "fields": {
            "wallets_id": {"type": "str", "required": True, "note": "max 16 ký tự"},
            "wallet_label": {"type": "str | null", "required": False, "note": "Mặc định: Ví chính"},
            "spending_summary": {
                "type": "object",
                "required": False,
                "fields": {
                    "total_earned": {"type": "int", "required": False},
                    "total_spent": {"type": "int", "required": False},
                    "last_tx_at": {"type": "datetime (ISO)", "required": False},
                },
            },
            "auto_topup": {
                "type": "object",
                "required": False,
                "fields": {
                    "enabled": {"type": "bool", "required": False},
                    "threshold": {"type": "int", "required": False},
                    "amount": {"type": "int", "required": False},
                },
            },
        }
    },
    "wallet_asset_meta": {
        "fields": {
            "asset_id": {"type": "str", "required": True, "note": "max 16 ký tự"},
            "display_name": {"type": "str", "required": False},
            "icon_url": {"type": "str (URL)", "required": False},
            "description": {"type": "str | null", "required": False},
            "earned_at": {"type": "datetime (ISO)", "required": False},
            "source": {
                "type": "object",
                "required": False,
                "fields": {
                    "ref_type": {"type": "str | null", "required": False},
                    "ref_id": {"type": "str | null", "required": False},
                },
            },
            "is_tradable": {"type": "bool", "required": False},
        }
    },
    "wallet_transaction_meta": {
        "fields": {
            "tx_id": {"type": "str", "required": True, "note": "max 16 ký tự"},
            "note": {"type": "str | null", "required": False},
            "triggered_by": {
                "type": "enum",
                "required": False,
                "note": "system_auto, admin, user, marketplace",
            },
            "snapshot": {
                "type": "object",
                "required": False,
                "fields": {
                    "balance_before": {"type": "int", "required": False},
                    "balance_after": {"type": "int", "required": False},
                },
            },
            "receipt_url": {"type": "str | null", "required": False},
        }
    },
    "identity_meta": {
        "fields": {
            "indentity_id": {"type": "str", "required": True, "note": "max 16 ký tự"},
            "scan_urls": {"type": "array", "required": False, "note": "mảng URL ảnh"},
            "ocr_extracted": {
                "type": "object",
                "required": False,
                "note": "full_name, dob, address...",
            },
            "verification_status": {
                "type": "enum",
                "required": False,
                "note": "pending, verified, rejected",
            },
            "review_note": {"type": "str | null", "required": False},
        }
    },
}


def _resolve_type(value):
    if value is None:
        return "null"
    t = type(value).__name__
    if t == "bool":
        return "bool"
    if t == "int":
        return "int"
    if t == "float":
        return "float"
    if t == "str":
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return "datetime (ISO)"
        except (ValueError, AttributeError):
            pass
        return "str"
    if t == "dict":
        return "object"
    if t == "list":
        return "array"
    return t


def _check_type(value, expected_type):
    if expected_type == "str | null":
        return value is None or isinstance(value, str)
    if expected_type == "str":
        return isinstance(value, str)
    if expected_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "bool":
        return isinstance(value, bool)
    if expected_type == "str (URL)":
        return isinstance(value, str) and value.startswith("http")
    if expected_type == "datetime (ISO)":
        if not isinstance(value, str):
            return False
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False
    if expected_type == "enum":
        return isinstance(value, str)
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "null":
        return value is None
    return True


def _render_schema(schema, data=None, prefix=""):
    for key, meta in schema["fields"].items():
        full_key = f"{prefix}.{key}" if prefix else key

        if meta["type"] == "object" and "fields" in meta:
            st.markdown(f"**• {key}** `object`")
            sub_data = (data or {}).get(key, {}) if data else {}
            _render_schema({"fields": meta["fields"]}, sub_data, full_key)
            continue

        col1, col2, col3 = st.columns([2, 1.5, 1])
        col1.markdown(f"`{key}`")

        if data is not None:
            actual = data.get(key)
            actual_type = _resolve_type(actual)
            col2.code(actual_type, language="")

            expected = meta["type"]
            ok = _check_type(actual, expected)
            status = "✅" if ok else "❌"
            col3.markdown(f"**{status}**")
        else:
            col2.caption(meta["type"])
            if meta.get("note"):
                col3.caption(meta["note"])


st.set_page_config(page_title="ETechs Data Normalizer", layout="wide")
st.title("ETechs Data Normalizer")

collection = st.selectbox(
    "Chọn loại dữ liệu",
    ["wallet_asset_meta", "wallet_transaction_meta", "wallet_meta", "identity_meta"],
)

schema = MODEL_SCHEMAS[collection]

with st.sidebar:
    st.header("📐 Schema mong đợi")
    st.caption(f"**{collection}**")
    _render_schema(schema)

    st.markdown("---")
    st.header("📊 Kiểm tra kiểu dữ liệu")
    st.caption("Kết quả sau khi chuẩn hóa sẽ được so sánh với schema ở trên.")

st.markdown("---")

if collection == "wallet_asset_meta":
    with st.form("asset_form"):
        st.subheader("Wallet Asset Meta")

        asset_id = st.text_input("asset_id *", value="   ASSET_MATH_101   ")
        display_name = st.text_input("display_name", value="  Huy hiệu Toán Học  ")
        icon_url = st.text_input("icon_url", "https://storage.cloud.com/icons/math.png")
        description = st.text_input("description", "Đạt điểm tối đa")
        earned_at = st.text_input("earned_at", "2026-06-06T17:00:00Z")
        is_tradable = st.text_input("is_tradable", "True")

        st.subheader("Source")
        col1, col2 = st.columns(2)
        with col1:
            ref_type = st.text_input("ref_type", "   assessment   ")
        with col2:
            ref_id = st.text_input("ref_id", "KT_01")

        submitted = st.form_submit_button("Gửi & Chuẩn hóa")

        if submitted:
            payload = {
                "asset_id": asset_id,
                "display_name": display_name,
                "icon_url": icon_url,
                "description": description if description else None,
                "earned_at": earned_at,
                "source": {"ref_type": ref_type, "ref_id": ref_id},
                "is_tradable": is_tradable,
            }
            with st.spinner("Đang chuẩn hóa..."):
                resp = requests.post(f"{API_URL}/normalize/wallet_asset_meta", json=payload, timeout=10)
            if resp.ok:
                data = resp.json()
                _id = data.pop("_id", None)
                if _id:
                    st.success(f"✅ Đã chuẩn hóa & lưu vào MongoDB (_id: `{_id}`)")
                else:
                    st.success("✅ Đã chuẩn hóa (MongoDB chưa kết nối)")

                tab1, tab2 = st.tabs(["📦 Dữ liệu đã chuẩn hóa", "🔍 Kiểm tra kiểu"])
                with tab1:
                    st.json(data)
                with tab2:
                    _render_schema(schema, data)
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")

elif collection == "wallet_transaction_meta":
    with st.form("tx_form"):
        st.subheader("Wallet Transaction Meta")

        tx_id = st.text_input("tx_id *", "TX_99999")
        note = st.text_input("note", "Học sinh nạp tiền")
        triggered_by = st.selectbox("triggered_by", ["system_auto", "admin", "user", "marketplace"])
        receipt_url = st.text_input("receipt_url", "https://receipts.com/1.pdf")

        st.subheader("Snapshot")
        col1, col2 = st.columns(2)
        with col1:
            balance_before = st.number_input("balance_before", value=50000, step=1)
        with col2:
            balance_after = st.number_input("balance_after", value=250000, step=1)

        submitted = st.form_submit_button("Gửi & Chuẩn hóa")

        if submitted:
            payload = {
                "tx_id": tx_id,
                "note": note if note else None,
                "triggered_by": triggered_by,
                "snapshot": {
                    "balance_before": int(balance_before),
                    "balance_after": int(balance_after),
                },
                "receipt_url": receipt_url if receipt_url else None,
            }
            with st.spinner("Đang chuẩn hóa..."):
                resp = requests.post(f"{API_URL}/normalize/wallet_transaction_meta", json=payload, timeout=10)
            if resp.ok:
                data = resp.json()
                _id = data.pop("_id", None)
                if _id:
                    st.success(f"✅ Đã chuẩn hóa & lưu vào MongoDB (_id: `{_id}`)")
                else:
                    st.success("✅ Đã chuẩn hóa (MongoDB chưa kết nối)")

                tab1, tab2 = st.tabs(["📦 Dữ liệu đã chuẩn hóa", "🔍 Kiểm tra kiểu"])
                with tab1:
                    st.json(data)
                with tab2:
                    _render_schema(schema, data)
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")

elif collection == "wallet_meta":
    with st.form("wallet_meta_form"):
        st.subheader("Wallet Meta")

        wallets_id = st.text_input("wallets_id *", "   WALLET_123   ")
        wallet_label = st.text_input("wallet_label", "  Ví chính  ")

        st.subheader("Spending Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_earned = st.number_input("total_earned", value=100000, step=1)
        with col2:
            total_spent = st.number_input("total_spent", value=50000, step=1)
        with col3:
            last_tx_at = st.text_input("last_tx_at", "2026-06-06T17:00:00Z")

        st.subheader("Auto Topup")
        col4, col5, col6 = st.columns(3)
        with col4:
            enabled = st.checkbox("enabled", value=True)
        with col5:
            threshold = st.number_input("threshold", value=10000, step=1)
        with col6:
            amount = st.number_input("amount", value=50000, step=1)

        submitted = st.form_submit_button("Gửi & Chuẩn hóa")

        if submitted:
            payload = {
                "wallets_id": wallets_id,
                "wallet_label": wallet_label if wallet_label else None,
                "spending_summary": {
                    "total_earned": int(total_earned),
                    "total_spent": int(total_spent),
                    "last_tx_at": last_tx_at if last_tx_at else None,
                },
                "auto_topup": {
                    "enabled": enabled,
                    "threshold": int(threshold) if threshold > 0 else None,
                    "amount": int(amount) if amount > 0 else None,
                },
            }
            with st.spinner("Đang chuẩn hóa..."):
                resp = requests.post(f"{API_URL}/normalize/wallet_meta", json=payload, timeout=10)
            if resp.ok:
                data = resp.json()
                _id = data.pop("_id", None)
                if _id:
                    st.success(f"✅ Đã chuẩn hóa & lưu vào MongoDB (_id: `{_id}`)")
                else:
                    st.success("✅ Đã chuẩn hóa (MongoDB chưa kết nối)")

                tab1, tab2 = st.tabs(["📦 Dữ liệu đã chuẩn hóa", "🔍 Kiểm tra kiểu"])
                with tab1:
                    st.json(data)
                with tab2:
                    _render_schema(schema, data)
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")

else:
    with st.form("identity_form"):
        st.subheader("Identity Meta")

        indentity_id = st.text_input("indentity_id *", value="   ID_DOC_777   ")
        scan_urls_raw = st.text_input("scan_urls (phân cách bằng dấu phẩy)", value="https://storage.cloud.com/docs/front.jpg, https://storage.cloud.com/docs/back.jpg")
        
        st.subheader("OCR Extracted (JSON)")
        ocr_extracted_raw = st.text_area("ocr_extracted (JSON format)", value='{\n  "full_name": "Nguyen Van A",\n  "dob": "1999-01-01",\n  "address": "123 Street"\n}')
        
        verification_status = st.selectbox("verification_status", ["pending", "verified", "rejected"])
        review_note = st.text_input("review_note", "Giấy tờ hợp lệ")

        submitted = st.form_submit_button("Gửi & Chuẩn hóa")

        if submitted:
            scan_urls = [url.strip() for url in scan_urls_raw.split(",") if url.strip()] if scan_urls_raw else []
            
            import json
            try:
                ocr_extracted = json.loads(ocr_extracted_raw) if ocr_extracted_raw else {}
                if not isinstance(ocr_extracted, dict):
                    st.error("ocr_extracted phải là một JSON Object (Dictionary)")
                    ocr_extracted = {}
            except json.JSONDecodeError:
                st.error("Định dạng JSON của ocr_extracted không hợp lệ")
                ocr_extracted = {}

            payload = {
                "indentity_id": indentity_id,
                "scan_urls": scan_urls,
                "ocr_extracted": ocr_extracted,
                "verification_status": verification_status,
                "review_note": review_note if review_note else None,
            }
            with st.spinner("Đang chuẩn hóa..."):
                resp = requests.post(f"{API_URL}/normalize/identity_meta", json=payload, timeout=10)
            if resp.ok:
                data = resp.json()
                _id = data.pop("_id", None)
                if _id:
                    st.success(f"✅ Đã chuẩn hóa & lưu vào MongoDB (_id: `{_id}`)")
                else:
                    st.success("✅ Đã chuẩn hóa (MongoDB chưa kết nối)")

                tab1, tab2 = st.tabs(["📦 Dữ liệu đã chuẩn hóa", "🔍 Kiểm tra kiểu"])
                with tab1:
                    st.json(data)
                with tab2:
                    _render_schema(schema, data)
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")
