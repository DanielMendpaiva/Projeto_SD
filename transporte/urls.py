from django.urls import path
from . import views

app_name = 'transporte'

urlpatterns = [
    path('', views.home, name='home'),
    path('viagens/', views.lista_viagens, name='lista_viagens'),
    path('viagens/<int:viagem_id>/', views.detalhe_viagem, name='detalhe_viagem'),
]
