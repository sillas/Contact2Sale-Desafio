import json
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from config.settings import logger


class MCPClient:

    def __init__(self, LLM_provider, messages):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm_provider = LLM_provider
        self.messages = messages

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py)
        """

        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        logger.log(
            f"\nConnected to server with tools: {[tool.name for tool in tools]}")
        logger.info("\nMCP Client Started!")

    async def process_query(self) -> str:
        """Process a query using Claude and available tools"""

        response = await self.session.list_tools()
        available_tools = [self.llm_provider.convert_tool_format(
            tool) for tool in response.tools]

        logger.log(f"available_tools: {json.dumps(available_tools, indent=2)}")

        # Initial Claude API call
        response = self.llm_provider.call(
            model=self.model_name,
            messages=self.messages.get(),
            tools=available_tools
        )

        final_text = []

        assistant_message_content = []
        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)

            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(
                    f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)
                self.messages.set(assistant_message_content)

                self.messages.set({
                    "type": "tool_result",
                    "tool_use_id": content.id,
                    "content": result.content
                },
                    role="user"
                )

                response = self.llm_provider.call(
                    model=self.model_name,
                    messages=self.messages.get(),
                    tools=available_tools
                )

                final_text.append(response.content[0].text)

        self.messages.set("\n".join(final_text))

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
