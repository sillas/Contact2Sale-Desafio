from typing import Any


class Message:
    def __init__(self, prompt: str = None):
        self.messages = []

        if (prompt):
            self.messages.append({
                "role": "user",
                "content": prompt
            })

    def set(self, message: str, role: str = "assistant"):
        self.messages.append({
            "role": role,
            "content": message
        })

    def get(self) -> list[dict[str, Any]]:
        return self.messages

    def __str__(self) -> str:
        return self.messages[-1]["content"]
