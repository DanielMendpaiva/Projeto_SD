"""
Configuração de URLs do projeto RotaAlt.
"""
from django.contrib import admin
from django.urls import path

# Customização do painel administrativo
admin.site.site_header = 'RotaAlt - Administração'
admin.site.site_title = 'RotaAlt Admin'
admin.site.index_title = 'Painel de Gestão'

urlpatterns = [
    path('admin/', admin.site.urls),
]
