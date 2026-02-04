# Importação das bibliotecas padrão do Python para manipulação de JSON e requisições
import functions_framework
from flask import jsonify
import logging
# Importação do módulo interno responsável pela lógica de RAG (Retrieval-Augmented Generation)
from vertex_rag import process_rag_query, create_ticket_in_django

# Configuração básica de logging para monitoramento no Google Cloud Logging
# Define o nível de log como INFO para capturar eventos importantes
logging.basicConfig(level=logging.INFO)

# Decorador do Functions Framework que marca a função 'dialogflow_webhook' como ponto de entrada HTTP
# Isso permite que a função seja acionada por requisições HTTP (POST) do Dialogflow
@functions_framework.http
def dialogflow_webhook(request):
    """
    Função principal do Webhook para o Dialogflow ES.
    Recebe a requisição JSON do Dialogflow, identifica a Intent e executa a lógica apropriada.
    """
    
    # Tenta processar o corpo da requisição como JSON
    # request.get_json(silent=True) retorna None se o corpo não for JSON válido, evitando erros abruptos
    request_json = request.get_json(silent=True)
    
    # Verifica se a requisição possui corpo JSON e se contém o campo 'queryResult'
    # 'queryResult' é o objeto padrão do Dialogflow contendo os detalhes da interação
    if request_json and 'queryResult' in request_json:
        
        # Extrai o objeto 'queryResult' para uma variável local para facilitar o acesso
        query_result = request_json.get('queryResult')
        
        # Extrai o nome da Intent detectada pelo Dialogflow
        # 'intent' é um dicionário e 'displayName' é o nome legível da intenção configurada no console
        intent_name = query_result.get('intent', {}).get('displayName')
        
        # Extrai os parâmetros capturados (entidades) da conversa
        # Ex: nome, empresa, descrição do problema
        parameters = query_result.get('parameters', {})
        
        # Extrai a mensagem original do usuário (queryText)
        # Isso é crucial para passar ao modelo de IA (Gemini) para contexto
        user_query = query_result.get('queryText')

        # Loga a intenção recebida para fins de depuração e monitoramento
        logging.info(f"Intent recebida: {intent_name}")

        # Estrutura de decisão para rotear a lógica baseada na Intent identificada
        
        # Caso 1: Intent de Dúvida Técnica (RAG)
        # Ocorre quando o usuário faz uma pergunta que requer consulta à base de conhecimento
        if intent_name == 'duvida_tecnica':
            # Chama a função auxiliar process_rag_query importada de vertex_rag.py
            # Passa a query do usuário para buscar documentos e gerar resposta com Gemini
            response_text = process_rag_query(user_query)
            
            # Retorna a resposta formatada no padrão esperado pelo Dialogflow
            return jsonify({
                "fulfillmentText": response_text
            })

        # Caso 2: Intent de Abertura de Chamado
        # Ocorre quando o usuário confirma que deseja abrir um ticket de suporte
        elif intent_name == 'abrir_chamado':
            # Chama a função auxiliar create_ticket_in_django para persistir os dados
            # Envia os parâmetros coletados pelo Dialogflow (nome, empresa, problema)
            ticket_id = create_ticket_in_django(parameters)
            
            # Constrói a mensagem de sucesso com o ID do chamado gerado
            response_text = f"Chamado #{ticket_id} criado com sucesso! Nossa equipe entrará em contato em breve."
            
            # Retorna a confirmação para o usuário
            return jsonify({
                "fulfillmentText": response_text
            })
            
        # Caso 3: Intent Default ou Desconhecida
        # Tratamento genérico para intents não mapeadas explicitamente no código
        else:
            # Retorna uma mensagem padrão indicando que a função foi acionada mas não tratou a intent
            return jsonify({
                "fulfillmentText": f"Webhook recebeu a intent: {intent_name}, mas não há lógica implementada para ela."
            })

    # Caso de erro: Requisição inválida (sem JSON ou formato incorreto)
    # Retorna um JSON de erro e código HTTP 400 (Bad Request)
    else:
        return jsonify({"error": "Requisição inválida. Esperado JSON do Dialogflow."}), 400
