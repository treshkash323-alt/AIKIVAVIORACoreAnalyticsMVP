from datetime import datetime

from supabase import create_client

try:
    from .config import settings
except ImportError:
    from config import settings


supabase = create_client(settings.supabase_url, settings.supabase_key) if settings.supabase_url and settings.supabase_key else None


def require_supabase():
    if supabase is None:
        raise RuntimeError("Supabase client is not configured")
    return supabase


def build_analytics_context() -> str:
    client = require_supabase()
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
            data = client.rpc(name, params).execute().data
            parts.append(f"## {name}\n{data}")
        except Exception as exc:
            parts.append(f"## {name}\nError: {exc}")
    return "\n\n".join(parts)


def check_health() -> dict:
    client = require_supabase()
    client.table("ai_dialogs").select("id").limit(1).execute()
    return {"status": "ok", "db": "connected", "database": "connected"}


def log_dialog(session_id: str, user_message: str, ai_response: str, provider: str) -> None:
    client = require_supabase()
    client.table("ai_dialogs").insert(
        {
            "session_id": session_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "ai_agent": provider,
            "created_at": datetime.utcnow().isoformat(),
        }
    ).execute()


def run_rpc(name: str, params: dict | None = None):
    client = require_supabase()
    return client.rpc(name, params or {}).execute().data
