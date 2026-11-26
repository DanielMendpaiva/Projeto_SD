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


# Usuários pré-configurados com credenciais fáceis para testes e apresentações
USUARIOS_TESTE_FIXOS = [
    # Motoristas de teste
    {
        'username': 'motorista.carlos',
        'first_name': 'Carlos',
        'last_name': 'Silva',
        'email': 'carlos.motorista@rotaalt.com',
        'tipo': 'motorista',
        'telefone': '(87) 98811-2233',
        'cpf': '111.222.333-01',
    },
    {
        'username': 'motorista.antonio',
        'first_name': 'Antônio',
        'last_name': 'Souza',
        'email': 'antonio.motorista@rotaalt.com',
        'tipo': 'motorista',
        'telefone': '(74) 98822-3344',
        'cpf': '222.333.444-02',
    },
    {
        'username': 'motorista.jose',
        'first_name': 'José',
        'last_name': 'Pereira',
        'email': 'jose.motorista@rotaalt.com',
        'tipo': 'motorista',
        'telefone': '(87) 98833-4455',
        'cpf': '333.444.555-03',
    },
    # Clientes / Passageiros de teste
    {
        'username': 'cliente.maria',
        'first_name': 'Maria',
        'last_name': 'Santos',
        'email': 'maria.passageira@gmail.com',
        'tipo': 'passageiro',
        'telefone': '(87) 99100-1122',
        'cpf': '444.555.666-04',
    },
    {
        'username': 'cliente.joao',
        'first_name': 'João',
        'last_name': 'Oliveira',
        'email': 'joao.passageiro@gmail.com',
        'tipo': 'passageiro',
        'telefone': '(74) 99200-2233',
        'cpf': '555.666.777-05',
    },
    {
        'username': 'cliente.ana',
        'first_name': 'Ana',
        'last_name': 'Ferreira',
        'email': 'ana.passageira@gmail.com',
        'tipo': 'passageiro',
        'telefone': '(87) 99300-3344',
        'cpf': '666.777.888-06',
    },
    # Gestor de Cooperativa de teste
    {
        'username': 'gestor.coop',
        'first_name': 'Marcos',
        'last_name': 'Gestor',
        'email': 'gestao@cootransvale.com',
        'tipo': 'gestor',
        'telefone': '(87) 98123-4567',
        'cpf': '777.888.999-07',
    },
]


def criar_usuarios(quantidade=200):
    """Cria usuários de teste fixos e completa com perfis gerados por Faker."""
    print(f'Criando usuários de teste fixos e até {quantidade} aleatórios...')
    usuarios = []

    # 1. Cria primeiro os usuários fixos com logins conhecidos
    for item in USUARIOS_TESTE_FIXOS:
        try:
            user = User.objects.create_user(
                username=item['username'],
                email=item['email'],
                password='senha123',
                first_name=item['first_name'],
                last_name=item['last_name'],
            )
            Perfil.objects.create(
                usuario=user,
                tipo=item['tipo'],
                telefone=item['telefone'],
                cpf=item['cpf'],
                data_nascimento=fake.date_of_birth(minimum_age=20, maximum_age=60),
            )
            usuarios.append(user)
        except Exception as e:
            pass

    # 2. Gera os demais usuários aleatórios
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
            pass  
    print(f'  {len(usuarios)} usuários criados (incluindo contas de teste fixas).')
    return usuarios


COOPERATIVAS_CONFIG = [
    # --- Pernambuco (Petrolina e Região) ---
    {
        'sigla': 'COOTRANSVALE',
        'nome': 'COOTRANSVALE - Coop. de Transporte do Vale do São Francisco',
        'endereco': 'Terminal Rodoviário de Petrolina - Geva, Petrolina - PE',
    },
    {
        'sigla': 'COOTRAP',
        'nome': 'COOTRAP - Coop. de Transporte de Passageiros de Petrolina',
        'endereco': 'Ponto das Vans do Interior, Centro, Petrolina - PE',
    },
    {
        'sigla': 'COOTRANSPE',
        'nome': 'COOTRANSPE - Coop. dos Transportadores de Pernambuco',
        'endereco': 'Av. Sete de Setembro, s/n, Petrolina - PE',
    },
    {
        'sigla': 'COOTRANSERTÃO',
        'nome': 'COOTRANSERTÃO - Coop. dos Transportadores Sertanejos',
        'endereco': 'Praça da Catedral, Centro, Petrolina - PE',
    },
    # --- Bahia (Juazeiro e Região) ---
    {
        'sigla': 'COOTRANSJUA',
        'nome': 'COOTRANSJUA - Coop. de Transporte Alternativo de Juazeiro',
        'endereco': 'Mercado do Produtor de Juazeiro, Rod. Lomanto Júnior, Juazeiro - BA',
    },
    {
        'sigla': 'ASTAFRAN',
        'nome': 'ASTAFRAN - Assoc. dos Transportadores de Casa Nova',
        'endereco': 'Terminal de Vans Juazeiro / Posto Fiscal BR-235, Juazeiro - BA',
    },
    {
        'sigla': 'ASTRASOB',
        'nome': 'ASTRASOB - Assoc. dos Transportadores de Sobradinho',
        'endereco': 'Terminal Rodoviário de Juazeiro - BA-210, Juazeiro - BA',
    },
    {
        'sigla': 'ASTRASS',
        'nome': 'ASTRASS - Assoc. dos Transportadores de Sento Sé',
        'endereco': 'Ponto das Vans de Sento Sé, BA-210, Juazeiro - BA',
    },
    {
        'sigla': 'ASTAR',
        'nome': 'ASTAR - Assoc. dos Transportadores de Remanso e Região',
        'endereco': 'Terminal Urbano de Juazeiro, Juazeiro - BA',
    },
    {
        'sigla': 'ASTRA-Curaçá',
        'nome': 'Assoc. dos Transportadores de Curaçá',
        'endereco': 'Terminal de Passageiros, BA-210, Juazeiro - BA',
    },
    {
        'sigla': 'ASTRA-Bonfim/Uauá',
        'nome': 'Assoc. dos Transportadores de Senhor do Bonfim e Uauá',
        'endereco': 'Saída BR-407, Juazeiro - BA',
    },
]


def criar_operadores():
    """Cria cooperativas e associações oficiais de Pernambuco e Bahia."""
    print('Criando cooperativas oficiais do Vale do São Francisco...')
    operadores_map = {}
    for item in COOPERATIVAS_CONFIG:
        operador = Operador.objects.create(
            nome=item['nome'],
            cnpj=fake.cnpj(),
            telefone=fake.phone_number(),
            email=f"{item['sigla'].lower().replace('-', '_')}@transporte.org.br",
            endereco=item['endereco'],
            ativo=True,
        )
        operadores_map[item['sigla']] = operador
    print(f'  {len(operadores_map)} cooperativas/associações oficiais criadas.')
    return operadores_map


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

        # Gera placas
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

    cnhs_fixas = {
        'motorista.carlos': '12345678901',
        'motorista.antonio': '23456789012',
        'motorista.jose': '34567890123',
    }

    for perfil in perfis_motorista:
        uname = perfil.usuario.username
        if uname in cnhs_fixas:
            cnh = cnhs_fixas[uname]
            cnhs_usadas.add(cnh)
            ativo = True
        else:
            while True:
                cnh = fake.numerify('###########')
                if cnh not in cnhs_usadas:
                    cnhs_usadas.add(cnh)
                    break
            ativo = random.choice([True, True, True, False])

        motorista = Motorista.objects.create(
            perfil=perfil,
            operador=random.choice(operadores),
            cnh=cnh,
            categoria_cnh=random.choice(['D', 'D', 'E']),
            ativo=ativo,
        )
        motoristas.append(motorista)
    print(f'  {len(motoristas)} motoristas criados.')
    return motoristas


# ── Rotas Oficiais do Vale do São Francisco ──────────────────
DADOS_ROTAS_REGIONAIS = [
    {
        'cooperativa': 'COOTRANSVALE',
        'cidade_a': 'Petrolina',
        'cidade_b': 'Lagoa Grande (PE)',
        'eixo': 'BR-428',
        'distancia': '~54 km',
        'preco': Decimal('20.00'),
        'paradas': [
            'Terminal Rodoviário de Petrolina',
            'Posto Trevo Petrolina (BR-428)',
            'Ponto Central de Izacolândia',
            'Rodoviária de Lagoa Grande'
        ]
    },
    {
        'cooperativa': 'COOTRANSVALE',
        'cidade_a': 'Petrolina',
        'cidade_b': 'Santa Maria da Boa Vista (PE)',
        'eixo': 'BR-428',
        'distancia': '~109 km',
        'preco': Decimal('45.00'),
        'paradas': [
            'Terminal Rodoviário de Petrolina',
            'Posto Trevo Petrolina',
            'Entrada de Lagoa Grande (BR-428)',
            'Trevo de Orocó',
            'Terminal de Santa Maria da Boa Vista'
        ]
    },
    {
        'cooperativa': 'COOTRANSVALE',
        'cidade_a': 'Petrolina',
        'cidade_b': 'Afrânio / Dormentes (PE)',
        'eixo': 'BR-407 / PE-630',
        'distancia': '~120 km',
        'preco': Decimal('35.00'),
        'paradas': [
            'Terminal Rodoviário de Petrolina',
            'Avenida Sete de Setembro',
            'Posto Fiscal de Rajada',
            'Entrada de Dormentes',
            'Terminal Central de Afrânio'
        ]
    },
    {
        'cooperativa': 'ASTRASOB',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Sobradinho (BA)',
        'eixo': 'BA-210',
        'distancia': '~48 km',
        'preco': Decimal('20.00'),
        'paradas': [
            'Terminal Rodoviário de Juazeiro',
            'Mercado do Produtor de Juazeiro',
            'Ponto da Serra da Batateira',
            'Terminal Urbano de Sobradinho'
        ]
    },
    {
        'cooperativa': 'ASTAFRAN',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Casa Nova (BA)',
        'eixo': 'BR-235',
        'distancia': '~69 km',
        'preco': Decimal('30.00'),
        'paradas': [
            'Terminal de Vans de Juazeiro',
            'Posto Fiscal Juazeiro (BR-235)',
            'Entrada de Santana do Sobrado',
            'Praça Central de Casa Nova'
        ]
    },
    {
        'cooperativa': 'ASTRA-Curaçá',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Curaçá (BA)',
        'eixo': 'BA-210',
        'distancia': '~97 km',
        'preco': Decimal('35.00'),
        'paradas': [
            'Terminal Rodoviário de Juazeiro',
            'Posto Pedra Branca (BA-210)',
            'Ponto do Barro Vermelho',
            'Rodoviária de Curaçá'
        ]
    },
    {
        'cooperativa': 'ASTRA-Bonfim/Uauá',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Uauá / Senhor do Bonfim (BA)',
        'eixo': 'BR-407 / BA-314',
        'distancia': '~110 a 130 km',
        'preco': Decimal('35.00'),
        'paradas': [
            'Terminal Rodoviário de Juazeiro',
            'Trevo de Carnaíba do Sertão',
            'Posto Fiscal de Jaguarari',
            'Terminal de Bonfim / Uauá'
        ]
    },
    {
        'cooperativa': 'ASTRASS',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Sento Sé (BA)',
        'eixo': 'BA-210',
        'distancia': '~195 km',
        'preco': Decimal('65.00'),
        'paradas': [
            'Terminal de Vans de Juazeiro',
            'Trevo de Sobradinho',
            'Distrito de Piçarrão',
            'Terminal Central de Sento Sé'
        ]
    },
    {
        'cooperativa': 'ASTAR',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Remanso / Pilão Arcado (BA)',
        'eixo': 'BR-235 / BA-309',
        'distancia': '~202 a 260 km',
        'preco': Decimal('85.00'),
        'paradas': [
            'Terminal Rodoviário de Juazeiro',
            'Santana do Sobrado',
            'Entrada de Casa Nova',
            'Rodoviária de Remanso',
            'Terminal de Pilão Arcado'
        ]
    },
    {
        'cooperativa': 'COOTRAP',
        'cidade_a': 'Petrolina',
        'cidade_b': 'Projetos Nilo Coelho / Bebedouro (PE)',
        'eixo': 'Vicinais / Projetos Irrigados',
        'distancia': '~35 km',
        'preco': Decimal('10.00'),
        'paradas': [
            'Terminal Rodoviário de Petrolina',
            'Ponto do KM 25',
            'Vila Nova N-4',
            'Projeto Maria Tereza',
            'Núcleo de Bebedouro'
        ]
    },
    {
        'cooperativa': 'COOTRANSPE',
        'cidade_a': 'Petrolina',
        'cidade_b': 'Orocó / Cabrobó / Salgueiro (PE)',
        'eixo': 'BR-428 / BR-116',
        'distancia': '~240 km',
        'preco': Decimal('60.00'),
        'paradas': [
            'Terminal Rodoviário de Petrolina',
            'Trevo de Santa Maria da Boa Vista',
            'Terminal de Orocó',
            'Rodoviária de Cabrobó',
            'Terminal Rodoviário de Salgueiro'
        ]
    },
    {
        'cooperativa': 'COOTRANSERTÃO',
        'cidade_a': 'Petrolina',
        'cidade_b': 'Distritos de Izacolândia / Rajada (PE)',
        'eixo': 'BR-428 / BR-407',
        'distancia': '~65 km',
        'preco': Decimal('15.00'),
        'paradas': [
            'Terminal Rodoviário de Petrolina',
            'Ponto Central de Izacolândia',
            'Posto Fiscal de Rajada',
            'Distrito de Pau Ferro'
        ]
    },
    {
        'cooperativa': 'COOTRANSJUA',
        'cidade_a': 'Juazeiro',
        'cidade_b': 'Distritos Maniçoba / Salitre (BA)',
        'eixo': 'Vicinais / Projetos Irrigados',
        'distancia': '~45 km',
        'preco': Decimal('10.00'),
        'paradas': [
            'Terminal de Vans de Juazeiro',
            'Mercado do Produtor de Juazeiro',
            'Ponto Central de Maniçoba',
            'Distrito de Itamotinga',
            'Região do Salitre'
        ]
    },
]


def criar_paradas():
    """Cria paradas fixas dos municípios da região."""
    print('Criando paradas reais da região de Petrolina e Juazeiro...')
    paradas_criadas = {}
    
    # Coleta todas as paradas únicas da lista
    nomes_paradas = set()
    for item in DADOS_ROTAS_REGIONAIS:
        for p in item['paradas']:
            nomes_paradas.add(p)
            
    for nome in nomes_paradas:
        parada = Parada.objects.create(
            nome=nome,
            endereco=f'{nome}, Região do São Francisco',
            latitude=Decimal(str(round(random.uniform(-9.5, -9.2), 6))),
            longitude=Decimal(str(round(random.uniform(-40.6, -40.3), 6))),
            referencia='Ponto oficial de transporte alternativo',
            ativa=True,
        )
        paradas_criadas[nome] = parada
        
    print(f'  {len(paradas_criadas)} paradas oficiais criadas.')
    return paradas_criadas


def criar_rotas(operadores_map, paradas_dict):
    """Cria rotas de ida e volta vinculadas às cooperativas correspondentes."""
    print('Criando rotas e itinerários oficiais (ida e volta)...')
    rotas = []
    precos_rotas = {}

    for item in DADOS_ROTAS_REGIONAIS:
        sigla = item['cooperativa']
        # Vincula à cooperativa oficial responsável
        operador = operadores_map.get(sigla, list(operadores_map.values())[0])
        
        # 1. Rota de Ida: A -> B
        rota_ida = Rota.objects.create(
            nome=f"{item['cidade_a']} → {item['cidade_b']}",
            descricao=f"Eixo: {item['eixo']} | Distância: {item['distancia']} | Tarifa: R$ {item['preco']}",
            operador=operador,
            ativa=True,
        )
        for ordem, p_nome in enumerate(item['paradas'], start=1):
            ParadaRota.objects.create(
                rota=rota_ida,
                parada=paradas_dict[p_nome],
                ordem=ordem,
                tempo_estimado=timedelta(minutes=random.randint(15, 45)),
            )
        rotas.append(rota_ida)
        precos_rotas[rota_ida.id] = item['preco']

        # 2. Rota de Volta: B -> A
        rota_volta = Rota.objects.create(
            nome=f"{item['cidade_b']} → {item['cidade_a']}",
            descricao=f"Eixo: {item['eixo']} | Distância: {item['distancia']} | Tarifa: R$ {item['preco']}",
            operador=operador,
            ativa=True,
        )
        for ordem, p_nome in enumerate(reversed(item['paradas']), start=1):
            ParadaRota.objects.create(
                rota=rota_volta,
                parada=paradas_dict[p_nome],
                ordem=ordem,
                tempo_estimado=timedelta(minutes=random.randint(15, 45)),
            )
        rotas.append(rota_volta)
        precos_rotas[rota_volta.id] = item['preco']

    print(f'  {len(rotas)} linhas ativas cadastradas.')
    return rotas, precos_rotas


def criar_viagens(rotas, precos_rotas, veiculos, motoristas, quantidade=120):
    """Cria viagens com os preços tabelados exatos de cada linha."""
    print(f'Criando {quantidade} viagens agendadas e operacionais...')
    if not motoristas:
        print('  Nenhum motorista disponível. Pulando viagens.')
        return []
    viagens = []
    agora = timezone.now()
    
    for _ in range(quantidade):
        rota = random.choice(rotas)
        veiculo = random.choice(veiculos)
        motorista = random.choice(motoristas)
        preco_oficial = precos_rotas.get(rota.id, Decimal('25.00'))

        # Distribui partidas entre os próximos 15 dias e os últimos 5 dias
        dias_offset = random.randint(-5, 15)
        hora = random.randint(6, 20)
        minuto = random.choice([0, 15, 30, 45])
        data_saida = agora + timedelta(days=dias_offset, hours=hora - agora.hour, minutes=minuto - agora.minute)

        if dias_offset < 0:
            status = random.choice(['concluida', 'concluida', 'cancelada'])
        else:
            status = random.choice(['agendada', 'agendada', 'agendada', 'em_andamento'])

        data_chegada = None
        if status == 'concluida':
            data_chegada = data_saida + timedelta(hours=random.randint(1, 3))

        viagem = Viagem.objects.create(
            rota=rota,
            veiculo=veiculo,
            motorista=motorista,
            data_hora_saida=data_saida,
            data_hora_chegada=data_chegada,
            status=status,
            vagas_disponiveis=random.randint(1, veiculo.capacidade),
            preco=preco_oficial,
            observacoes=f'Linha regular do eixo {rota.descricao.split("|")[0].strip()}.',
        )
        viagens.append(viagem)
        
    print(f'  {len(viagens)} viagens registradas com sucesso.')
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

    usuarios = criar_usuarios(150)
    operadores_map = criar_operadores()
    operadores_lista = list(operadores_map.values())
    veiculos = criar_veiculos(operadores_lista, 40)
    motoristas = criar_motoristas(operadores_lista, usuarios)
    paradas = criar_paradas()
    rotas, precos_rotas = criar_rotas(operadores_map, paradas)
    viagens = criar_viagens(rotas, precos_rotas, veiculos, motoristas, 120)
    reservas = criar_reservas(viagens, usuarios, 100)
    avaliacoes = criar_avaliacoes(viagens, usuarios, 70)

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
