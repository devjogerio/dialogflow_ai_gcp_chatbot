import os
import sys
import argparse
from dotenv import load_dotenv

# Adiciona o diretório raiz do projeto ao sys.path para permitir a resolução do pacote 'dialogflow_automation'
# Isso deve ser feito ANTES de importar os módulos internos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dialogflow_automation.core.logger import setup_logger
from dialogflow_automation.core.parser import ConfigParser
from dialogflow_automation.core.client import DialogflowClient

# Inicializa o logger principal da aplicação
logger = setup_logger("main")

def main():
    """
    Função principal de entrada (Entry Point).
    Gerencia o fluxo de execução da ferramenta de automação.
    """
    # Carrega variáveis de ambiente do arquivo .env na raiz do projeto
    # Isso é essencial para obter credenciais sem hardcode
    load_dotenv()

    # Configuração do parser de argumentos da linha de comando (CLI)
    parser = argparse.ArgumentParser(description="Automação de Setup do Dialogflow ES")
    parser.add_argument(
        "--config-dir", 
        type=str, 
        default="dialogflow_automation/config",
        help="Caminho para o diretório de configurações (JSONs)"
    )
    parser.add_argument(
        "--project-id", 
        type=str, 
        help="ID do Projeto no Google Cloud (sobrescreve env var DIALOGFLOW_PROJECT_ID)"
    )
    parser.add_argument(
        "--credentials", 
        type=str, 
        help="Caminho para o JSON da Service Account (sobrescreve env var GOOGLE_APPLICATION_CREDENTIALS)"
    )
    
    args = parser.parse_args()

    logger.info("Iniciando processo de automação do Dialogflow...")

    # --- 1. Validação de Credenciais e Parâmetros ---
    
    # Obtém Project ID (Argumento > ENV > Erro)
    project_id = args.project_id or os.getenv("DIALOGFLOW_PROJECT_ID")
    if not project_id:
        logger.error("Project ID não fornecido via argumento ou variável de ambiente DIALOGFLOW_PROJECT_ID.")
        sys.exit(1)

    # Obtém Caminho das Credenciais (Argumento > ENV > Erro)
    credentials_path = args.credentials or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        logger.error("Caminho das credenciais não fornecido. Defina GOOGLE_APPLICATION_CREDENTIALS ou use --credentials.")
        sys.exit(1)

    if not os.path.exists(credentials_path):
        logger.error(f"Arquivo de credenciais não encontrado no caminho: {credentials_path}")
        sys.exit(1)

    # --- 2. Inicialização dos Componentes ---

    try:
        # Inicializa o parser de configuração
        config_parser = ConfigParser(args.config_dir)
        
        # Inicializa o cliente do Dialogflow
        df_client = DialogflowClient(project_id, credentials_path)
        
    except Exception as e:
        logger.critical(f"Falha na inicialização dos componentes: {e}")
        sys.exit(1)

    # --- 3. Execução da Automação (Sync) ---

    try:
        # Carrega a definição de intenções do arquivo JSON
        # O parser valida a estrutura do JSON antes de retornar
        intents_list = config_parser.load_intents()
        
        # Simulação de carregamento de Entidades (poderia vir de entities.json)
        # Aqui definimos hardcoded para exemplo, mas deveria estar em config/
        entities_config = [
            {
                "display_name": "TipoServico",
                "kind": "KIND_MAP",
                "entities": [
                    {"value": "Consultoria Padrão", "synonyms": ["padrão", "básica", "standard"]},
                    {"value": "Consultoria Premium", "synonyms": ["premium", "completa", "avançada"]}
                ]
            }
        ]

        logger.info("Iniciando criação de Entidades...")
        for ent in entities_config:
            df_client.create_entity_type(ent['display_name'], ent['kind'], ent['entities'])
        
        logger.info(f"Iniciando sincronização de {len(intents_list)} intenções...")

        # Itera sobre cada intenção definida e cria no Dialogflow
        for intent_data in intents_list:
            df_client.create_intent(
                display_name=intent_data['display_name'],
                training_phrases_parts=intent_data['training_phrases'],
                message_texts=intent_data['messages'],
                parameters=intent_data.get('parameters'),
                input_context_names=intent_data.get('input_context_names'),
                output_contexts=intent_data.get('output_contexts')
            )
            
        logger.info("Processo de sincronização concluído com sucesso! 🚀")
        logger.info("Verifique o agente no console: https://dialogflow.cloud.google.com/#/agent/nexus-ai-aws-v1-ahuj/intents")

    except Exception as e:
        logger.error(f"Erro durante o processo de execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
