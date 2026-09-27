import httpx

from app.core.config import settings
from app.llm.base import LLMProvider


class OllamaClient(LLMProvider):

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = httpx.post(
            f"{settings.ollama_base_url}/api/chat",
            json={
                "model": settings.llm_model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": settings.llm_temperature,
                },
            },
            timeout=settings.llm_timeout_seconds,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]


    def health(self) -> bool:
        try:
            response = httpx.get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=5,
            )

            return response.status_code == 200

        except httpx.HTTPError:
            return False


def get_llm_client() -> LLMProvider:
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        return OllamaClient()

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )