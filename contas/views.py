from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CadastroPassageiroForm


def cadastro_passageiro(request):
    if request.method == 'POST':
        form = CadastroPassageiroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('contas:cadastro')
        messages.error(request, 'Não foi possível concluir o cadastro. Confira os campos destacados.')
    else:
        form = CadastroPassageiroForm()

    return render(request, 'contas/cadastro.html', {'form': form})
