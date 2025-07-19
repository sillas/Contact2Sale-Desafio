import asyncio

from client.mcp_client import MCPClient
from client.providers.antropic_llm_provider import AnthropicProvider
from client.chat_handler import Chat
from client.message import Message

from config.settings import logger
from client.strings.prompts import main_prompt


async def main():

    if len(sys.argv) < 2:
        logger.info("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    llm_provider = AnthropicProvider()
    messages = Message(main_prompt)
    mcp_client = MCPClient(llm_provider, messages)
    chat = Chat(mcp_client, messages)

    try:
        await mcp_client.connect_to_server(sys.argv[1])
        await chat.loop()
    finally:
        await mcp_client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())

# uv run src/main.py ../cars/cars.py
