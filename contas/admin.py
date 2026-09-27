from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil


class PerfilInline(admin.StackedInline):
    """Inline do perfil dentro do User admin."""
    model = Perfil
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil'
    fk_name = 'usuario'


class UserAdmin(BaseUserAdmin):
    """Admin customizado do User com perfil inline."""
    inlines = [PerfilInline]
    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'get_tipo', 'is_active', 'date_joined'
    )
    list_filter = ('is_active', 'is_staff', 'perfil__tipo')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'perfil__cpf')

    @admin.display(description='Tipo', ordering='perfil__tipo')
    def get_tipo(self, obj):
        try:
            return obj.perfil.get_tipo_display()
        except Perfil.DoesNotExist:
            return '-'


# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'telefone', 'cpf', 'criado_em')
    list_filter = ('tipo', 'criado_em')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'cpf', 'telefone')
    raw_id_fields = ('usuario',)
    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Dados do Perfil', {
            'fields': ('tipo', 'cpf', 'telefone', 'data_nascimento')
        }),
    )
    readonly_fields = ('criado_em', 'atualizado_em')
