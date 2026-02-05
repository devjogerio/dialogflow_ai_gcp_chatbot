from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Ticket, Budget


class TicketModelTest(TestCase):
    """
    Testes para o modelo Ticket.
    """

    def setUp(self):
        self.ticket = Ticket.objects.create(
            customer_name="João Silva",
            description="Problema com internet",
            status="OPEN",
            priority="HIGH"
        )

    def test_ticket_creation(self):
        """Teste se o ticket é criado corretamente."""
        self.assertEqual(self.ticket.customer_name, "João Silva")
        self.assertEqual(self.ticket.status, "OPEN")
        self.assertTrue(isinstance(self.ticket, Ticket))
        self.assertEqual(str(self.ticket), f"Ticket #{self.ticket.id} - João Silva")


class BudgetModelTest(TestCase):
    """
    Testes para o modelo Budget.
    """

    def setUp(self):
        self.budget = Budget.objects.create(
            customer_name="Maria Oliveira",
            products=[{"name": "Modem", "price": 100}],
            total_value=100.00
        )

    def test_budget_creation(self):
        """Teste se o orçamento é criado corretamente."""
        self.assertEqual(self.budget.customer_name, "Maria Oliveira")
        self.assertEqual(self.budget.total_value, 100.00)
        self.assertEqual(str(self.budget), f"Orçamento #{self.budget.id} - R$ 100.0")


class TicketAPITest(APITestCase):
    """
    Testes para a API de Tickets.
    """

    def setUp(self):
        self.url = reverse('ticket-list')  # Assume que a rota se chama 'ticket-list'
        self.ticket_data = {
            "customer_name": "Teste API",
            "description": "Teste via API",
            "status": "OPEN",
            "priority": "MEDIUM"
        }

    def test_create_ticket(self):
        """Teste de criação de ticket via API."""
        # Precisamos garantir que a URL esteja correta. Se não estiver configurada no urls.py, isso falhará.
        # Vamos assumir que o router registrou como 'ticket-list'.
        # Se falhar, ajustaremos o urls.py.
        
        # Nota: Como não temos acesso fácil ao urls.py neste momento para confirmar o nome,
        # vou usar o caminho explícito se o reverse falhar, mas o ideal é reverse.
        # Vou tentar usar o caminho '/api/tickets/' que estava na docstring da view.
        
        url = '/api/tickets/'
        response = self.client.post(url, self.ticket_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().customer_name, "Teste API")
