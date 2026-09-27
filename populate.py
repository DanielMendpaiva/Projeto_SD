#!/usr/bin/env python
"""Script para popular o banco de dados do RotaAlt com dados fake usando Faker."""
import os
import sys
import random
from datetime import timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rotaalt.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

from contas.models import Perfil
from transporte.models import Operador, Veiculo, Motorista, Parada, Rota, ParadaRota, Viagem
from reservas.models import Reserva, Avaliacao

fake = Faker('pt_BR')


def limpar_banco():
    """Remove todos os dados existentes."""
    print('Limpando banco de dados...')
    Avaliacao.objects.all().delete()
    Reserva.objects.all().delete()
    Viagem.objects.all().delete()
    ParadaRota.objects.all().delete()
    Rota.objects.all().delete()
    Parada.objects.all().delete()
    Motorista.objects.all().delete()
    Veiculo.objects.all().delete()
    Operador.objects.all().delete()
    Perfil.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()


def criar_superusuario():
    """Cria o superusuário admin."""
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@rotaalt.com',
            password='admin123',
            first_name='Administrador',
            last_name='RotaAlt'
        )
        Perfil.objects.create(usuario=admin_user, tipo='gestor')
        print('Superusuário criado: admin / admin123')
    else:
        print('Superusuário já existe.')


def criar_usuarios(quantidade=200):
    """Cria usuários com perfis (passageiros, motoristas, gestores)."""
    print(f'Criando {quantidade} usuários...')
    usuarios = []
    for i in range(quantidade):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name.lower()}.{last_name.lower()}.{i}'
        try:
            user = User.objects.create_user(
                username=username[:30],
                email=fake.email(),
                password='senha123',
                first_name=first_name,
                last_name=last_name,
            )
            # 70% passageiros, 20% motoristas, 10% gestores
            r = random.random()
            if r < 0.7:
                tipo = 'passageiro'
            elif r < 0.9:
                tipo = 'motorista'
            else:
                tipo = 'gestor'

            Perfil.objects.create(
                usuario=user,
                tipo=tipo,
                telefone=fake.phone_number(),
                cpf=fake.cpf(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=65),
            )
            usuarios.append(user)
        except Exception as e:
            pass  # Skip duplicates
    print(f'  {len(usuarios)} usuários criados.')
    return usuarios


def criar_operadores(quantidade=15):
    """Cria operadores (cooperativas/empresas)."""
    print(f'Criando {quantidade} operadores...')
    operadores = []
    nomes_prefixos = [
        'Cooperativa', 'TransCoop', 'VanTur', 'RápidoTrans',
        'ExpressoVan', 'LotaFácil', 'TransAlternativo', 'VanExpress',
        'CoopTrans', 'MicroTrans', 'AlternaVan', 'VanRota',
        'TransCidade', 'CoopVan', 'VanPopular'
    ]
    for i in range(quantidade):
        nome = f'{nomes_prefixos[i % len(nomes_prefixos)]} {fake.city_suffix()} {fake.city()}'
        operador = Operador.objects.create(
            nome=nome[:200],
            cnpj=fake.cnpj(),
            telefone=fake.phone_number(),
            email=fake.company_email(),
            endereco=fake.address(),
            ativo=random.choice([True, True, True, False]),  # 75% ativos
        )
        operadores.append(operador)
    print(f'  {len(operadores)} operadores criados.')
    return operadores


def criar_veiculos(operadores, quantidade=80):
    """Cria veículos vinculados a operadores."""
    print(f'Criando {quantidade} veículos...')
    modelos_van = [
        'Fiat Ducato', 'Mercedes Sprinter', 'Renault Master',
        'Peugeot Boxer', 'Iveco Daily', 'Citroën Jumper'
    ]
    modelos_micro = [
        'Volare V8', 'Marcopolo Senior', 'Neobus Thunder+',
        'Comil Piá', 'Mercedes LO 916', 'Volkswagen 9.160'
    ]
    veiculos = []
    placas_usadas = set()
    for _ in range(quantidade):
        tipo = random.choice(['van', 'van', 'van', 'micro_onibus', 'lotacao'])
        if tipo == 'van':
            modelo = random.choice(modelos_van)
            capacidade = random.choice([12, 15, 16, 18])
        elif tipo == 'micro_onibus':
            modelo = random.choice(modelos_micro)
            capacidade = random.choice([20, 24, 28, 32])
        else:
            modelo = random.choice(modelos_van + modelos_micro)
            capacidade = random.choice([12, 15, 20])

        # Generate unique plate
        while True:
            placa = fake.license_plate()
            if placa not in placas_usadas:
                placas_usadas.add(placa)
                break

        veiculo = Veiculo.objects.create(
            operador=random.choice(operadores),
            placa=placa,
            modelo=modelo,
            tipo=tipo,
            capacidade=capacidade,
            ano=random.randint(2015, 2025),
            ativo=random.choice([True, True, True, False]),
        )
        veiculos.append(veiculo)
    print(f'  {len(veiculos)} veículos criados.')
    return veiculos


def criar_motoristas(operadores, usuarios):
    """Cria motoristas a partir dos usuários com perfil de motorista."""
    print('Criando motoristas...')
    perfis_motorista = Perfil.objects.filter(tipo='motorista')
    motoristas = []
    cnhs_usadas = set()
    for perfil in perfis_motorista:
        while True:
            cnh = fake.numerify('###########')
            if cnh not in cnhs_usadas:
                cnhs_usadas.add(cnh)
                break
        motorista = Motorista.objects.create(
            perfil=perfil,
            operador=random.choice(operadores),
            cnh=cnh,
            categoria_cnh=random.choice(['D', 'D', 'E']),
            ativo=random.choice([True, True, True, False]),
        )
        motoristas.append(motorista)
    print(f'  {len(motoristas)} motoristas criados.')
    return motoristas


def criar_paradas(quantidade=120):
    """Cria paradas (pontos de embarque/desembarque)."""
    print(f'Criando {quantidade} paradas...')
    tipos_local = [
        'Terminal', 'Ponto', 'Praça', 'Rodoviária', 'Estação',
        'Parada', 'Cruzamento', 'Rotatória', 'Shopping', 'Hospital',
        'Mercado', 'Igreja', 'Escola', 'Posto', 'Parque'
    ]
    paradas = []
    for _ in range(quantidade):
        tipo_local = random.choice(tipos_local)
        nome = f'{tipo_local} {fake.street_name()}'
        parada = Parada.objects.create(
            nome=nome[:200],
            endereco=fake.address(),
            latitude=Decimal(str(round(random.uniform(-10.0, -8.0), 6))),
            longitude=Decimal(str(round(random.uniform(-40.0, -38.0), 6))),
            referencia=f'Próximo ao {fake.street_name()}' if random.random() > 0.3 else '',
            ativa=random.choice([True, True, True, True, False]),
        )
        paradas.append(parada)
    print(f'  {len(paradas)} paradas criadas.')
    return paradas


def criar_rotas(operadores, paradas, quantidade=40):
    """Cria rotas com paradas ordenadas."""
    print(f'Criando {quantidade} rotas...')
    rotas = []
    for i in range(quantidade):
        origem = fake.city()
        destino = fake.city()
        rota = Rota.objects.create(
            nome=f'{origem} → {destino}',
            descricao=f'Linha de transporte alternativo de {origem} a {destino}. {fake.sentence()}',
            operador=random.choice(operadores),
            ativa=random.choice([True, True, True, False]),
        )
        # Add 3 to 8 ordered stops
        num_paradas = random.randint(3, 8)
        paradas_selecionadas = random.sample(paradas, min(num_paradas, len(paradas)))
        for ordem, parada in enumerate(paradas_selecionadas, start=1):
            ParadaRota.objects.create(
                rota=rota,
                parada=parada,
                ordem=ordem,
                tempo_estimado=timedelta(minutes=random.randint(5, 30)),
            )
        rotas.append(rota)
    print(f'  {len(rotas)} rotas criadas.')
    return rotas


def criar_viagens(rotas, veiculos, motoristas, quantidade=300):
    """Cria viagens agendadas, em andamento, concluídas e canceladas."""
    print(f'Criando {quantidade} viagens...')
    if not motoristas:
        print('  Nenhum motorista disponível. Pulando viagens.')
        return []
    viagens = []
    agora = timezone.now()
    for _ in range(quantidade):
        rota = random.choice(rotas)
        veiculo = random.choice(veiculos)
        motorista = random.choice(motoristas)
        dias_offset = random.randint(-30, 30)
        hora = random.randint(5, 22)
        minuto = random.choice([0, 15, 30, 45])
        data_saida = agora + timedelta(days=dias_offset, hours=hora - agora.hour, minutes=minuto - agora.minute)

        if dias_offset < -2:
            status = random.choice(['concluida', 'concluida', 'concluida', 'cancelada'])
        elif dias_offset < 0:
            status = random.choice(['concluida', 'em_andamento'])
        else:
            status = random.choice(['agendada', 'agendada', 'agendada', 'cancelada'])

        data_chegada = None
        if status == 'concluida':
            data_chegada = data_saida + timedelta(minutes=random.randint(30, 180))

        viagem = Viagem.objects.create(
            rota=rota,
            veiculo=veiculo,
            motorista=motorista,
            data_hora_saida=data_saida,
            data_hora_chegada=data_chegada,
            status=status,
            vagas_disponiveis=random.randint(0, veiculo.capacidade),
            preco=Decimal(str(round(random.uniform(3.50, 25.00), 2))),
            observacoes=fake.sentence() if random.random() > 0.6 else '',
        )
        viagens.append(viagem)
    print(f'  {len(viagens)} viagens criadas.')
    return viagens


def criar_reservas(viagens, usuarios, quantidade=250):
    """Cria reservas de passageiros em viagens."""
    print(f'Criando até {quantidade} reservas...')
    passageiros = [u for u in usuarios if hasattr(u, 'perfil') and u.perfil.tipo == 'passageiro']
    if not passageiros:
        passageiros = usuarios[:50]
    reservas = []
    pares_usados = set()
    tentativas = 0
    while len(reservas) < quantidade and tentativas < quantidade * 3:
        tentativas += 1
        viagem = random.choice(viagens)
        passageiro = random.choice(passageiros)
        par = (viagem.id, passageiro.id)
        if par in pares_usados:
            continue
        pares_usados.add(par)

        if viagem.status == 'cancelada':
            status = 'cancelada'
        elif viagem.status == 'concluida':
            status = random.choice(['utilizada', 'utilizada', 'cancelada'])
        else:
            status = random.choice(['confirmada', 'confirmada', 'confirmada', 'cancelada'])

        try:
            reserva = Reserva.objects.create(
                viagem=viagem,
                passageiro=passageiro,
                status=status,
                quantidade_vagas=random.choice([1, 1, 1, 2]),
            )
            reservas.append(reserva)
        except Exception:
            pass
    print(f'  {len(reservas)} reservas criadas.')
    return reservas


def criar_avaliacoes(viagens, usuarios, quantidade=180):
    """Cria avaliações de viagens concluídas."""
    print(f'Criando até {quantidade} avaliações...')
    viagens_concluidas = [v for v in viagens if v.status == 'concluida']
    if not viagens_concluidas:
        print('  Nenhuma viagem concluída. Pulando avaliações.')
        return []
    passageiros = [u for u in usuarios if hasattr(u, 'perfil') and u.perfil.tipo == 'passageiro']
    if not passageiros:
        passageiros = usuarios[:50]

    comentarios_positivos = [
        'Ótimo serviço! Motorista muito educado.',
        'Pontual e confortável. Recomendo!',
        'Van limpa e bem conservada.',
        'Excelente! Sempre viajo com essa linha.',
        'Muito bom, preço justo.',
        'Motorista experiente, viagem tranquila.',
        'Melhor que o ônibus convencional!',
        'Rápido e seguro. Nota 10!',
    ]
    comentarios_negativos = [
        'Atrasou bastante hoje.',
        'Van lotada, desconfortável.',
        'Motorista dirigindo muito rápido.',
        'Poderia melhorar a limpeza.',
        'Demorou muito para sair.',
    ]
    comentarios_neutros = [
        'Serviço ok, nada demais.',
        'Normal, cumpriu o horário.',
        'Viagem tranquila.',
        '',
    ]

    avaliacoes = []
    pares_usados = set()
    tentativas = 0
    while len(avaliacoes) < quantidade and tentativas < quantidade * 3:
        tentativas += 1
        viagem = random.choice(viagens_concluidas)
        passageiro = random.choice(passageiros)
        par = (viagem.id, passageiro.id)
        if par in pares_usados:
            continue
        pares_usados.add(par)

        nota = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 30, 40])[0]
        if nota >= 4:
            comentario = random.choice(comentarios_positivos)
        elif nota <= 2:
            comentario = random.choice(comentarios_negativos)
        else:
            comentario = random.choice(comentarios_neutros)

        try:
            avaliacao = Avaliacao.objects.create(
                viagem=viagem,
                passageiro=passageiro,
                nota=nota,
                comentario=comentario,
            )
            avaliacoes.append(avaliacao)
        except Exception:
            pass
    print(f'  {len(avaliacoes)} avaliações criadas.')
    return avaliacoes


def main():
    """Função principal de população do banco."""
    print('=' * 60)
    print('  RotaAlt - Populando banco de dados com Faker')
    print('=' * 60)
    print()

    limpar_banco()
    criar_superusuario()

    usuarios = criar_usuarios(200)
    operadores = criar_operadores(15)
    veiculos = criar_veiculos(operadores, 80)
    motoristas = criar_motoristas(operadores, usuarios)
    paradas = criar_paradas(120)
    rotas = criar_rotas(operadores, paradas, 40)
    viagens = criar_viagens(rotas, veiculos, motoristas, 300)
    reservas = criar_reservas(viagens, usuarios, 250)
    avaliacoes = criar_avaliacoes(viagens, usuarios, 180)

    print()
    print('=' * 60)
    print('  Resumo')
    print('=' * 60)
    print(f'  Usuários:    {User.objects.count()}')
    print(f'  Perfis:      {Perfil.objects.count()}')
    print(f'  Operadores:  {Operador.objects.count()}')
    print(f'  Veículos:    {Veiculo.objects.count()}')
    print(f'  Motoristas:  {Motorista.objects.count()}')
    print(f'  Paradas:     {Parada.objects.count()}')
    print(f'  Rotas:       {Rota.objects.count()}')
    print(f'  Viagens:     {Viagem.objects.count()}')
    print(f'  Reservas:    {Reserva.objects.count()}')
    print(f'  Avaliações:  {Avaliacao.objects.count()}')
    print()
    print('Credenciais do admin:')
    print('  URL:    http://localhost:8000/admin/')
    print('  User:   admin')
    print('  Senha:  admin123')
    print()
    print('Pronto!')


if __name__ == '__main__':
    main()
