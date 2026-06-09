import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

load_dotenv()

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_db():
    global client, db
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "etechs_database")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    print(f"✅ Đã kết nối MongoDB: {db_name}")


async def close_db():
    global client
    if client:
        client.close()
        print("✅ Đã đóng kết nối MongoDB")


def get_db() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("MongoDB chưa được kết nối")
    return db
