from django.shortcuts import render, get_object_or_404
from .models import Viagem, Rota


def home(request):
    """Pagina inicial: mostra o formulario de busca e as proximas viagens."""
    # pega as primeiras 6 viagens agendadas
    viagens = Viagem.objects.filter(status='agendada').order_by('data_hora_saida')[:6]
    rotas = Rota.objects.filter(ativa=True)[:6]

    return render(request, 'transporte/home.html', {
        'viagens': viagens,
        'rotas': rotas,
    })


def lista_viagens(request):
    """Lista as viagens com filtros de busca por origem, destino ou data."""
    viagens = Viagem.objects.filter(status='agendada').order_by('data_hora_saida')

    origem = request.GET.get('origem', '').strip()
    destino = request.GET.get('destino', '').strip()
    data = request.GET.get('data', '').strip()

    # filtra se o usuario digitou alguma origem ou destino no nome da rota
    if origem:
        viagens = viagens.filter(rota__nome__icontains=origem)
    if destino:
        viagens = viagens.filter(rota__nome__icontains=destino)
    if data:
        # compara apenas a data sem as horas
        viagens = viagens.filter(data_hora_saida__date=data)

    return render(request, 'transporte/lista_viagens.html', {
        'viagens': viagens,
        'origem': origem,
        'destino': destino,
        'data': data,
    })


def detalhe_viagem(request, viagem_id):
    """Exibe todos os dados de uma viagem e suas paradas."""
    viagem = get_object_or_404(Viagem, id=viagem_id)
    # busca as paradas ordenadas pela sequencia da rota
    paradas = viagem.rota.paradas_ordenadas.all().order_by('ordem')

    return render(request, 'transporte/detalhe_viagem.html', {
        'viagem': viagem,
        'paradas': paradas,
    })
