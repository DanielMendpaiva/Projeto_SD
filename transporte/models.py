from django.db import models


class Operador(models.Model):
    """Cooperativa ou empresa operadora de transporte alternativo."""
    nome = models.CharField(max_length=200, verbose_name='Nome')
    cnpj = models.CharField(max_length=18, unique=True, verbose_name='CNPJ')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    endereco = models.TextField(blank=True, verbose_name='Endereço')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    """Veículo utilizado no transporte alternativo."""
    TIPO_CHOICES = [
        ('van', 'Van'),
        ('micro_onibus', 'Micro-ônibus'),
        ('lotacao', 'Lotação'),
        ('onibus', 'Ônibus'),
    ]
    operador = models.ForeignKey(
        Operador, on_delete=models.CASCADE, related_name='veiculos',
        verbose_name='Operador'
    )
    placa = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default='van',
        verbose_name='Tipo'
    )
    capacidade = models.PositiveIntegerField(verbose_name='Capacidade (passageiros)')
    ano = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ano')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']

    def __str__(self):
        return f'{self.placa} - {self.modelo} ({self.get_tipo_display()})'


class Motorista(models.Model):
    """Motorista vinculado a um operador."""
    perfil = models.OneToOneField(
        'contas.Perfil', on_delete=models.CASCADE, related_name='motorista',
        verbose_name='Perfil'
    )
    operador = models.ForeignKey(
        Operador, on_delete=models.CASCADE, related_name='motoristas',
        verbose_name='Operador'
    )
    cnh = models.CharField(max_length=20, unique=True, verbose_name='CNH')
    categoria_cnh = models.CharField(
        max_length=5, default='D', verbose_name='Categoria CNH'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'
        ordering = ['perfil__usuario__first_name']

    def __str__(self):
        return f'{self.perfil.usuario.get_full_name()} - CNH: {self.cnh}'


class Parada(models.Model):
    """Ponto de parada de uma rota."""
    nome = models.CharField(max_length=200, verbose_name='Nome')
    endereco = models.TextField(blank=True, verbose_name='Endereço')
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        verbose_name='Latitude'
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        verbose_name='Longitude'
    )
    referencia = models.CharField(
        max_length=300, blank=True, verbose_name='Ponto de referência'
    )
    ativa = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Parada'
        verbose_name_plural = 'Paradas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Rota(models.Model):
    """Rota de transporte alternativo."""
    nome = models.CharField(max_length=200, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    operador = models.ForeignKey(
        Operador, on_delete=models.CASCADE, related_name='rotas',
        verbose_name='Operador'
    )
    paradas = models.ManyToManyField(
        Parada, through='ParadaRota', related_name='rotas',
        verbose_name='Paradas'
    )
    ativa = models.BooleanField(default=True, verbose_name='Ativa')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')

    class Meta:
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ParadaRota(models.Model):
    """Relação ordenada entre Parada e Rota (through table)."""
    rota = models.ForeignKey(
        Rota, on_delete=models.CASCADE, related_name='paradas_ordenadas',
        verbose_name='Rota'
    )
    parada = models.ForeignKey(
        Parada, on_delete=models.CASCADE, verbose_name='Parada'
    )
    ordem = models.PositiveIntegerField(verbose_name='Ordem')
    tempo_estimado = models.DurationField(
        null=True, blank=True,
        verbose_name='Tempo estimado desde a parada anterior',
        help_text='Formato: HH:MM:SS'
    )

    class Meta:
        verbose_name = 'Parada da Rota'
        verbose_name_plural = 'Paradas da Rota'
        ordering = ['rota', 'ordem']
        unique_together = [('rota', 'ordem'), ('rota', 'parada')]

    def __str__(self):
        return f'{self.rota.nome} - {self.ordem}ª: {self.parada.nome}'


class Viagem(models.Model):
    """Uma viagem agendada ou realizada em uma rota."""
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    rota = models.ForeignKey(
        Rota, on_delete=models.CASCADE, related_name='viagens',
        verbose_name='Rota'
    )
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE, related_name='viagens',
        verbose_name='Veículo'
    )
    motorista = models.ForeignKey(
        Motorista, on_delete=models.CASCADE, related_name='viagens',
        verbose_name='Motorista'
    )
    data_hora_saida = models.DateTimeField(verbose_name='Data/hora de saída')
    data_hora_chegada = models.DateTimeField(
        null=True, blank=True, verbose_name='Data/hora de chegada'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='agendada',
        verbose_name='Status'
    )
    vagas_disponiveis = models.PositiveIntegerField(
        verbose_name='Vagas disponíveis'
    )
    preco = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Preço (R$)'
    )
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')

    class Meta:
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'
        ordering = ['-data_hora_saida']

    def __str__(self):
        return f'{self.rota.nome} - {self.data_hora_saida.strftime("%d/%m/%Y %H:%M")}'
