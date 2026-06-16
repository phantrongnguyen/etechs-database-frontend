from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from middleware.normalizer import normalize_data
from database import connect_db, close_db, get_db
from middleware.repositories.wallet_repo import (
    insert_asset_meta,
    insert_transaction_meta,
    insert_wallet_meta
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(title="ETechs Data Normalizer API", version="1.0.0", lifespan=lifespan)


class NormalizeRequest(BaseModel):
    collection_name: str
    raw_data: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/normalize")
async def normalize(request: NormalizeRequest):
    result = normalize_data(request.collection_name, request.raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    return result


@app.post("/normalize/wallet_asset_meta")
async def normalize_wallet_asset_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_asset_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    try:
        db = get_db()
        inserted_id = await insert_asset_meta(db, result)
        return {**result, "_id": inserted_id}
    except RuntimeError:
        return result


@app.post("/normalize/wallet_transaction_meta")
async def normalize_wallet_transaction_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_transaction_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    try:
        db = get_db()
        inserted_id = await insert_transaction_meta(db, result)
        return {**result, "_id": inserted_id}
    except RuntimeError:
        return result

@app.post("/normalize/wallet_meta")
async def normalize_wallet_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    try:
        db = get_db()
        inserted_id = await insert_wallet_meta(db, result)
        return {**result, "_id": inserted_id}
    except RuntimeError:
        return result