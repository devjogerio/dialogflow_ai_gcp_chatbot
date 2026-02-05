"""
URL configuration for nexus_admin project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import TicketViewSet, LoginView, LogoutView, CSRFTokenView, UserInfoView
from core.api.fulfillment import DialogflowFulfillmentView

# Configuração do Router da API
router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/dialogflow/fulfillment/', DialogflowFulfillmentView.as_view(), name='dialogflow_fulfillment'),
    path('api/auth/login/', LoginView.as_view(), name='api_login'),
    path('api/auth/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/auth/csrf/', CSRFTokenView.as_view(), name='api_csrf'),
    path('api/auth/user/', UserInfoView.as_view(), name='api_user_info'),
]
