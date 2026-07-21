from pydantic import BaseModel


class Credentials(BaseModel):
    use_app_keys: bool = True

    gemini_api_key: str | None = None
    groq_api_key: str | None = None
    