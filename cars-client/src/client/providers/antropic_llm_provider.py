from typing import Any
import anthropic as antr

from interfaces.llm_interface import LLMInterface


class AnthropicProvider(LLMInterface):

    PRICING = {  # For Anthropic API
        "Claude-Opus-4": {"version": "claude-opus-4-20250514", "input": '0.15', "output": '0.75', "rate_limit": 50},
        "Claude-Sonnet-4": {"version": "claude-sonnet-4-20250514", "input": '0.03', "output": '0.15', "rate_limit": 50},
        "Claude-Sonnet-3.7": {"version": "claude-3-7-sonnet-20250219", "input": '0.03', "output": '0.15', "rate_limit": 50},
        "Claude-Haiku-3.5": {"version": "claude-3-5-haiku-20241022", "input": '0.03', "output": '0.15', "rate_limit": 50},
        "Claude-Sonnet-3.5-v2": {"version": "claude-3-5-sonnet-20241022", "input": '0.80', "output": '0.04', "rate_limit": 50},
        "Claude-Sonnet-3.5": {"version": "claude-3-5-sonnet-20240620", "input": '0.15', "output": '0.75', "rate_limit": 50},
        "Claude-Haiku-3": {"version": "claude-3-haiku-20240307", "input": '0.0025', "output": '0.0125', "rate_limit": 50},
    }

    model = None
    model_name = None
    input_tokens = 0
    output_tokens = 0

    def __init__(self, model_name: str):
        self.client = antr.Anthropic()
        self.set_model(model_name)

    def set_model(self, model_name: str):
        if (not self.PRICING.get(model_name)):
            raise Exception(
                f"Model name {model_name} not allowed or not exist.")

        self.model_name = model_name
        self.model = self.PRICING[model_name]

    def call(self, messages: list, max_tokens: int = 1000, tools: list = []) -> list[str, str]:
        """Calls the Anthropic API to generate content based on the provided messages.

        Args:
            messages (list): A list of message objects representing the conversation history.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1000.
            tools (list, optional): A list of tools that the model can use. Defaults to [].

        Returns:
            list[str, str]: The generated content from the Anthropic API.

        Raises:
            antr.BadRequestError: If the request is malformed or invalid (HTTP 400).
            antr.AuthenticationError: If authentication fails (HTTP 401).
            antr.PermissionDeniedError: If the API key lacks permission to perform the request (HTTP 403).
            antr.NotFoundError: If the requested resource is not found (HTTP 404).
            antr.RequestTooLargeError: If the request exceeds the maximum size (HTTP 413).
            antr.RateLimitError: If the rate limit is exceeded (HTTP 429).
            antr.OverloadedError: If the server is overloaded (HTTP 529).
            antr.APIConnectionError: If there is an error connecting to the API.
            antr.APIStatusError: If the API returns an HTTP error status code.
            antr.APIError: If a general API error occurs.
        """

        try:
            result = self.client.messages.create(
                model=self.model["version"],
                max_tokens=max_tokens,
                messages=messages,
                tools=tools
            )

            self.input_tokens = result.usage.input_tokens
            self.output_tokens = result.usage.output_tokens
            content = result.content

            return content
        # C.f. https://docs.anthropic.com/en/api/errors
        except antr.BadRequestError as e:
            raise antr.BadRequestError(f'400 - Bad request: {str(e)}')

        except antr.AuthenticationError as e:
            raise antr.AuthenticationError(
                f'401 - Authentication failed: {str(e)}')

        except antr.PermissionDeniedError as e:
            raise antr.PermissionDeniedError(
                f'403 - Permission denied: {str(e)}')

        except antr.NotFoundError as e:
            raise antr.NotFoundError(f'404 - Resource not found: {str(e)}')

        except antr.RequestTooLargeError as e:
            raise antr.RequestTooLargeError(
                f'413 - Request too large: {str(e)}')

        except antr.RateLimitError as e:
            raise antr.RateLimitError(f'429 - Rate limit exceeded: {str(e)}')

        except antr.OverloadedError as e:
            raise antr.OverloadedError(f'529 - Server overloaded: {str(e)}')

        except antr.APIConnectionError as e:
            raise antr.APIConnectionError(
                f'Connection error: {str(e.__cause__)}')

        except antr.APIStatusError as e:
            raise antr.APIStatusError(
                f'HTTP {e.status_code} error: {str(e.response)}')

        except antr.APIError as e:
            print("API error:", e)
            raise antr.APIError(f'API error: {str(e)}')

    def convert_tool_format(self, tool: Any) -> dict[str, Any]:
        """Converts a tool object to a dictionary format suitable for Anthropic's models."""
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        }
