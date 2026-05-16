from openai import OpenAI

try:
    from google import genai
except ImportError:
    genai = None

try:
    from .config import settings
except ImportError:
    from config import settings


deepseek_client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url="https://api.deepseek.com",
) if settings.deepseek_api_key else None

openai_client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

gemini_client = genai.Client() if settings.gemini_api_key and genai else None


def _call_deepseek(system_prompt: str, user_message: str) -> str:
    if not deepseek_client:
        raise RuntimeError("DeepSeek client is not configured")
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=2048,
        temperature=0.7,
    )
    return response.choices[0].message.content or "Нет ответа"


def _call_openai(system_prompt: str, user_message: str) -> str:
    if not openai_client:
        raise RuntimeError("OpenAI client is not configured")
    response = openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=2048,
        temperature=0.7,
    )
    return response.choices[0].message.content or "Нет ответа"


def _call_gemini(system_prompt: str, user_message: str) -> str:
    if not gemini_client:
        raise RuntimeError("Gemini client is not configured")
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{system_prompt}\n\nUser: {user_message}",
    )
    return response.text or "Нет ответа"


PROVIDER_CALLS = {
    "deepseek": _call_deepseek,
    "openai": _call_openai,
    "gemini": _call_gemini,
}


def _fallback_chain(primary_provider: str) -> list[str]:
    fallback_order = ["deepseek", "openai", "gemini"]
    chain = [primary_provider]
    for provider in fallback_order:
        if provider not in chain:
            chain.append(provider)
    return chain


def _friendly_error_message(provider: str) -> str:
    provider_labels = {
        "deepseek": "DeepSeek",
        "openai": "OpenAI",
        "gemini": "Gemini",
    }
    label = provider_labels.get(provider, provider)
    return f"⚠️ {label} сейчас недоступен. Переключаюсь на резервный провайдер, если он настроен."


def generate_reply(system_prompt: str, user_message: str) -> dict:
    requested_provider = settings.model_provider
    errors: list[tuple[str, str]] = []

    for provider in _fallback_chain(requested_provider):
        call = PROVIDER_CALLS.get(provider)
        if call is None:
            errors.append((provider, "Provider is not supported"))
            continue

        try:
            reply = call(system_prompt, user_message)
            warning = None
            if provider != requested_provider:
                warning = _friendly_error_message(requested_provider)
            return {
                "reply": reply,
                "provider": provider,
                "warning": warning,
            }
        except Exception as exc:
            print(f"AI error [{provider}]: {exc}")
            errors.append((provider, str(exc)))

    return {
        "reply": "⚠️ Сейчас ни один AI-провайдер не ответил. Проверьте ключи, квоты и настройки API.",
        "provider": requested_provider,
        "warning": None,
        "errors": errors,
    }
