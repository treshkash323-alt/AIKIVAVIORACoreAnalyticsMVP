from fastapi import APIRouter

try:
    from ..supabase_service import run_rpc
except ImportError:
    from supabase_service import run_rpc


router = APIRouter(prefix="/api", tags=["analytics"])


@router.get("/monthly-revenue")
def get_monthly_revenue():
    try:
        return run_rpc("monthly_revenue")
    except Exception as exc:
        return {"error": str(exc)}


@router.get("/top-products")
def get_top_products():
    try:
        return run_rpc("top_products", {"lim": 10})
    except Exception as exc:
        return {"error": str(exc)}


@router.get("/revenue-by-category")
def get_revenue_by_category():
    try:
        return run_rpc("revenue_by_category")
    except Exception as exc:
        return {"error": str(exc)}


@router.get("/top-cities")
def get_top_cities():
    try:
        return run_rpc("top_cities", {"lim": 10})
    except Exception as exc:
        return {"error": str(exc)}


@router.get("/top-customers")
def get_top_customers():
    try:
        return run_rpc("top_customers", {"lim": 10})
    except Exception as exc:
        return {"error": str(exc)}
