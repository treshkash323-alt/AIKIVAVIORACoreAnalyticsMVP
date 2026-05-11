from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

test_data = {
    "session_id": "test_session_001",
    "user_role": "user",
    "user_message": "Hello AI",
    "ai_response": "Connection successful",
    "ai_agent": "DeepSeek",
    "sentiment": "neutral",
    "stage": "test",
    "validation_status": "ok",
    "notes": "first database insert"
}

response = supabase.table("ai_dialogs").insert(test_data).execute()

print(response)