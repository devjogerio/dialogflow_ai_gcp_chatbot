import sys
from unittest.mock import MagicMock

# MOCK AGRESSIVO DE DEPENDÊNCIAS DO GOOGLE
# Necessário porque o ambiente Python 3.14 tem problemas com protobuf/google-cloud
mock_google = MagicMock()
mock_dialogflow = MagicMock()
mock_api_core = MagicMock()
mock_protobuf = MagicMock()

sys.modules["google"] = mock_google
sys.modules["google.cloud"] = MagicMock()
sys.modules["google.cloud.dialogflow_v2"] = mock_dialogflow
sys.modules["google.api_core"] = mock_api_core
sys.modules["google.protobuf"] = mock_protobuf
sys.modules["google.protobuf.internal"] = MagicMock()
sys.modules["google.rpc"] = MagicMock()

# Agora podemos importar o resto
from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, mock_open
import os
import json

class SyncDialogflowCommandTest(TestCase):
    def setUp(self):
        # Configura variáveis de ambiente necessárias para o teste
        self.env_patcher = patch.dict(os.environ, {
            'DIALOGFLOW_PROJECT_ID': 'test-project',
            'GOOGLE_APPLICATION_CREDENTIALS': '/tmp/fake-creds.json'
        })
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @patch('core.management.commands.sync_dialogflow.DialogflowClient')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "entities": [
            {
                "display_name": "TestEntity",
                "kind": "KIND_MAP",
                "entities": [{"value": "v1", "synonyms": ["s1"]}]
            }
        ],
        "intents": [
            {
                "display_name": "TestIntent",
                "training_phrases": ["Hello"],
                "messages": ["Hi"],
                "parameters": []
            }
        ]
    }))
    @patch('pathlib.Path.exists', return_value=True)
    def test_sync_dialogflow_success(self, mock_exists, mock_file, MockDialogflowClient):
        """Teste de sucesso na execução do comando sync_dialogflow com JSON mockado"""
        # Configura o mock do cliente
        mock_client_instance = MockDialogflowClient.return_value
        
        # Executa o comando
        from io import StringIO
        out = StringIO()
        call_command('sync_dialogflow', stdout=out)
        
        # Verifica se o cliente foi inicializado corretamente
        MockDialogflowClient.assert_called_with('test-project', '/tmp/fake-creds.json')
        
        # Verifica se create_entity_type foi chamado
        mock_client_instance.create_entity_type.assert_called_once()
        _, kwargs = mock_client_instance.create_entity_type.call_args
        self.assertEqual(kwargs['display_name'], "TestEntity")

        # Verifica se create_intent foi chamado
        mock_client_instance.create_intent.assert_called_once()
        
        # Verifica a saída
        output = out.getvalue()
        self.assertIn('Sincronização concluída com sucesso!', output)

    @patch('core.management.commands.sync_dialogflow.DialogflowClient')
    @patch('pathlib.Path.exists', return_value=False)
    def test_sync_dialogflow_file_not_found(self, mock_exists, MockDialogflowClient):
        """Teste quando o arquivo JSON não é encontrado"""
        from io import StringIO
        out = StringIO()
        call_command('sync_dialogflow', stdout=out)
        
        output = out.getvalue()
        self.assertIn('Arquivo de configuração não encontrado', output)

    @patch('core.management.commands.sync_dialogflow.DialogflowClient')
    @patch.dict(os.environ, {}, clear=True)
    def test_sync_dialogflow_missing_env(self, MockDialogflowClient):
        """Teste quando variáveis de ambiente estão faltando"""
        with patch.dict(os.environ):
            from io import StringIO
            out = StringIO()
            call_command('sync_dialogflow', stdout=out)
            
            output = out.getvalue()
            self.assertIn('devem estar definidos no .env', output)
