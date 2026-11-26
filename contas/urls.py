from django.urls import path

from . import views

app_name = 'contas'

urlpatterns = [
    path('cadastro/', views.cadastro_passageiro, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]
