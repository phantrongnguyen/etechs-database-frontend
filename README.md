# ETechs Data Normalizer

Hệ thống chuẩn hóa dữ liệu đầu vào cho các collection MongoDB sử dụng **FastAPI** (backend) và **Streamlit** (frontend). Dữ liệu thô được validate, làm sạch (trim whitespace, chuẩn hóa kiểu dữ liệu, kiểm tra enum, ràng buộc logic) trước khi lưu vào database.

---

## Tính năng

- ✅ Chuẩn hóa dữ liệu collection `wallet_asset_meta`
- ✅ Chuẩn hóa dữ liệu collection `wallet_transaction_meta`
- ✅ Tự động trim khoảng trắng, chuẩn hóa chữ hoa/thường
- ✅ Parse datetime từ chuỗi ISO format
- ✅ Ép kiểu Boolean từ string
- ✅ Ép kiểu số từ string → int
- ✅ Kiểm tra enum (triggered_by)
- ✅ Ràng buộc logic nghiệp vụ (số dư không âm)
- ✅ Kiểm tra trường bắt buộc
- ✅ API RESTful với tài liệu tự động (Swagger UI)
- ✅ Giao diện Streamlit nhập liệu trực quan

---

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Backend | Python 3.12+, FastAPI, Uvicorn |
| Validation | Pydantic v2 (BaseModel, field_validator) |
| Frontend | Streamlit |
| Testing | Pytest |
| Khác | Requests, python-dotenv |

---

## Cấu trúc thư mục

```
etechs/
├── backend/
│   ├── main.py                          # FastAPI app - định nghĩa endpoints
│   ├── requirements.txt                 # Danh sách dependencies
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── normalizer.py                # Hàm điều phối normalize_data()
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── wallet_asset_meta.py     # Pydantic model cho wallet_asset_meta
│   │       └── wallet_transaction_meta.py # Pydantic model cho wallet_transaction_meta
│   └── tests/
│       ├── __init__.py
│       └── test_normalizer.py           # Unit tests
├── frontend/
│   └── form.py                          # Streamlit UI
├── docs/                                # Tài liệu dự án (Word, PDF)
└── README.md
```

---

## Hướng dẫn cài đặt & chạy

### Yêu cầu

- Python 3.12+
- pip

### 1. Clone dự án

```bash
git clone git@github.com:phantrongnguyen/etechs-database-frontend.git
cd etechs
```

### 2. Tạo môi trường ảo & cài dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install requirements.txt
```

### 3. Chạy backend (FastAPI)

```bash
.\venv\Scripts\uvicorn.exe main:app --reload
```

Backend chạy tại: **http://localhost:8000**

Tài liệu API tự động (Swagger UI): **http://localhost:8000/docs**

### 4. Chạy frontend (Streamlit) — mở terminal riêng

```bash
cd backend
.\venv\Scripts\streamlit.exe run ..\frontend\form.py
```

Frontend chạy tại: **http://localhost:8501**

---

## API Endpoints

### `GET /health`

Kiểm tra trạng thái server.

**Response:**
```json
{ "status": "ok" }
```

### `POST /normalize`

Chuẩn hóa dữ liệu theo tên collection.

**Request body:**
```json
{
  "collection_name": "wallet_asset_meta",
  "raw_data": {
    "asset_id": "   ASSET_001   ",
    "display_name": "  Huy hiệu  ",
    "icon_url": "https://example.com/icon.png",
    "earned_at": "2026-06-06T17:00:00Z",
    "source": { "ref_type": "   assessment   ", "ref_id": "ID_01" },
    "is_tradable": "True"
  }
}
```

**Response (200):**
```json
{
  "asset_id": "ASSET_001",
  "display_name": "Huy hiệu",
  "icon_url": "https://example.com/icon.png",
  "earned_at": "2026-06-06T17:00:00+00:00",
  "source": { "ref_type": "assessment", "ref_id": "ID_01" },
  "is_tradable": true
}
```

### `POST /normalize/wallet_asset_meta`

Endpoint riêng cho collection `wallet_asset_meta` (không cần truyền `collection_name`).

### `POST /normalize/wallet_transaction_meta`

Endpoint riêng cho collection `wallet_transaction_meta`.

---

## Chạy kiểm thử

```bash
cd backend
pytest tests\test_normalizer.py -v
```

Kết quả mong đợi: **5 passed**

| Test case | Mục đích |
|-----------|----------|
| `test_wallet_asset_meta_valid` | Dữ liệu hợp lệ → trim string, parse datetime, ép boolean |
| `test_wallet_asset_meta_missing_required` | Thiếu trường bắt buộc → trả về None |
| `test_wallet_transaction_meta_valid` | Ép kiểu số từ string, lowercasing |
| `test_wallet_transaction_meta_invalid_enum` | triggered_by không hợp lệ → trả về None |
| `test_wallet_transaction_meta_negative_balance` | Số dư âm → trả về None |

---

## Quy trình phát triển

Dự án được xây dựng theo các bước sau:

### Bước 1: Khởi tạo dự án

- Tạo cấu trúc thư mục backend/frontend
- Thiết lập môi trường ảo Python
- Cài đặt FastAPI, Uvicorn, Pydantic, Streamlit

### Bước 2: Xây dựng Pydantic Models

- Tách riêng model cho từng collection MongoDB
- Sử dụng `field_validator` để trim string, parse datetime, kiểm tra enum
- Xây dựng model con (nested) như `AssetSource`, `BalanceSnapshot`

### Bước 3: Xây dựng Normalizer Middleware

- Tạo hàm `normalize_data()` nhận collection_name + raw_data
- Điều phối đến model tương ứng
- Xử lý lỗi tập trung

### Bước 4: Xây dựng FastAPI endpoints

- `GET /health` — kiểm tra health check
- `POST /normalize` — endpoint tổng quát
- `POST /normalize/wallet_asset_meta` — endpoint riêng
- `POST /normalize/wallet_transaction_meta` — endpoint riêng

### Bước 5: Viết Unit Tests

- Test happy path: dữ liệu hợp lệ → chuẩn hóa thành công
- Test edge cases: thiếu field, enum sai, số âm
- Dùng Pytest để kiểm thử tự động

### Bước 6: Xây dựng Frontend Streamlit

- Form nhập liệu cho từng collection
- Gọi API backend bằng requests
- Hiển thị kết quả JSON

### Bước 7: Kiểm thử tích hợp

- Chạy backend + frontend đồng thời
- Kiểm tra luồng dữ liệu từ UI → API → Model → Response

---

## Mở rộng

Để thêm collection mới:

1. Tạo file model mới trong `backend/middleware/models/` (VD: `student_profile.py`)
2. Viết Pydantic BaseModel với các `field_validator` tương ứng
3. Thêm `elif` trong `normalizer.py` để mapping collection_name → model
4. Thêm endpoint mới trong `main.py` nếu cần
5. Viết test cases trong `tests/`
6. Thêm form nhập liệu trong `frontend/form.py`

---

## License

MIT
