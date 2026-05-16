from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    deepseek_api_key: str
    openai_api_key: str
    gemini_api_key: str
    model_provider: str
    openai_model: str


settings = Settings(
    supabase_url=os.getenv("SUPABASE_URL") or "",
    supabase_key=os.getenv("SUPABASE_ANON_KEY") or "",
    deepseek_api_key=os.getenv("DEEPSEEK_API_KEY") or "",
    openai_api_key=os.getenv("OPENAI_API_KEY") or "",
    gemini_api_key=os.getenv("GEMINI_API_KEY") or "",
    model_provider=(os.getenv("MODEL_PROVIDER", "deepseek") or "deepseek").strip().lower(),
    openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
)
