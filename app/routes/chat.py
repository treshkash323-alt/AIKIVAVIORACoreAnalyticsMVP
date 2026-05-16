import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

try:
    from ..config import settings
    from ..providers import generate_reply
    from ..supabase_service import build_analytics_context, log_dialog
except ImportError:
    from config import settings
    from providers import generate_reply
    from supabase_service import build_analytics_context, log_dialog


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: List[Dict[str, Any]] = Field(default_factory=list)


@router.post("/chat")
async def chat(req: ChatRequest):
    session_id: str = req.session_id or str(uuid.uuid4())
    context = build_analytics_context()

    system_prompt = f"""Ты — AIKIVAVIORA Analytics AI. Отвечай на русском.
Используй ТОЛЬКО эти данные из базы:
{context}
Если данных нет — честно скажи. Не выдумывай цифры."""

    reply: str = ""
    provider_used: str = settings.model_provider

    try:
        result = generate_reply(system_prompt, req.message)
        reply = result["reply"]
        provider_used = result["provider"]
        if result.get("warning"):
            reply = f"{result['warning']}\n\n{reply}"
    except Exception as exc:
        reply = f"⚠️ Ошибка AI ({settings.model_provider}): {str(exc)}"
        print(f"AI error: {exc}")

    try:
        log_dialog(session_id, req.message, reply, provider_used)
    except Exception as db_err:
        print(f"DB log error: {db_err}")

    return {"reply": reply, "session_id": session_id, "provider": provider_used}
