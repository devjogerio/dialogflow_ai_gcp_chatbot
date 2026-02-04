# Importações necessárias para interagir com a API do Vertex AI e Discovery Engine
import os
import requests
import json
import logging
# Importação das bibliotecas do Google Cloud para Search e Generative AI
from google.cloud import discoveryengine_v1 as discoveryengine
import vertexai
from vertexai.generative_models import GenerativeModel

# Configuração de variáveis de ambiente
# Estas variáveis devem ser definidas no ambiente de execução (Cloud Functions)
# PROJECT_ID: ID do projeto no Google Cloud
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "nexus-ai-project")
# LOCATION: Região onde os recursos estão alocados (ex: us-central1)
LOCATION = os.environ.get("GCP_LOCATION", "global")
# DATA_STORE_ID: ID do Data Store criado no Vertex AI Search & Conversation
DATA_STORE_ID = os.environ.get("DATA_STORE_ID", "nexus-docs-store")
# DJANGO_API_URL: URL do backend Django para criação de tickets
DJANGO_API_URL = os.environ.get(
    "DJANGO_API_URL", "https://api.nexus-ai.com/api/tickets/")

# Inicialização do Vertex AI SDK
# Prepara o ambiente para chamadas aos modelos Gemini
vertexai.init(project=PROJECT_ID, location="us-central1")


def process_rag_query(user_query):
    """
    Executa o fluxo RAG (Retrieval-Augmented Generation).
    1. Busca documentos relevantes no Vertex AI Search (Data Store).
    2. Envia o contexto encontrado + pergunta do usuário para o Gemini 1.5.
    3. Retorna a resposta gerada.
    """

    # Passo 1: Busca (Retrieval)
    # Inicializa o cliente de busca do Discovery Engine
    client = discoveryengine.SearchServiceClient()

    # Constrói o caminho completo do recurso de configuração de serviço (serving config)
    # O padrão geralmente é 'default_config'
    serving_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=DATA_STORE_ID,
        serving_config="default_config",
    )

    # Configura a requisição de busca
    # query: A pergunta original do usuário
    # page_size: Número de trechos (snippets) a recuperar (5 é um bom equilíbrio)
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=user_query,
        page_size=5,
    )

    try:
        # Executa a busca no índice vetorial
        response = client.search(request)

        # Processa os resultados para extrair o texto relevante
        context_text = ""
        for result in response.results:
            # Extrai os dados do documento (assumindo documentos não estruturados/PDFs)
            # O campo 'derivedStructData' geralmente contém os snippets extraídos
            data = result.document.derived_struct_data
            if 'snippets' in data:
                for snippet in data['snippets']:
                    context_text += snippet.get('snippet', '') + "\n"

        # Caso nenhum contexto seja encontrado, retorna uma mensagem de fallback
        if not context_text:
            return "Desculpe, não encontrei informações suficientes na minha base de conhecimento para responder isso."

    except Exception as e:
        # Loga erros de busca (ex: problemas de permissão ou configuração)
        logging.error(f"Erro ao buscar no Vertex AI Search: {e}")
        return "Ocorreu um erro ao consultar a base de conhecimento."

    # Passo 2: Geração (Generation)
    # Instancia o modelo Gemini 1.5 Flash (otimizado para velocidade e custo)
    model = GenerativeModel("gemini-1.5-flash-001")

    # Constrói o prompt para o modelo
    # Instrução clara para atuar como assistente técnico e usar apenas o contexto fornecido
    prompt = f"""
    Você é o Nexus AI, um assistente de suporte técnico especializado.
    Use as informações de contexto abaixo para responder à pergunta do usuário.
    Se a resposta não estiver no contexto, diga que não sabe. Não invente informações.
    
    Contexto:
    {context_text}
    
    Pergunta do Usuário:
    {user_query}
    
    Resposta:
    """

    try:
        # Envia o prompt para o modelo gerar a resposta
        generation_response = model.generate_content(prompt)
        # Retorna o texto gerado
        return generation_response.text
    except Exception as e:
        logging.error(f"Erro ao gerar resposta com Gemini: {e}")
        return "Desculpe, tive um problema ao processar sua resposta."


def create_ticket_in_django(parameters):
    """
    Envia os dados coletados pelo Dialogflow para a API do Django criar um chamado.
    """
    # Prepara o payload (dados) para a requisição POST
    # Mapeia os parâmetros do Dialogflow para os campos esperados pela API Django
    payload = {
        # Tenta extrair nome de entidade pessoa
        "customer_name": parameters.get("person", {}).get("name", "Cliente Anônimo"),
        # Tenta extrair empresa
        "company": parameters.get("organization", "Não informada"),
        # Descrição do problema
        "description": parameters.get("problem_description", "Sem descrição"),
        # Define prioridade padrão (pode ser ajustada por lógica de sentimento futura)
        "priority": "MEDIUM"
    }

    try:
        # Faz a requisição HTTP POST para o endpoint de criação de tickets
        # Timeout de 5 segundos para não travar a Cloud Function
        response = requests.post(DJANGO_API_URL, json=payload, timeout=5)

        # Verifica se a criação foi bem sucedida (Status 201 Created)
        if response.status_code == 201:
            # Retorna o ID do ticket criado
            return response.json().get("id")
        else:
            logging.error(f"Falha ao criar ticket: {response.text}")
            return "ERRO-API"

    except Exception as e:
        logging.error(f"Erro de conexão com Django API: {e}")
        return "ERRO-CONEXAO"
