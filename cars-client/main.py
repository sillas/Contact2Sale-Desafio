import asyncio

from src.client.mcp_client import MCPClient
from src.client.providers.antropic_llm_provider import AnthropicProvider
from src.client.llm import LLM
from src.client.chat_handler import Chat
from src.client.message import Message

from src.client.strings.prompts import main_prompt


async def main():

    llm = LLM(AnthropicProvider)
    messages = Message(main_prompt)
    mcp_client = MCPClient(llm, messages)
    chat = Chat(mcp_client, messages)

    try:
        await mcp_client.connect_to_server()
        await chat.loop()
    finally:
        await mcp_client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

# uv run src/main.py ../cars/cars.py
