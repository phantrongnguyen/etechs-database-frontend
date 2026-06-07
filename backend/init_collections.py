import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Add current directory to path so we can import models and database
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from middleware.models.student_profile_meta import StudentProfileMetaModel
from middleware.models.education_meta import EducationMetaModel

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "etechs_db")

def seed_database():
    print(f"Connecting to MongoDB: {MONGO_URI}...")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    
    # 1. Mock Data for student_profile_meta
    raw_profile = {
        "profile_id": "PROFILE_KT_001",
        "display_preferences": {
            "theme": "   dark   ",
            "language": "vi",
            "timezone": "Asia/Ho_Chi_Minh"
        },
        "privacy_settings": {
            "show_avatar": "public",
            "show_bio": "   friends_only   ",
            "show_interests": "private"
        },
        "onboarding": {
            "is_completed": "True",
            "steps_done": ["  step_1  ", "step_2"],
            "last_step_at": "2026-06-07T12:00:00Z"
        },
        "tags": ["   active   ", "premium"],
        "ai_summary": "   Học sinh chăm chỉ, thế mạnh các môn Khoa học Tự nhiên.   ",
        "ai_summary_at": "2026-06-07T18:00:00Z"
    }
    
    # 2. Mock Data for education_meta
    raw_education = {
        "education_id": "EDU_KT_999",
        "description": "   Trường THPT Chuyên Lê Hồng Phong   ",
        "achievements": ["   Giải Nhì Tin học trẻ cấp tỉnh   ", "Học sinh giỏi 3 năm liền"],
        "document_urls": ["https://storage.etechs.vn/diploma/edu_kt_999.pdf"],
        "verification_status": "   verified   ",
        "verified_at": "2026-06-08T00:00:00Z"
    }
    
    try:
        # Validate using models (trimming and parsing will be applied automatically)
        print("\nValidating and normalizing profile metadata...")
        profile_model = StudentProfileMetaModel(**raw_profile)
        normalized_profile = profile_model.model_dump()
        print("✅ Normalization success for student_profile_meta:")
        print(normalized_profile)
        
        print("\nValidating and normalizing education metadata...")
        education_model = EducationMetaModel(**raw_education)
        normalized_education = education_model.model_dump()
        print("✅ Normalization success for education_meta:")
        print(normalized_education)
        
        # Insert into MongoDB
        print("\nInserting documents into MongoDB...")
        
        # Insert student_profile_meta
        col_profile = db["student_profile_meta"]
        # Clear existing test documents to prevent duplicate pollution
        col_profile.delete_many({"profile_id": "PROFILE_KT_001"})
        res_profile = col_profile.insert_one(normalized_profile)
        print(f"✅ Created student_profile_meta with _id: {res_profile.inserted_id}")
        
        # Insert education_meta
        col_education = db["education_meta"]
        col_education.delete_many({"education_id": "EDU_KT_999"})
        res_education = col_education.insert_one(normalized_education)
        print(f"✅ Created education_meta with _id: {res_education.inserted_id}")
        
        print("\n🎉 Seeding successful! Both collections initialized in MongoDB.")
        
    except Exception as e:
        print(f"❌ Error during database seeding: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    seed_database()
