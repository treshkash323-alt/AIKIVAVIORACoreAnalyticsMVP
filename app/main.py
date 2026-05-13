"""
AIKIVAVIORA — Core Analytics System
FastAPI entry point (v0.3 - Fixed)
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from openai import OpenAI
from supabase import create_client
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
import os, uuid
from datetime import datetime

# ============================================
# LOAD ENVIRONMENT
# ============================================
load_dotenv()
SUPABASE_URL: str = os.getenv("SUPABASE_URL") or ""
SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY") or ""
DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY") or ""

# ============================================
# CLIENTS
# ============================================
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ============================================
# FASTAPI APP
# ============================================
app = FastAPI(title="AIKIVAVIORA Core Analytics MVP", version="0.3")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ============================================
# MODELS  ← FIX: типизация исправлена
# ============================================
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []

# ============================================
# HELPER: ANALYTICS CONTEXT
# ============================================
async def build_analytics_context() -> str:
    rpc_calls = [
        ("monthly_revenue", {}),
        ("top_products", {"lim": 10}),
        ("revenue_by_category", {}),
        ("top_cities", {"lim": 10}),
        ("top_customers", {"lim": 10}),
    ]
    parts = []
    for name, params in rpc_calls:
        try:
            data = supabase.rpc(name, params).execute().data
            parts.append(f"## {name}\n{data}")
        except Exception as e:
            parts.append(f"## {name}\nError: {e}")
    return "\n\n".join(parts)

# ============================================
# ROUTES
# ============================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user_name": "KIV"}
    )

@app.get("/health")
def health():
    try:
        supabase.table("ai_dialogs").select("id").limit(1).execute()
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    session_id: str = req.session_id or str(uuid.uuid4())
    context = await build_analytics_context()

    system_prompt = f"""Ты — AIKIVAVIORA Analytics AI. Отвечай на русском.
Используй ТОЛЬКО эти данные из базы:
{context}
Если данных нет — честно скажи. Не выдумывай цифры."""

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        reply: str = response.choices[0].message.content or "Нет ответа"
    except Exception as e:
        reply = f"⚠️ Ошибка AI: {e}"
        print(f"DeepSeek error: {e}")

    # Log to DB
    try:
        supabase.table("ai_dialogs").insert({
            "session_id": session_id,
            "user_message": req.message,
            "ai_response": reply,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as db_err:
        print(f"DB log error: {db_err}")

    return {"reply": reply, "session_id": session_id}

# ============================================
# ANALYTICS ENDPOINTS
# ============================================
@app.get("/api/monthly-revenue")
def get_monthly_revenue():
    try: return supabase.rpc("monthly_revenue").execute().data
    except Exception as e: return {"error": str(e)}

@app.get("/api/top-products")
def get_top_products():
    try: return supabase.rpc("top_products", {"lim": 10}).execute().data
    except Exception as e: return {"error": str(e)}

@app.get("/api/revenue-by-category")
def get_revenue_by_category():
    try: return supabase.rpc("revenue_by_category").execute().data
    except Exception as e: return {"error": str(e)}

@app.get("/api/top-cities")
def get_top_cities():
    try: return supabase.rpc("top_cities", {"lim": 10}).execute().data
    except Exception as e: return {"error": str(e)}

@app.get("/api/top-customers")
def get_top_customers():
    try: return supabase.rpc("top_customers", {"lim": 10}).execute().data
    except Exception as e: return {"error": str(e)}

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)