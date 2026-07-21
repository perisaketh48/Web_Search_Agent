from app.config.settings import settings

LLM_PROVIDERS = {
    "gemini": {
        "provider": "gemini",
        "portkey_provider": "@gemini-for-saketh",
        "model": "gemini-2.5-flash",
    },
    "groq": {
    "provider": "groq",
    "portkey_provider": "@groq-for-saketh",
    "model": "openai/gpt-oss-120b",
    },
}


DEFAULT_LLM = settings.DEFAULT_PROVIDER