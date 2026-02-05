import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock google.cloud.dialogflow_v2 and google.api_core before importing client
# This prevents import errors on environments with incompatible protobuf/python versions
mock_dialogflow_module = MagicMock()
mock_api_core = MagicMock()
mock_exceptions = MagicMock()

sys.modules["google.cloud"] = MagicMock()
sys.modules["google.cloud.dialogflow_v2"] = mock_dialogflow_module
sys.modules["google.api_core"] = mock_api_core
sys.modules["google.api_core.exceptions"] = mock_exceptions

# Define exceptions on the mock so client.py can import them
mock_exceptions.AlreadyExists = Exception
mock_exceptions.GoogleAPICallError = Exception
mock_exceptions.NotFound = Exception

# NOW we can import the client
from dialogflow_automation.core.client import DialogflowClient

class TestDialogflowClient(unittest.TestCase):
    def setUp(self):
        self.project_id = "test-project"
        self.service_account_path = "/path/to/credentials.json"
        
        # We don't need to patch 'dialogflow_automation.core.client.dialogflow' anymore
        # because we mocked the module globally.
        # But we need to ensure the client uses our mock
        self.mock_dialogflow = mock_dialogflow_module
        
        # Initialize client
        self.client = DialogflowClient(self.project_id, self.service_account_path)

    def tearDown(self):
        pass

    def test_init(self):
        """Test initialization of DialogflowClient"""
        self.assertEqual(self.client.project_id, self.project_id)
        self.assertEqual(self.client.parent, f"projects/{self.project_id}/agent")
        
        # Check if clients were initialized
        self.assertTrue(hasattr(self.client, 'intents_client'))
        self.assertTrue(hasattr(self.client, 'entity_types_client'))
        self.assertTrue(hasattr(self.client, 'agents_client'))

    def test_create_intent_new(self):
        """Test creating a new intent"""
        # Mock _get_intent_by_display_name to return None (intent doesn't exist)
        self.client._get_intent_by_display_name = MagicMock(return_value=None)
        
        # Mock create_intent response
        mock_intent = MagicMock()
        mock_intent.name = "projects/test-project/agent/intents/123"
        mock_intent.display_name = "TestIntent"
        self.client.intents_client.create_intent.return_value = mock_intent
        
        # Call method
        result = self.client.create_intent(
            display_name="TestIntent",
            training_phrases_parts=["Hello"],
            message_texts=["Hi there"]
        )
        
        # Verify result
        self.assertEqual(result, mock_intent)
        self.client.intents_client.create_intent.assert_called_once()

    def test_create_intent_existing(self):
        """Test creating an intent that already exists (idempotency)"""
        # Mock existing intent
        existing_intent = MagicMock()
        existing_intent.display_name = "TestIntent"
        self.client._get_intent_by_display_name = MagicMock(return_value=existing_intent)
        
        # Call method
        result = self.client.create_intent(
            display_name="TestIntent",
            training_phrases_parts=["Hello"],
            message_texts=["Hi there"]
        )
        
        # Verify it returns existing intent and DOES NOT call create_intent
        self.assertEqual(result, existing_intent)
        self.client.intents_client.create_intent.assert_not_called()

if __name__ == '__main__':
    unittest.main()
