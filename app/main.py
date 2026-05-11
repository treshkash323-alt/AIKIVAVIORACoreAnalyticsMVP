from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client

import os
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

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title="AIKIVAVIORA Core Analytics MVP",
    version="0.1"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

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