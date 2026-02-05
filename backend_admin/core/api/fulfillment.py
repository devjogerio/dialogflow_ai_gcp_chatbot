import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import transaction
from core.models import Ticket

logger = logging.getLogger(__name__)


class DialogflowFulfillmentView(APIView):
    """
    Endpoint para receber Webhooks do Dialogflow ES.
    """
    # Desativa autenticação padrão do DRF para este endpoint, pois usamos token customizado
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Recebe POST do Dialogflow com intent e parâmetros.
        """
        # 1. Validação de Segurança (Token no Header)
        # O token deve ser configurado no Dialogflow Fulfillment headers
        auth_header = request.headers.get(
            'Authorization') or request.headers.get('x-dialogflow-token')
        expected_token = getattr(settings, 'DIALOGFLOW_WEBHOOK_TOKEN', None)

        # Se não houver token configurado no settings, loga aviso (mas bloqueia por segurança se for prod)
        if not expected_token:
            logger.error(
                "DIALOGFLOW_WEBHOOK_TOKEN não configurado no settings. Bloqueando requisição.")
            return Response({"error": "Server misconfiguration"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if auth_header != expected_token:
            logger.warning(
                f"Tentativa de acesso não autorizado ao Webhook. Token recebido: {auth_header}")
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # 2. Extração de Dados
        data = request.data
        query_result = data.get('queryResult', {})
        intent_display_name = query_result.get('intent', {}).get('displayName')
        parameters = query_result.get('parameters', {})

        logger.info(
            f"Webhook Dialogflow recebido. Intent: {intent_display_name}")

        try:
            # 3. Roteamento de Intents
            if intent_display_name == 'abrir_chamado':
                return self.handle_abrir_chamado(parameters)

            # Se for outra intent que não tratamos, retorna resposta padrão
            return Response({
                "fulfillmentText": f"Recebi a intenção {intent_display_name}, mas não tenho ação configurada para ela no backend."
            })

        except Exception as e:
            logger.error(f"Erro ao processar webhook: {str(e)}", exc_info=True)
            return Response({
                "fulfillmentText": "Desculpe, ocorreu um erro interno ao processar sua solicitação."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_abrir_chamado(self, params):
        """
        Lógica para criar ticket a partir dos parâmetros do Dialogflow.
        """
        # Mapeamento de campos
        # Dialogflow pode enviar sys.person como dict {'name': 'Fulano'} ou string
        person_name_raw = params.get('person_name')
        if isinstance(person_name_raw, dict):
            person_name = person_name_raw.get('name')
        else:
            person_name = person_name_raw

        contact_info = params.get('contact_info', '')
        department = params.get('department', '')
        ticket_title = params.get('ticket_title', '')
        ticket_type = params.get('ticket_type', '')
        category = params.get('category', '')
        priority_raw = params.get('priority', 'Média')
        description_text = params.get('description', '')
        location = params.get('location', '')

        # Mapeamento de Prioridade
        priority_map = {
            'Crítica': 'CRITICAL',
            'Alta': 'HIGH',
            'Média': 'MEDIUM',
            'Baixa': 'LOW'
        }
        priority_db = priority_map.get(priority_raw, 'MEDIUM')

        # Construção da Descrição Completa
        full_description = (
            f"Título: {ticket_title}\n"
            f"Tipo: {ticket_type}\n"
            f"Categoria: {category}\n"
            f"Contato: {contact_info}\n"
            f"Localização: {location}\n\n"
            f"Descrição do Usuário:\n{description_text}"
        )

        # Criação Atômica do Ticket
        with transaction.atomic():
            ticket = Ticket.objects.create(
                customer_name=person_name or "Anônimo",
                company=department,  # Usando departamento como empresa/org
                description=full_description,
                status='OPEN',
                priority=priority_db
            )

        logger.info(f"Ticket #{ticket.id} criado via Dialogflow.")

        # Resposta para o Dialogflow
        return Response({
            "fulfillmentText": f"Seu chamado foi aberto com sucesso! O número do protocolo é #{ticket.id}. Nossa equipe de {department} analisará o caso com prioridade {priority_raw}."
        })
