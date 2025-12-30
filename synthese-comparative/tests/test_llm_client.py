import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.llm_client import LLMClient

class TestLLMClient(unittest.TestCase):

    def setUp(self):
        self.client = LLMClient(base_url="http://fake-url")

    def test_summarize_fake_short(self):
        text = "Short text"
        result = self.client._summarize_fake(text, max_chars=100)
        self.assertEqual(result, text)

    def test_summarize_fake_truncate(self):
        text = "Hello World"
        result = self.client._summarize_fake(text, max_chars=5)
        self.assertEqual(result, "World")

    @patch('core.llm_client.httpx.Client')
    def test_call_llm_qa_sync_success(self, mock_client_cls):
        # Setup mock
        mock_client_instance = mock_client_cls.return_value.__enter__.return_value
        mock_response = MagicMock()
        mock_response.json.return_value = {"summary": "Summarized text"}
        mock_client_instance.post.return_value = mock_response
        
        # Execute
        result = self.client._call_llm_qa_sync("Prompt")
        
        # Verify
        self.assertEqual(result, "Summarized text")
        mock_client_instance.post.assert_called_once()

    @patch('core.llm_client.LLMClient._call_llm_qa_sync')
    def test_summarize_remote_success(self, mock_call_sync):
        mock_call_sync.return_value = "Remote summary"
        
        # Force NOT fake mode logic is a bit tricky since it's hardcoded in config.py
        # We need to ensure we bypass valid checks if possible or just test the _call_llm_qa_sync directly as above.
        # But we can test _summarize_remote directly.
        
        result = self.client._summarize_remote("Prompt")
        self.assertEqual(result, "Remote summary")

    @patch('core.llm_client.LLMClient._call_llm_qa_sync')
    def test_summarize_remote_fallback(self, mock_call_sync):
        mock_call_sync.side_effect = Exception("Network error")
        
        # Should fallback to fake
        text = "This is a fallback text"
        # Since logic calls _summarize_fake(prompt, 1200) on error
        result = self.client._summarize_remote(text)
        self.assertEqual(result, text)

if __name__ == '__main__':
    unittest.main()
