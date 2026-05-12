"""
AIKIVAVIORA — Core Analytics System
FastAPI entry point
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from openai import OpenAI
from supabase import create_client
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

# ============================================
# LOAD ENVIRONMENT
# ============================================

load_dotenv()

SUPABASE_URL      = os.getenv("SUPABASE_URL")
SUPABASE_KEY      = os.getenv("SUPABASE_ANON_KEY")
DEEPSEEK_API_KEY  = os.getenv("DEEPSEEK_API_KEY")
MODEL_PROVIDER    = os.getenv("MODEL_PROVIDER", "deepseek")

# ============================================
# CLIENTS
# ============================================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

print(f"✅ MODEL PROVIDER: {MODEL_PROVIDER}")

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="AIKIVAVIORA Core Analytics MVP",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# STATIC + TEMPLATES
# ============================================

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ============================================
# ROOT PAGE
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user_name": "KIV",
            "model_name": "DeepSeek-R1",
        }
    )

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
def health_check():
    try:
        response = (
            supabase
            .table("ai_dialogs")
            .select("*")
            .limit(1)
            .execute()
        )
        return {
            "status": "ok",
            "database": "connected",
            "model_provider": MODEL_PROVIDER
        }
    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }

# ============================================
# AI CHAT ENDPOINT
# ============================================

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@app.post("/api/chat")
async def chat(body: ChatRequest):
    try:
        session_id = body.session_id or str(uuid.uuid4())[:18]

        # DeepSeek запрос
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AIKIVAVIORA — an intelligent analytics assistant. "
                        "You help analyze business data, answer questions about sales, "
                        "revenue, customers and products. Be concise and insightful."
                    )
                },
                {
                    "role": "user",
                    "content": body.message
                }
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        ai_text = response.choices[0].message.content

        # Сохраняем диалог в Supabase
        try:
            supabase.table("ai_dialogs").insert({
                "session_id":        session_id,
                "user_role":         "user",
                "user_message":      body.message,
                "ai_response":       ai_text,
                "ai_agent":          "DeepSeek",
                "sentiment":         "neutral",
                "stage":             "production",
                "validation_status": "ok",
                "notes":             f"chat {datetime.utcnow().isoformat()}"
            }).execute()
        except Exception as db_err:
            print(f"⚠️ Supabase write error: {db_err}")

        return {
            "status":     "ok",
            "session_id": session_id,
            "response":   ai_text
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

# ============================================
# ANALYTICS ENDPOINTS
# ============================================

@app.get("/api/monthly-revenue")
def get_monthly_revenue():
    try:
        return supabase.rpc("monthly_revenue").execute().data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-products")
def get_top_products():
    try:
        return supabase.rpc("top_products", {"lim": 10}).execute().data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/revenue-by-category")
def get_revenue_by_category():
    try:
        return supabase.rpc("revenue_by_category").execute().data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-cities")
def get_top_cities():
    try:
        return supabase.rpc("top_cities", {"lim": 10}).execute().data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-customers")
def get_top_customers():
    try:
        return supabase.rpc("top_customers", {"lim": 10}).execute().data
    except Exception as e:
        return {"error": str(e)}

# ============================================
# ЗАПУСК: python main.py
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
