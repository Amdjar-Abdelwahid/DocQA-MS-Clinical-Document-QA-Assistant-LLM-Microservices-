import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processing import extract_text_from_file, publish_to_queue

class TestProcessing(unittest.TestCase):

    @patch('processing.parser')
    def test_extract_text_from_file_success(self, mock_parser):
        # Setup mock
        mock_parser.from_file.return_value = {"content": "\n  Extracted Text  \n"}
        
        # Execute
        result = extract_text_from_file("dummy/path.pdf")
        
        # Verify
        mock_parser.from_file.assert_called_once()
        self.assertEqual(result, "Extracted Text")

    @patch('processing.parser')
    def test_extract_text_from_file_failure(self, mock_parser):
        # Setup mock to raise exception
        mock_parser.from_file.side_effect = Exception("Tika error")
        
        # Execute
        result = extract_text_from_file("dummy/path.pdf")
        
        # Verify
        self.assertIsNone(result)

    @patch('processing.pika')
    def test_publish_to_queue(self, mock_pika):
        # Setup mocks
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_pika.BlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        
        doc_id = 123
        text = "Sample text"
        metadata = {"type": "report"}
        
        # Execute
        publish_to_queue(doc_id, text, metadata)
        
        # Verify
        mock_pika.BlockingConnection.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue='raw_documents_queue', durable=True)
        
        expected_body = json.dumps({
            "doc_id": doc_id,
            "text": text,
            "metadata": metadata
        })
        
        mock_channel.basic_publish.assert_called_once()
        args, kwargs = mock_channel.basic_publish.call_args
        self.assertEqual(kwargs['routing_key'], 'raw_documents_queue')
        self.assertEqual(kwargs['body'], expected_body)
        
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
