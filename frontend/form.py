import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="ETechs Data Normalizer", layout="centered")
st.title("ETechs Data Normalizer")

collection = st.selectbox(
    "Chọn loại dữ liệu",
    ["wallet_asset_meta", "wallet_transaction_meta"]
)

st.markdown("---")

if collection == "wallet_asset_meta":
    with st.form("asset_form"):
        st.subheader("Wallet Asset Meta")

        asset_id = st.text_input("asset_id *", value="   ASSET_MATH_101   ")
        display_name = st.text_input("display_name *", value="  Huy hiệu Toán Học  ")
        icon_url = st.text_input("icon_url *", "https://storage.cloud.com/icons/math.png")
        description = st.text_input("description", "Đạt điểm tối đa")
        earned_at = st.text_input("earned_at *", "2026-06-06T17:00:00Z")
        is_tradable = st.text_input("is_tradable", "True")

        st.subheader("Source")
        col1, col2 = st.columns(2)
        with col1:
            ref_type = st.text_input("ref_type *", "   assessment   ")
        with col2:
            ref_id = st.text_input("ref_id *", "KT_01")

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
                st.success("Thành công!")
                st.json(resp.json())
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")

else:
    with st.form("tx_form"):
        st.subheader("Wallet Transaction Meta")

        tx_id = st.text_input("tx_id *", "TX_99999")
        note = st.text_input("note", "Học sinh nạp tiền")
        triggered_by = st.selectbox("triggered_by *", ["system_auto", "admin", "user", "marketplace"])
        receipt_url = st.text_input("receipt_url", "https://receipts.com/1.pdf")

        st.subheader("Snapshot")
        col1, col2 = st.columns(2)
        with col1:
            balance_before = st.number_input("balance_before *", value=50000, step=1)
        with col2:
            balance_after = st.number_input("balance_after *", value=250000, step=1)

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
                st.success("Thành công!")
                st.json(resp.json())
            else:
                st.error(f"Lỗi {resp.status_code}: {resp.text}")
