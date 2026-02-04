import unittest
import json
import os
import shutil
from automation.deploy_agent import create_agent_zip

class TestDialogflowSchema(unittest.TestCase):

    def setUp(self):
        self.schema_dir = "automation/dialogflow_schema"
        self.agent_file = os.path.join(self.schema_dir, "agent.json")

    def test_agent_json_exists(self):
        """Testa se o arquivo agent.json existe."""
        self.assertTrue(os.path.exists(self.agent_file), "agent.json deve existir")

    def test_agent_json_validity(self):
        """Testa se o agent.json é um JSON válido e tem campos obrigatórios."""
        with open(self.agent_file, 'r') as f:
            data = json.load(f)
        self.assertIn("googleAssistant", data)
        self.assertIn("defaultTimezone", data)
        self.assertEqual(data["defaultTimezone"], "America/Sao_Paulo")

    def test_intent_structure(self):
        """Testa se os arquivos de intent estão corretos."""
        intent_dir = os.path.join(self.schema_dir, "intents")
        for filename in os.listdir(intent_dir):
            if filename.endswith(".json") and "usersays" not in filename:
                with open(os.path.join(intent_dir, filename), 'r') as f:
                    data = json.load(f)
                self.assertIn("name", data, f"{filename} deve ter 'name'")
                self.assertIn("responses", data, f"{filename} deve ter 'responses'")

    def test_zip_creation(self):
        """Testa a criação do ZIP."""
        # Cria um zip de teste
        zip_path = create_agent_zip()
        self.assertTrue(os.path.exists(zip_path))
        # Limpeza
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == '__main__':
    unittest.main()
