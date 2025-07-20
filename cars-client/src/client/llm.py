from os import getenv
from time import time
from typing import Any
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass

from src.interfaces.llm_interface import LLMProvider
from src.config.settings import logger


@dataclass
class CallRecord:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: Decimal
    total_cost: Decimal


class LLM:
    """
    A class for interacting with Large Language Models (LLMs) through a specified provider.

    This class handles model selection, rate limiting, cost calculation, and call history logging.
    It acts as an intermediary between the user and the LLM provider, providing a consistent
    interface for making requests and managing the responses.

    Attributes:
        provider (LLMProvider): An instance of the LLMProvider class, responsible for interacting
            with the specific LLM being used.
        total_cost (Decimal): The cumulative cost of all LLM calls made through this instance.
        calls_history (list[CallRecord]): A list of dictionaries, where each dictionary contains
            information about a single LLM call, such as timestamp, model used, input/output tokens,
            cost, and total cost at that mooment.
        rate_limit (int): The maximum number of calls allowed per minute, as defined by the provider's model.
        min_interval_ms (int): The minimum time interval (in milliseconds) that must elapse between
            successive LLM calls to respect the rate limit.
        last_call_timestamp_in_ms (int): The timestamp (in milliseconds) of the most recent LLM call.
        """

    def __init__(self, provider: LLMProvider):
        self.provider = provider(getenv('LLM_MODEL_NAME'))
        self.total_cost = Decimal('0')
        self.calls_history: list[CallRecord] = []

        # calls per minute
        self.rate_limit: int = self.provider.model['rate_limit']
        self.min_interval_ms = 60_000 / self.rate_limit
        self.last_call_timestamp_in_ms = 0

    def set_model(self, new_model_name: str):
        """Update model name"""
        return self.provider.set_model(new_model_name)

    def _current_time_ms(self) -> int:
        return int(time.time() * 1000)

    def _handle_rate_limit(self) -> None:
        """Handles rate limiting by pausing execution if necessary to respect the minimum interval between calls."""
        now = self._current_time_ms()
        elapsed = now - self.last_call_timestamp_in_ms

        if elapsed < self.min_interval_ms:
            sleep_time_ms = self.min_interval_ms - elapsed
            time.sleep(sleep_time_ms / 1000)
            now = self._current_time_ms()

        self.last_call_timestamp_in_ms = now

    def call(self, messages: list, max_tokens: int = 1000, tools: list = []) -> list[str, str]:
        """
        Call method with logging, rate limiting
        """
        self._handle_rate_limit()

        try:
            response = self.provider.call(messages, max_tokens, tools)

            cost = self.calculate_cost()
            input_tokens = self.provider.input_tokens
            output_tokens = self.provider.output_tokens

            call_record = {
                "timestamp": datetime.now().isoformat(),
                "model": self.provider.model_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "total_cost": self.total_cost
            }
            self.calls_history.append(call_record)

            logger.info(
                f"LLM Call: {input_tokens} input tokens, {output_tokens} output tokens. "
                f"Cost: ${cost:.4f}. Total acumulado: ${self.total_cost:.4f}"
            )

            return response

        except Exception as e:
            logger.exception(f"LLM-Call Error: {str(e)}", exc_info=e)

    def convert_tool_format(self, tool: Any) -> dict[str, Any]:
        """Convert tool format"""
        return self.provider.convert_tool_format(tool)

    def calculate_cost(self) -> Decimal:
        """Calculates the total cost and the cost of each call."""
        # Get prices multiplied by 10.000
        raw_input_price = Decimal(self.provider.PRICING[self.model]['input'])
        raw_output_price = Decimal(self.provider.PRICING[self.model]['output'])

        # Normalize prices
        input_price: Decimal = raw_input_price / Decimal('10000')
        output_price: Decimal = raw_output_price / Decimal('10000')

        input_tokens: int = self.provider.input_tokens
        output_tokens: int = self.provider.output_tokens

        total = (input_tokens * input_price) + (output_tokens * output_price)

        self.total_cost += total

        return total
