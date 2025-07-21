import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal

from src.client.llm import LLM


class TestLLM(unittest.TestCase):
    def setUp(self):

        self.provider_instance = MagicMock()
        self.provider_instance.model = {
            'rate_limit': 60,
            'input': '100',
            'output': '200',
        }
        self.provider_instance.input_tokens = 10
        self.provider_instance.output_tokens = 20
        self.provider_instance.model_name = 'fake-model'
        self.provider_instance.call.return_value = ["resposta", "id"]
        self.provider_instance.set_model.return_value = 'novo-modelo'
        self.provider_instance.convert_tool_format.side_effect = lambda x: {
            "converted": x}

        self.mock_provider_class = MagicMock(
            return_value=self.provider_instance)

    def test_calculate_cost(self):
        llm = LLM(self.mock_provider_class)
        cost = llm.calculate_cost()
        expected = (Decimal('0.01') * 10) + (Decimal('0.02') * 20)
        self.assertEqual(cost, expected)
        self.assertEqual(llm.total_cost, expected)

    def test_set_model(self):
        llm = LLM(self.mock_provider_class)
        result = llm.set_model('novo-modelo')
        self.assertEqual(result, 'novo-modelo')
        self.provider_instance.set_model.assert_called_with('novo-modelo')

    @patch('src.client.llm.time')
    def test_handle_rate_limit(self, mock_time):
        llm = LLM(self.mock_provider_class)
        llm.last_call_timestamp_in_ms = 0
        llm.min_interval_ms = 1000

        mock_time.time.side_effect = [0.5, 1.5]  # força o sleep

        with patch('src.client.llm.time.sleep') as mock_sleep:
            llm._handle_rate_limit()
            mock_sleep.assert_called_once()
            self.assertGreater(llm.last_call_timestamp_in_ms, 0)

    def test_call_success(self):
        llm = LLM(self.mock_provider_class)
        result = llm.call([{"role": "user", "content": "Hello"}])
        self.assertEqual(result, ["resposta", "id"])
        self.provider_instance.call.assert_called_once()

    def test_convert_tool_format(self):
        llm = LLM(self.mock_provider_class)
        result = llm.convert_tool_format({'name': 'tool'})
        self.assertEqual(result, {'converted': {'name': 'tool'}})


if __name__ == '__main__':
    unittest.main()
