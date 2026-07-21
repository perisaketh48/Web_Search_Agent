from openai import OpenAI

from app.config.settings import settings
from app.schemas.credentials import Credentials
from app.schemas.llm_client import LLMClient


def create_llm_client(
    credentials: Credentials,
    provider: str,
) -> LLMClient:

    # -------------------------
    # App Keys (Portkey)
    # -------------------------

    if credentials.use_app_keys:
        return LLMClient(
            client=OpenAI(
                api_key=settings.PORTKEY_API_KEY,
                base_url="https://api.portkey.ai/v1",
            ),
            use_portkey=True,
        )

    # -------------------------
    # User Gemini
    # -------------------------

    if provider == "gemini":

        return LLMClient(
            client=OpenAI(
                api_key=credentials.gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
            use_portkey=False,
        )

    # -------------------------
    # User Groq
    # -------------------------

    if provider == "groq":

        return LLMClient(
            client=OpenAI(
                api_key=credentials.groq_api_key,
                base_url="https://api.groq.com/openai/v1",
            ),
            use_portkey=False,
        )

    raise ValueError(f"Unsupported provider: {provider}")