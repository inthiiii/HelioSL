from pydantic import BaseModel


class LLMRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None


class LLMResponse(BaseModel):
    content: str
    provider: str
    model: str