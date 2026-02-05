from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
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
    # Exige autenticação para acessar os tickets
    permission_classes = [permissions.IsAuthenticated]

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


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'detail': 'Login successful',
                'username': user.username,
                'is_staff': user.is_staff
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'csrfToken': get_token(request)})


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser
        })
