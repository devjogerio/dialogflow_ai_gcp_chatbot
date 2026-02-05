from django.db import models


class Ticket(models.Model):
    """
    Modelo que representa um Chamado de Suporte (Ticket).
    Armazena os dados vindos do Dialogflow/Cloud Function e o status
    do atendimento.
    """

    # Opções de status para o controle do fluxo de atendimento
    STATUS_CHOICES = [
        ('OPEN', 'Aberto'),
        ('IN_PROGRESS', 'Em Andamento'),
        ('RESOLVED', 'Resolvido'),
        ('CLOSED', 'Fechado'),
    ]

    # Opções de prioridade
    PRIORITY_CHOICES = [
        ('LOW', 'Baixa'),
        ('MEDIUM', 'Média'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]

    # Nome do cliente que solicitou o suporte
    customer_name = models.CharField(
        max_length=255,
        verbose_name="Nome do Cliente"
    )

    # Nome da empresa do cliente (importante para contratos B2B)
    company = models.CharField(
        max_length=255,
        verbose_name="Empresa",
        blank=True,
        null=True
    )

    # Descrição detalhada do problema relatado
    description = models.TextField(verbose_name="Descrição do Problema")

    # Status atual do chamado (padrão: Aberto)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN',
        verbose_name="Status"
    )

    # Prioridade do chamado (pode ser inferida via IA futuramente)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name="Prioridade"
    )

    # Data de criação automática (timestamp)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Abertura"
    )

    # Data da última atualização automática
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    def __str__(self):
        # Representação em string do objeto (ex: Ticket #123 - Cliente X)
        return f"Ticket #{self.id} - {self.customer_name}"

    class Meta:
        # Nome amigável no painel administrativo
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        # Ordenação padrão: mais recentes primeiro
        ordering = ['-created_at']


class Budget(models.Model):
    """
    Modelo simplificado para Orçamentos gerados pelo bot.
    """
    customer_name = models.CharField(max_length=255)
    # Armazena JSON com itens
    products = models.JSONField(verbose_name="Lista de Produtos")
    total_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Total"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orçamento #{self.id} - R$ {self.total_value}"
