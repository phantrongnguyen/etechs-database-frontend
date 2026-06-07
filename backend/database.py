import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "etechs_db")

client = None
db = None

def connect_db():
    """Establish a connection to the MongoDB instance."""
    global client, db
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    print(f"🔌 Connected to MongoDB: {MONGO_URI} (db: {MONGO_DB_NAME})")

def get_db():
    """Retrieve the current database instance."""
    return db

def close_db():
    """Close the MongoDB connection."""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed.")
