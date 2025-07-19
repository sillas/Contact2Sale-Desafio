from typing import Any
from ..interfaces.llm_interface import LLMProvider

class LLM:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def call(self, model: str, messages: list, max_tokens: int = 1000, tools: list = []) -> Any:
        return self.provider.call(model, messages, max_tokens, tools)
    
    def convert_tool_format(self, tool: Any) -> dict[str, Any]:
        return self.provider.convert_tool_format(tool)
