import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anonymizer import process_text_anonymization

class TestAnonymizer(unittest.TestCase):

    @patch('anonymizer.analyzer')
    @patch('anonymizer.anonymizer')
    def test_process_text_anonymization(self, mock_anonymizer_engine, mock_analyzer_engine):
        # Setup mocks
        mock_results = [MagicMock()] 
        mock_analyzer_engine.analyze.return_value = mock_results
        
        mock_anonymized_result = MagicMock()
        mock_anonymized_result.text = "My name is <PERSON>."
        mock_anonymizer_engine.anonymize.return_value = mock_anonymized_result

        # Test input
        text = "My name is John Doe."
        
        # Execute
        result = process_text_anonymization(text)

        # Verify
        mock_analyzer_engine.analyze.assert_called_once()
        mock_anonymizer_engine.anonymize.assert_called_once_with(text=text, analyzer_results=mock_results)
        self.assertEqual(result, "My name is <PERSON>.")

    def test_process_text_anonymization_empty(self):
        result = process_text_anonymization("")
        self.assertEqual(result, "")

    def test_process_text_anonymization_none(self):
        result = process_text_anonymization(None)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
