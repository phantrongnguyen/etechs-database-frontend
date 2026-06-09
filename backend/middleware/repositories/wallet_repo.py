from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


async def insert_asset_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.utcnow()}
    result = await db["wallet_asset_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_transaction_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.utcnow()}
    result = await db["wallet_transaction_meta"].insert_one(doc)
    return str(result.inserted_id)
