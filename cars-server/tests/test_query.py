import unittest
# from unittest.mock import patch
# import asyncio
from src.utils import query_transform


class ValidationError(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)


class TestGetCars(unittest.TestCase):
    pass

    # def setUp(self):
    #     self.loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(self.loop)

    # def tearDown(self):
    #     self.loop.close()

    # def test_query_transform_success(self):
    #     query = '{\\\'year\\\': 2025}'
    #     result = query_transform(query)
    #     self.assertDictEqual(result, {"year": 2025})

    # def test_query_transform_success(self):
    #     query = "{\\\"color\\\": {\\\"$exists\\\": true}}"
    #     result = query_transform(query)
    #     self.assertDictEqual(result, {"color": {"$exists": True}})

    # @patch('main.query_cars')
    # def test_get_cars_valid_query(self, mock_query_cars):
    #     mock_query_cars.return_value = {}
    #     query = '{\"year\": 2025}'
    #     self.loop.run_until_complete(get_cars(query))
    #     mock_query_cars.assert_called_once_with({"year": 2025})

    # def test_get_cars_invalid_query(self):
    #     query = '{invalid_json}'
    #     with self.assertRaises(ValidationError) as context:
    #         self.loop.run_until_complete(get_cars(query))
    #     self.assertEqual(context.exception.status_code, 400)


if __name__ == '__main__':
    unittest.main()
