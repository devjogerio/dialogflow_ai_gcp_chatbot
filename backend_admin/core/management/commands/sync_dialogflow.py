import os
import sys
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

# Tenta importar o cliente do Dialogflow.
try:
    from dialogflow_automation.core.client import DialogflowClient
except ImportError:
    DialogflowClient = None


class Command(BaseCommand):
    help = 'Sincroniza intenções e entidades com o Dialogflow a partir do arquivo JSON'

    def handle(self, *args, **options):
        # Verifica se o módulo foi importado corretamente
        if DialogflowClient is None:
            self.stdout.write(self.style.ERROR(
                'Módulo dialogflow_automation não encontrado ou dependências ausentes.\n'
                'Certifique-se de que o pacote google-cloud-dialogflow está instalado.'
            ))
            return

        # Obtém credenciais do ambiente
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        # Valida configuração
        if not project_id or not credentials_path:
            self.stdout.write(self.style.ERROR(
                'Erro: DIALOGFLOW_PROJECT_ID e GOOGLE_APPLICATION_CREDENTIALS devem estar definidos no .env'
            ))
            return

        self.stdout.write(
            f'Inicializando Cliente Dialogflow para o projeto: {project_id}...')

        try:
            # Inicializa o cliente
            client = DialogflowClient(project_id, credentials_path)

            # Caminho para o arquivo intents.json
            # Assume que a estrutura de pastas é fixa
            # BASE_DIR do Django é nexus_ai_gcp/backend_admin/nexus_admin/..
            # O arquivo está em nexus_ai_gcp/dialogflow_automation/config/intents.json

            # Obtemos o caminho do arquivo atual para navegar
            current_file = Path(__file__).resolve()
            # backend_admin/core/management/commands/sync_dialogflow.py -> backend_admin -> nexus_ai_gcp
            project_root = current_file.parent.parent.parent.parent.parent
            config_path = project_root / "dialogflow_automation" / "config" / "intents.json"

            if not config_path.exists():
                self.stdout.write(self.style.ERROR(
                    f'Arquivo de configuração não encontrado em: {config_path}'))
                return

            self.stdout.write(f'Lendo configuração de: {config_path}')

            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. Sincronizar Entidades
            entities_data = data.get('entities', [])
            if entities_data:
                self.stdout.write(
                    f'Encontradas {len(entities_data)} entidades para sincronizar.')
                for ent in entities_data:
                    self.stdout.write(
                        f'  - Sincronizando entidade: {ent["display_name"]}')
                    client.create_entity_type(
                        display_name=ent['display_name'],
                        kind=ent['kind'],
                        entities=ent['entities']
                    )

            # 2. Sincronizar Intenções
            intents_data = data.get('intents', [])
            if intents_data:
                self.stdout.write(
                    f'Encontradas {len(intents_data)} intenções para sincronizar.')
                for intent_data in intents_data:
                    self.stdout.write(
                        f'  - Sincronizando intenção: {intent_data["display_name"]}')
                    client.create_intent(
                        display_name=intent_data['display_name'],
                        training_phrases_parts=intent_data['training_phrases'],
                        message_texts=intent_data['messages'],
                        parameters=intent_data.get('parameters', [])
                    )

            self.stdout.write(self.style.SUCCESS(
                'Sincronização concluída com sucesso!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Erro ao sincronizar Dialogflow: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
