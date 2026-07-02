from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone


async def insert_asset_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["wallet_asset_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_transaction_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["wallet_transaction_meta"].insert_one(doc)
    return str(result.inserted_id)

async def insert_wallet_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["wallet_meta"].insert_one(doc)
    return str(result.inserted_id)

async def insert_identity_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["identity_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_education_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["education_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_student_profile_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["student_profile_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_user_interest_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["user_interest_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_post_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["post_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_comment_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["comment_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_group_membership_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["group_membership_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_message_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["message_meta"].insert_one(doc)
    return str(result.inserted_id)


async def insert_poll_meta(db: AsyncIOMotorDatabase, data: dict) -> str:
    doc = {**data, "created_at": datetime.now(timezone.utc)}
    result = await db["poll_meta"].insert_one(doc)
    return str(result.inserted_id)




