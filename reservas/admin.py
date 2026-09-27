from django.contrib import admin
from .models import Reserva, Avaliacao


class ReservaInline(admin.TabularInline):
    """Reservas inline (usável dentro de Viagem via admin do transporte)."""
    model = Reserva
    extra = 0
    fields = ('passageiro', 'quantidade_vagas', 'status', 'data_reserva')
    readonly_fields = ('data_reserva',)
    raw_id_fields = ('passageiro',)


class AvaliacaoInline(admin.TabularInline):
    """Avaliações inline (usável dentro de Viagem via admin do transporte)."""
    model = Avaliacao
    extra = 0
    fields = ('passageiro', 'nota', 'comentario', 'criada_em')
    readonly_fields = ('criada_em',)
    raw_id_fields = ('passageiro',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'viagem', 'passageiro', 'status',
        'quantidade_vagas', 'data_reserva'
    )
    list_filter = ('status', 'data_reserva', 'viagem__rota')
    search_fields = (
        'passageiro__username', 'passageiro__first_name',
        'passageiro__last_name', 'viagem__rota__nome'
    )
    list_select_related = ('viagem__rota', 'passageiro')
    raw_id_fields = ('viagem', 'passageiro')
    date_hierarchy = 'data_reserva'
    fieldsets = (
        ('Viagem', {
            'fields': ('viagem',)
        }),
        ('Passageiro', {
            'fields': ('passageiro', 'quantidade_vagas')
        }),
        ('Status', {
            'fields': ('status', 'data_cancelamento')
        }),
    )
    readonly_fields = ('data_reserva',)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'viagem', 'passageiro', 'nota', 'criada_em')
    list_filter = ('nota', 'criada_em', 'viagem__rota')
    search_fields = (
        'passageiro__username', 'passageiro__first_name',
        'passageiro__last_name', 'viagem__rota__nome', 'comentario'
    )
    list_select_related = ('viagem__rota', 'passageiro')
    raw_id_fields = ('viagem', 'passageiro')
    fieldsets = (
        ('Viagem', {
            'fields': ('viagem',)
        }),
        ('Avaliação', {
            'fields': ('passageiro', 'nota', 'comentario')
        }),
    )
    readonly_fields = ('criada_em',)
