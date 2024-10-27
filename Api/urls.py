from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),  # Configuración para login de allauth
    path('', include('entradasplus.urls')),  # Enlace a las URLs de la aplicación
]
