import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from src.client.strings.messages import welcome_message
from src.client.chat_handler import Chat


class TestChat(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_mcp_client = MagicMock()
        self.mock_mcp_client.process_query = AsyncMock()

        self.mock_messages = MagicMock()
        self.chat = Chat(self.mock_mcp_client, self.mock_messages)

    @patch("builtins.input", side_effect=['q'])
    @patch("src.client.chat_handler.logger")
    async def test_quit_immediately(self, mock_logger, mock_input):
        await self.chat.loop()
        self.mock_messages.set.assert_called_once_with(welcome_message)
        mock_logger.info.assert_any_call(welcome_message)
        mock_logger.info.assert_any_call("Até breve")

    @patch("builtins.input", side_effect=['   ', 'q'])
    @patch("src.client.chat_handler.logger")
    async def test_empty_query(self, mock_logger, mock_input):
        await self.chat.loop()
        self.assertIn(
            unittest.mock.call("Ops! o que quis dizer?"),
            mock_logger.info.call_args_list
        )

    @patch("builtins.input", side_effect=['olá', 'q'])
    @patch("src.client.chat_handler.logger")
    async def test_valid_query(self, mock_logger, mock_input):
        await self.chat.loop()
        self.mock_messages.set.assert_any_call("olá", role="user")
        self.mock_mcp_client.process_query.assert_awaited()
        self.assertTrue(any("R:-------------------------------------" in str(c)
                        for c in mock_logger.info.call_args_list))
