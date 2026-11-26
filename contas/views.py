from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import CadastroPassageiroForm


def cadastro_passageiro(request):
    if request.method == 'POST':
        form = CadastroPassageiroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('contas:login')
        messages.error(request, 'Não foi possível concluir o cadastro. Confira os campos destacados.')
    else:
        form = CadastroPassageiroForm()

    return render(request, 'contas/cadastro.html', {'form': form})


def login_usuario(request):
    # Se o usuário já estiver logado, redireciona para o início
    if request.user.is_authenticated:
        return redirect('transporte:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Bem-vindo(a), {usuario.first_name or usuario.username}!')

            # Redireciona para o destino original (next) ou para a home
            proxima = request.GET.get('next') or 'transporte:home'
            return redirect(proxima)
        else:
            messages.error(request, 'Usuário ou senha inválidos. Confira os dados informados.')
    else:
        form = AuthenticationForm()

    return render(request, 'contas/login.html', {'form': form})


def logout_usuario(request):
    logout(request)
    messages.info(request, 'Você encerrou sua sessão com sucesso.')
    return redirect('transporte:home')

