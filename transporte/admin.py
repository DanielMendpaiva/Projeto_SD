from django.contrib import admin
from .models import Operador, Veiculo, Motorista, Parada, Rota, ParadaRota, Viagem
from reservas.admin import ReservaInline, AvaliacaoInline


# ── Inlines ──────────────────────────────────────────────

class VeiculoInline(admin.TabularInline):
    """Veículos inline dentro do Operador."""
    model = Veiculo
    extra = 0
    fields = ('placa', 'modelo', 'tipo', 'capacidade', 'ano', 'ativo')


class MotoristaInline(admin.TabularInline):
    """Motoristas inline dentro do Operador."""
    model = Motorista
    extra = 0
    fields = ('perfil', 'cnh', 'categoria_cnh', 'ativo')
    raw_id_fields = ('perfil',)


class RotaInlineOperador(admin.TabularInline):
    """Rotas inline dentro do Operador."""
    model = Rota
    extra = 0
    fields = ('nome', 'descricao', 'ativa')
    show_change_link = True


class ParadaRotaInline(admin.TabularInline):
    """Paradas ordenadas inline dentro da Rota."""
    model = ParadaRota
    extra = 1
    fields = ('ordem', 'parada', 'tempo_estimado')
    ordering = ('ordem',)


class ViagemInlineRota(admin.TabularInline):
    """Viagens inline dentro da Rota."""
    model = Viagem
    extra = 0
    fields = ('data_hora_saida', 'veiculo', 'motorista', 'status', 'vagas_disponiveis', 'preco')
    show_change_link = True


# ── ModelAdmins ──────────────────────────────────────────

@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'email', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('nome', 'cnpj', 'email')
    inlines = [VeiculoInline, MotoristaInline, RotaInlineOperador]
    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'cnpj')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'tipo', 'operador', 'capacidade', 'ano', 'ativo')
    list_filter = ('tipo', 'ativo', 'operador')
    search_fields = ('placa', 'modelo', 'operador__nome')
    list_select_related = ('operador',)
    fieldsets = (
        ('Identificação', {
            'fields': ('operador', 'placa', 'modelo')
        }),
        ('Detalhes', {
            'fields': ('tipo', 'capacidade', 'ano')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'operador', 'cnh', 'categoria_cnh', 'ativo')
    list_filter = ('ativo', 'categoria_cnh', 'operador')
    search_fields = ('perfil__usuario__first_name', 'perfil__usuario__last_name', 'cnh')
    raw_id_fields = ('perfil',)
    list_select_related = ('perfil__usuario', 'operador')
    fieldsets = (
        ('Vínculo', {
            'fields': ('perfil', 'operador')
        }),
        ('Habilitação', {
            'fields': ('cnh', 'categoria_cnh')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'latitude', 'longitude', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('nome', 'endereco', 'referencia')
    fieldsets = (
        ('Identificação', {
            'fields': ('nome', 'referencia')
        }),
        ('Localização', {
            'fields': ('endereco', ('latitude', 'longitude'))
        }),
        ('Status', {
            'fields': ('ativa',)
        }),
    )


@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'operador', 'get_num_paradas', 'ativa', 'criada_em')
    list_filter = ('ativa', 'operador', 'criada_em')
    search_fields = ('nome', 'descricao', 'operador__nome')
    list_select_related = ('operador',)
    inlines = [ParadaRotaInline, ViagemInlineRota]
    fieldsets = (
        ('Informações da Rota', {
            'fields': ('nome', 'descricao', 'operador')
        }),
        ('Status', {
            'fields': ('ativa',)
        }),
    )

    @admin.display(description='Nº Paradas')
    def get_num_paradas(self, obj):
        return obj.paradas_ordenadas.count()


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'rota', 'veiculo', 'motorista', 'status',
        'vagas_disponiveis', 'preco', 'data_hora_saida'
    )
    list_filter = ('status', 'rota__operador', 'data_hora_saida')
    search_fields = (
        'rota__nome', 'veiculo__placa', 'motorista__perfil__usuario__first_name'
    )
    list_select_related = ('rota', 'veiculo', 'motorista__perfil__usuario')
    date_hierarchy = 'data_hora_saida'
    inlines = [ReservaInline, AvaliacaoInline]
    fieldsets = (
        ('Rota e Veículo', {
            'fields': ('rota', 'veiculo', 'motorista')
        }),
        ('Horários', {
            'fields': ('data_hora_saida', 'data_hora_chegada')
        }),
        ('Detalhes', {
            'fields': ('status', 'vagas_disponiveis', 'preco', 'observacoes')
        }),
    )
