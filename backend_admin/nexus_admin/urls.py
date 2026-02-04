from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('core.urls')), # Descomentar quando houver urls no app core
]
