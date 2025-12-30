import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to mock SentenceTransformer BEFORE generated import in indexer.py because it loads the model at top level
# However, indexer.py is a script, not a module with easy functions to isolate without running global code.
# The `indexer.py` has global execution code at the bottom (if __name__ == '__main__': ...), but also global variables initialized at top.
# Ideally we would refactor indexer.py, but we can't touch source code.
# We will use patch.dict or similar to mock os.environ and try to patch the model loader.
# Actually, `indexer.py` instantiates `model = SentenceTransformer(...)` at the module level.
# To test `add_to_index`, we need to import it. Importing it will trigger the model load.
# We can mock `sentence_transformers.SentenceTransformer` in `sys.modules` before importing `indexer`.

sys.modules['sentence_transformers'] = MagicMock()
sys.modules['faiss'] = MagicMock()

# Now import the module under test
import indexer

class TestIndexer(unittest.TestCase):

    def setUp(self):
        # Reset global variables in indexer module for each test
        indexer.index = None
        indexer.metadata_store = []
        # Mock the model instance already created in indexer
        indexer.model = MagicMock()

    def test_add_to_index(self):
        # Setup
        text = "Test sentence"
        source = "test_source.txt"
        fake_embedding = [0.1, 0.2, 0.3]
        indexer.model.encode.return_value = fake_embedding
        
        mock_faiss_index = MagicMock()
        indexer.faiss.IndexFlatL2.return_value = mock_faiss_index
        
        # Execute
        indexer.add_to_index(text, source)
        
        # Verify
        indexer.model.encode.assert_called_with([text])
        indexer.faiss.IndexFlatL2.assert_called_once() # Should be called to create index
        mock_faiss_index.add.assert_called_once()
        
        # Verify metadata
        self.assertEqual(len(indexer.metadata_store), 1)
        self.assertEqual(indexer.metadata_store[0]['text_content'], text)
        self.assertEqual(indexer.metadata_store[0]['source'], source)

    def test_add_to_index_empty(self):
        indexer.add_to_index("   ", "source")
        self.assertEqual(len(indexer.metadata_store), 0)

if __name__ == '__main__':
    unittest.main()
