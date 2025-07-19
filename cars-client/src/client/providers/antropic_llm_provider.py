from typing import Any
from anthropic import Anthropic

from interfaces.llm_interface import LLMProvider

class AnthropicProvider(LLMProvider):

    def __init__(self):
        self.client = Anthropic()

    def call(self, model: str, messages: list, max_tokens: int = 1000, tools: list = []) -> Any:
        return self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            tools=tools
        )
    
    def convert_tool_format(self, tool: Any) -> dict[str, Any]:
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        }