import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

MODEL_SCHEMAS = {
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
    ["wallet_asset_meta", "wallet_transaction_meta"],
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
                resp = requests.post(f"{API_URL}/normalize/wallet_asset_meta", json=payload)
            if resp.ok:
                data = resp.json()
                st.success("Thành công!")

                tab1, tab2 = st.tabs(["📦 Dữ liệu đã chuẩn hóa", "🔍 Kiểm tra kiểu"])
                with tab1:
                    st.json(data)
                with tab2:
                    _render_schema(schema, data)
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")

else:
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
                resp = requests.post(f"{API_URL}/normalize/wallet_transaction_meta", json=payload)
            if resp.ok:
                data = resp.json()
                st.success("Thành công!")

                tab1, tab2 = st.tabs(["📦 Dữ liệu đã chuẩn hóa", "🔍 Kiểm tra kiểu"])
                with tab1:
                    st.json(data)
                with tab2:
                    _render_schema(schema, data)
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")
