import os
import sys
import tempfile
import unittest
from unittest import mock


class TestCreatePDF(unittest.TestCase):

    def setUp(self):

        mock_pymongo = mock.MagicMock()
        mock_pymongo.ASCENDING = 1
        mock_pymongo.DESCENDING = -1
        mock_pymongo.errors.OperationFailure = Exception
        mock_pymongo.errors.InvalidOperation = Exception
        mock_pymongo.errors.ConnectionFailure = Exception

        sys.modules['pymongo'] = mock_pymongo
        sys.modules['pymongo.errors'] = mock_pymongo.errors

        from src.car_repository import create_pdf
        self.create_pdf = create_pdf

        self.temp_dir = tempfile.TemporaryDirectory()
        self.title = "Test PDF"
        self.content = "This is a test content."

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_pdf_success(self):
        message = self.create_pdf(self.title, self.content, self.temp_dir.name)

        expected_filename = "Test_PDF.pdf"
        expected_path = os.path.join(self.temp_dir.name, expected_filename)

        self.assertTrue(os.path.exists(expected_path))
        self.assertIn("Saved to", message)
        self.assertIn(expected_filename, message)

        # Só por garantia!
        os.remove(expected_path)
        self.assertFalse(os.path.exists(expected_path))

    @mock.patch("src.car_repository.FPDF.output")
    def test_create_pdf_failure(self, mock_output):
        mock_output.side_effect = Exception("Save failed")

        with self.assertLogs("src.config.logger", level="ERROR") as log:
            result = self.create_pdf(
                self.title, self.content, self.temp_dir.name)

        self.assertIn("Falha ao salvar em PDF", result)
        self.assertIn("Save failed", result)
        self.assertTrue(any("ERROR" in record for record in log.output))


if __name__ == '__main__':
    unittest.main()
