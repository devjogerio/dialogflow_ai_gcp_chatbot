from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Ticket
import json

class DialogflowFulfillmentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('dialogflow_fulfillment')
        self.token = 'test-token'
        
        # Override setting for test
        from django.conf import settings
        self.original_token = getattr(settings, 'DIALOGFLOW_WEBHOOK_TOKEN', None)
        settings.DIALOGFLOW_WEBHOOK_TOKEN = self.token

    def tearDown(self):
        from django.conf import settings
        if self.original_token:
            settings.DIALOGFLOW_WEBHOOK_TOKEN = self.original_token

    def test_missing_token(self):
        """Teste de rejeição sem token"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_wrong_token(self):
        """Teste de rejeição com token errado"""
        response = self.client.post(
            self.url, 
            {}, 
            format='json',
            HTTP_AUTHORIZATION='wrong-token'
        )
        self.assertEqual(response.status_code, 401)

    def test_create_ticket_success(self):
        """Teste de criação bem sucedida de ticket via intent abrir_chamado"""
        payload = {
            "queryResult": {
                "intent": {
                    "displayName": "abrir_chamado"
                },
                "parameters": {
                    "person_name": {"name": "João Silva"},
                    "department": "RH",
                    "ticket_title": "Impressora quebrada",
                    "ticket_type": "Incidente",
                    "category": "Hardware",
                    "priority": "Alta",
                    "description": "Não liga mais",
                    "location": "Sala 3"
                }
            }
        }
        
        response = self.client.post(
            self.url,
            payload,
            format='json',
            HTTP_AUTHORIZATION=self.token
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("chamado foi aberto com sucesso", response.data['fulfillmentText'])
        
        # Verificar DB
        ticket = Ticket.objects.last()
        self.assertEqual(ticket.customer_name, "João Silva")
        self.assertEqual(ticket.company, "RH")
        self.assertEqual(ticket.priority, "HIGH")
        self.assertIn("Impressora quebrada", ticket.description)
        self.assertIn("Não liga mais", ticket.description)

    def test_create_ticket_simple_string_name(self):
        """Teste com person_name vindo como string (comportamento variável do Dialogflow)"""
        payload = {
            "queryResult": {
                "intent": {
                    "displayName": "abrir_chamado"
                },
                "parameters": {
                    "person_name": "Maria",
                    "priority": "Baixa"
                }
            }
        }
        
        response = self.client.post(
            self.url,
            payload,
            format='json',
            HTTP_AUTHORIZATION=self.token
        )
        
        self.assertEqual(response.status_code, 200)
        ticket = Ticket.objects.last()
        self.assertEqual(ticket.customer_name, "Maria")
        self.assertEqual(ticket.priority, "LOW")

    def test_unhandled_intent(self):
        """Teste de intent desconhecida"""
        payload = {
            "queryResult": {
                "intent": {
                    "displayName": "unknown_intent"
                }
            }
        }
        response = self.client.post(
            self.url,
            payload,
            format='json',
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("não tenho ação configurada", response.data['fulfillmentText'])
