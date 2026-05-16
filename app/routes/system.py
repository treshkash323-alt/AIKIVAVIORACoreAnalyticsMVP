from fastapi import APIRouter

try:
    from ..config import settings
    from ..supabase_service import check_health
except ImportError:
    from config import settings
    from supabase_service import check_health


router = APIRouter(tags=["system"])


@router.get("/health")
def health():
    try:
        result = check_health()
        result["model_provider"] = settings.model_provider
        return result
    except Exception as exc:
        return {
            "status": "error",
            "db": "disconnected",
            "database": "disconnected",
            "model_provider": settings.model_provider,
            "message": str(exc),
        }
