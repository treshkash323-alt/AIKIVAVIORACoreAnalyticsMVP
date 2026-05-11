from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
import os

# ============================================
# LOAD ENVIRONMENT
# ============================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")

# ============================================
# SUPABASE CLIENT
# ============================================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = None

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
print(f"MODEL PROVIDER: {MODEL_PROVIDER}")

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="AIKIVAVIORA Core Analytics MVP",
    version="0.1"
)

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
def root():

    return {
        "status": "online",
        "project": "AIKIVAVIORA Core Analytics MVP",
        "database": "connected",
        "model_provider": "DeepSeek"
    }

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
def health_check():

    response = supabase.table("ai_dialogs").select("*").limit(1).execute()

    return {
        "api": "ok",
        "database": "ok",
        "records_found": len(response.data)
    }