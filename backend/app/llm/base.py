from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> bool:
        raise NotImplementedError