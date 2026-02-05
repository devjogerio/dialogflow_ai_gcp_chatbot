from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Ticket, Budget
import time


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
        self.assertEqual(str(self.ticket),
                         f"Ticket #{self.ticket.id} - João Silva")


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
        self.assertEqual(str(self.budget),
                         f"Orçamento #{self.budget.id} - R$ 100.0")


class TicketAPITest(APITestCase):
    """
    Testes para a API de Tickets (CRUD completo, Casos de Borda, Performance e Segurança).
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.url = '/api/tickets/'
        self.ticket_data = {
            "customer_name": "Teste API",
            "description": "Teste via API",
            "status": "OPEN",
            "priority": "MEDIUM"
        }

    def test_create_ticket(self):
        """Teste de criação de ticket via API (Cenário Feliz)."""
        response = self.client.post(self.url, self.ticket_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().customer_name, "Teste API")

    def test_create_ticket_invalid_data(self):
        """Teste de validação de dados obrigatórios."""
        invalid_data = {
            "description": "Faltando nome do cliente",
            "status": "OPEN"
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_name", response.data)

    def test_update_ticket(self):
        """Teste de atualização de ticket (PUT/PATCH)."""
        # Cria ticket inicial
        response_create = self.client.post(
            self.url, self.ticket_data, format='json')
        ticket_id = response_create.data['id']

        # Atualiza status
        update_url = f'{self.url}{ticket_id}/'
        update_data = {"status": "RESOLVED", "customer_name": "Teste API",
                       "description": "Resolvido", "priority": "MEDIUM"}
        response = self.client.put(update_url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ticket.objects.get(id=ticket_id).status, "RESOLVED")

    def test_delete_ticket(self):
        """Teste de exclusão de ticket."""
        response_create = self.client.post(
            self.url, self.ticket_data, format='json')
        ticket_id = response_create.data['id']

        delete_url = f'{self.url}{ticket_id}/'
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_performance_create_ticket(self):
        """Teste de performance: criação deve ser menor que 200ms."""
        start_time = time.time()
        response = self.client.post(self.url, self.ticket_data, format='json')
        end_time = time.time()

        duration = (end_time - start_time) * 1000  # ms
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(
            duration, 200, f"Tempo de resposta excedeu 200ms: {duration:.2f}ms")

    def test_method_not_allowed(self):
        """Teste de segurança: Método HTTP inválido."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_access(self):
        """Teste de acesso sem autenticação (deve falhar)."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthAPITest(APITestCase):
    """
    Testes de Autenticação (Login, Logout, CSRF).
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.login_url = '/api/auth/login/'
        self.logout_url = '/api/auth/logout/'

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)

    def test_login_failure(self):
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'wrong'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CORSTest(TestCase):
    """
    Testes de CORS.
    """

    def test_cors_headers(self):
        # Simula uma requisição OPTIONS de uma origem permitida (localhost:3000)
        response = self.client.options(
            '/api/tickets/', HTTP_ORIGIN='http://localhost:3000')
        self.assertTrue(response.has_header('Access-Control-Allow-Origin'))
        self.assertEqual(
            response['Access-Control-Allow-Origin'], 'http://localhost:3000')
        self.assertTrue(response.has_header(
            'Access-Control-Allow-Credentials'))
        self.assertEqual(response['Access-Control-Allow-Credentials'], 'true')
