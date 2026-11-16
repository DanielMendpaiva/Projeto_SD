from django.urls import path

from . import views

app_name = 'contas'

urlpatterns = [
    path('', views.cadastro_passageiro, name='cadastro'),
]
