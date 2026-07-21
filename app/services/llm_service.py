from typing import TypeVar
import json
from pydantic import ValidationError
import logfire
from pydantic import BaseModel
from portkey_ai import createHeaders

from app.services.llm_client_factory import create_llm_client
from app.schemas.credentials import Credentials
from app.config.llm_providers import (
    LLM_PROVIDERS,
    DEFAULT_LLM,
)

T = TypeVar("T", bound=BaseModel)


class LLMService:

    def __init__(
        self,
        credentials: Credentials,
    ):
        self.credentials = credentials

    def _get_provider_config(self, provider: str):
        return LLM_PROVIDERS[provider]

    def _resolve_provider(self, provider: str | None) -> str:
        """
        Resolve which provider should be used.

        Rules:
        - If provider is explicitly passed, use it.
        - If using app keys, use the default provider.
        - If using user keys:
            * Both keys -> default provider (Gemini)
            * Only Gemini -> Gemini
            * Only Groq -> Groq
        """

        if provider is not None:
            return provider

        if self.credentials.use_app_keys:
            return DEFAULT_LLM

        has_gemini = bool(self.credentials.gemini_api_key)
        has_groq = bool(self.credentials.groq_api_key)

        if has_gemini:
            return "gemini"

        if has_groq:
            return "groq"

        raise ValueError(
            "No API key provided. Please enter at least one API key."
        )

    def _should_fallback(self, exception: Exception) -> bool:
        """
        Decide whether Gemini errors should fallback to Groq.
        """

        error = str(exception).lower()

        fallback_errors = [
            "429",
            "resource_exhausted",
            "quota exceeded",
            "rate limit",
            "rate_limit",
            "503",
            "502",
            "500",
            "timeout",
        ]

        return any(keyword in error for keyword in fallback_errors)

    def _generate_with_provider(
        self,
        system_prompt: str,
        user_prompt: str,
        provider: str,
    ) -> str:

        config = self._get_provider_config(provider)

        llm_client = create_llm_client(
    credentials=self.credentials,
    provider=provider,
)

        client = llm_client.client

        with logfire.span(
    "LLM Generate",
    provider=provider,
    model=config["model"],
):
            headers = None

            if llm_client.use_portkey:
                headers = createHeaders(provider=config["portkey_provider"],)

            response = client.chat.completions.create(
                model=config["model"],
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                extra_headers=headers,
            )

            return response.choices[0].message.content

    def _generate_structured_with_provider(
    self,
    system_prompt: str,
    user_prompt: str,
    response_model: type[T],
    provider: str,
) -> T:

        config = self._get_provider_config(provider)

        llm_client = create_llm_client(
            credentials=self.credentials,
            provider=provider,
        )

        client = llm_client.client

        with logfire.span(
            "LLM Structured Generate",
            provider=provider,
            model=config["model"],
        ):
            headers = None

            if llm_client.use_portkey:
                headers = createHeaders(
                    provider=config["portkey_provider"],
                )

            # Providers that support native structured outputs
            if provider == "gemini" or llm_client.use_portkey:

                response = client.beta.chat.completions.parse(
                    model=config["model"],
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    response_format=response_model,
                    extra_headers=headers,
                )

                return response.choices[0].message.parsed

            # Groq fallback: prompt-based JSON
            schema = response_model.model_json_schema()

            response = client.chat.completions.create(
                model=config["model"],
                messages=[
                    {
                        "role": "system",
                        "content": (
                            system_prompt
                            + "\n\n"
                            + "Return ONLY valid JSON matching this schema:\n"
                            + json.dumps(schema, indent=2)
                        ),
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                extra_headers=headers,
            )

            text = response.choices[0].message.content.strip()

            try:
                return response_model.model_validate_json(text)

            except ValidationError:
                logfire.exception(
                    "Failed to parse Groq structured response."
                )
                raise
            
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        provider: str | None = None,
    ) -> str:

        provider = self._resolve_provider(provider)

        try:
            return self._generate_with_provider(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                provider=provider,
            )

        except Exception as e:

            config = self._get_provider_config(provider)

            logfire.exception(
                "LLM text generation failed",
                provider=provider,
                model=config["model"],
            )

            if provider == "gemini" and self._should_fallback(e):

                if (
                    not self.credentials.use_app_keys
                    and not self.credentials.groq_api_key
                ):
                    raise
                logfire.warning(
                    "Gemini failed. Falling back to Groq.",
                )

                try:
                    result = self._generate_with_provider(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        provider="groq",
                    )

                    logfire.info(
                        "Fallback to Groq succeeded.",
                    )

                    return result

                except Exception:

                    logfire.exception(
                        "Groq fallback also failed.",
                    )
                    raise

            raise

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        provider: str | None = None,
    ) -> T:

        provider = self._resolve_provider(provider)

        try:
            return self._generate_structured_with_provider(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_model=response_model,
                provider=provider,
            )

        except Exception as e:

            config = self._get_provider_config(provider)

            logfire.exception(
                "LLM structured generation failed",
                provider=provider,
                model=config["model"],
            )

            if provider == "gemini" and self._should_fallback(e):

                if (
                    not self.credentials.use_app_keys
                    and not self.credentials.groq_api_key
                ):
                    raise

                logfire.warning(
                    "Gemini failed. Falling back to Groq.",
                )

                try:
                    result = self._generate_structured_with_provider(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        response_model=response_model,
                        provider="groq",
                    )

                    logfire.info(
                        "Fallback to Groq succeeded.",
                    )

                    return result

                except Exception:

                    logfire.exception(
                        "Groq fallback also failed.",
                    )
                    raise

            raise
