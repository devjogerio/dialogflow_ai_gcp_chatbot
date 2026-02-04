import json
import os
import shutil
import logging
from playwright.sync_api import sync_playwright

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AGENT_ZIP_PATH = "automation/dialogflow_agent.zip"
SCHEMA_DIR = "automation/dialogflow_schema"
TARGET_URL = "https://dialogflow.cloud.google.com/#/agent/nexus-ai-aws-v1-ahuj/intents"

def create_agent_zip():
    """Compacta a pasta do schema em um arquivo ZIP para importação."""
    logging.info("Criando arquivo ZIP do agente...")
    try:
        shutil.make_archive(AGENT_ZIP_PATH.replace('.zip', ''), 'zip', SCHEMA_DIR)
        logging.info(f"Arquivo ZIP criado em: {AGENT_ZIP_PATH}")
        return AGENT_ZIP_PATH
    except Exception as e:
        logging.error(f"Erro ao criar ZIP: {e}")
        raise

def deploy_agent_with_playwright(zip_path):
    """
    Automatiza o processo de importação do ZIP no console do Dialogflow.
    Nota: Requer login manual ou cookies persistentes para funcionar em produção.
    """
    logging.info("Iniciando automação com Playwright...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Headless False para visualização
        context = browser.new_context()
        page = context.new_page()

        try:
            logging.info(f"Navegando para {TARGET_URL}")
            page.goto(TARGET_URL)
            
            # Nota: O login do Google é complexo de automatizar devido a 2FA e captchas.
            # Em um cenário real, usaríamos a API do Google Cloud Dialogflow.
            # Este script assume que o usuário fará o login ou já existe uma sessão.
            
            logging.info("Aguardando login manual (se necessário)...")
            # Aqui você pode adicionar lógica para esperar um elemento específico do console carregado
            page.wait_for_selector('div[data-test-id="intent-list"]', timeout=60000)
            logging.info("Console carregado.")

            # Navegar para Configurações -> Export/Import
            logging.info("Navegando para Importação...")
            page.click('button[aria-label="Settings"]') # Exemplo de seletor
            page.click('text=Export and Import')

            # Upload do ZIP
            logging.info("Fazendo upload do arquivo ZIP...")
            with page.expect_file_chooser() as fc_info:
                page.click('button:has-text("Import from ZIP")')
            file_chooser = fc_info.value
            file_chooser.set_files(zip_path)

            # Confirmar Importação
            page.fill('input[placeholder="IMPORT"]', 'IMPORT') # Confirmação comum do Dialogflow
            page.click('button:has-text("Import")')
            
            logging.info("Importação iniciada. Aguardando conclusão...")
            page.wait_for_selector('text=Done', timeout=30000)
            logging.info("Importação concluída com sucesso!")

        except Exception as e:
            logging.error(f"Erro durante a automação: {e}")
            # Tira screenshot do erro
            page.screenshot(path="automation/error_screenshot.png")
        finally:
            browser.close()

if __name__ == "__main__":
    if not os.path.exists(SCHEMA_DIR):
        logging.error(f"Diretório de schema não encontrado: {SCHEMA_DIR}")
        exit(1)

    try:
        zip_file = create_agent_zip()
        print(f"Agente pronto para importação: {os.path.abspath(zip_file)}")
        print("Para rodar a automação de UI, execute este script em um ambiente com interface gráfica.")
        # deploy_agent_with_playwright(zip_file) # Comentado para não bloquear em headless server
    except Exception as e:
        logging.critical(f"Falha fatal: {e}")
