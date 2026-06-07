from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from contextlib import asynccontextmanager
from middleware.normalizer import normalize_data
from database import connect_db, close_db, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to MongoDB
    connect_db()
    yield
    # Shutdown: close MongoDB connection
    close_db()

app = FastAPI(title="ETechs Data Normalizer API", version="1.0.0", lifespan=lifespan)


class NormalizeRequest(BaseModel):
    collection_name: str
    raw_data: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-status")
def db_status():
    from database import get_db
    db = get_db()
    return {"db_is_none": db is None, "db_str": str(db)}


@app.post("/normalize")
def normalize(request: NormalizeRequest):
    result = normalize_data(request.collection_name, request.raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    
    # Save to MongoDB
    db = get_db()
    if db is not None:
        try:
            collection = db[request.collection_name]
            doc = result.copy()
            inserted = collection.insert_one(doc)
            result["_id"] = str(inserted.inserted_id)
        except Exception as e:
            print(f"⚠️ Failed to save to MongoDB: {e}")
            
    return result


@app.post("/normalize/wallet_asset_meta")
def normalize_wallet_asset_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_asset_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    
    # Save to MongoDB
    db = get_db()
    if db is not None:
        try:
            collection = db["wallet_asset_meta"]
            doc = result.copy()
            inserted = collection.insert_one(doc)
            result["_id"] = str(inserted.inserted_id)
        except Exception as e:
            print(f"⚠️ Failed to save to MongoDB: {e}")
            
    return result


@app.post("/normalize/wallet_transaction_meta")
def normalize_wallet_transaction_meta(raw_data: Dict[str, Any]):
    result = normalize_data("wallet_transaction_meta", raw_data)
    if result is None:
        raise HTTPException(status_code=422, detail="Validation failed")
    
    # Save to MongoDB
    db = get_db()
    if db is not None:
        try:
            collection = db["wallet_transaction_meta"]
            doc = result.copy()
            inserted = collection.insert_one(doc)
            result["_id"] = str(inserted.inserted_id)
        except Exception as e:
            print(f"⚠️ Failed to save to MongoDB: {e}")
            
    return result

