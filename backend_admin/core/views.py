from rest_framework import viewsets
from rest_framework import serializers
from .models import Ticket


# Serializer define como o modelo Ticket é convertido para JSON e vice-versa
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'  # Expõe todos os campos do modelo na API


class TicketViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para gerenciar Tickets.
    Fornece automaticamente as operações CRUD (Create, Read, Update, Delete).
    O endpoint será acessível em /api/tickets/
    """
    # Define a query base: todos os tickets ordenados por criação
    queryset = Ticket.objects.all()
    # Define o serializer a ser usado para validação e formatação
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método create para adicionar logs ou lógica
        customizada ao receber um novo chamado via API.
        """
        # Chama a implementação padrão de criação
        response = super().create(request, *args, **kwargs)

        # Aqui poderíamos adicionar lógica extra, como enviar um email
        # para o suporte
        # print(f"Novo ticket criado com ID: {response.data['id']}")

        return response
