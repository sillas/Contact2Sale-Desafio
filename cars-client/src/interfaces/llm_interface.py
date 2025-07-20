from typing import Any
from abc import ABC, abstractmethod


class LLMInterface(ABC):

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, 'PRICING'):
            raise TypeError(
                f"{cls.__name__} is missing required class attribute 'PRICING'")

        if not hasattr(cls, 'input_tokens'):
            raise TypeError(
                f"{cls.__name__} is missing required class attribute 'input_tokens'")

        if not hasattr(cls, 'output_tokens'):
            raise TypeError(
                f"{cls.__name__} is missing required class attribute 'output_tokens'")

    @abstractmethod
    def set_model(self, new_model: str):
        pass

    @abstractmethod
    def call(self, model: str, messages: list, max_tokens: int = 1000, tools: list = []) -> Any:
        pass

    @abstractmethod
    def convert_tool_format(self, tool: Any) -> dict[str, Any]:
        pass
