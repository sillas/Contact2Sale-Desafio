from typing import Any
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    
    @abstractmethod
    def call(self, model: str, messages: list, max_tokens: int = 1000, tools: list = []) -> Any:
        pass

    @abstractmethod
    def convert_tool_format(self, tool: Any) -> dict[str, Any]:
        pass