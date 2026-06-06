from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from middleware.normalizer import normalize_data

app = FastAPI(title="ETechs Data Normalizer API", version="1.0.0")


class NormalizeRequest(BaseModel):
    collection_name: str
    raw_data: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/normalize")
def normalize(request: NormalizeRequest):
    result = normalize_data(request.collection_name, request.raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    return result


@app.post("/normalize/wallet_asset_meta")
def normalize_wallet_asset_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_asset_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    return result


@app.post("/normalize/wallet_transaction_meta")
def normalize_wallet_transaction_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_transaction_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    return result
