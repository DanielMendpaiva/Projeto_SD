from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """Perfil estendido do usuário com tipo de acesso."""
    TIPO_CHOICES = [
        ('passageiro', 'Passageiro'),
        ('motorista', 'Motorista'),
        ('gestor', 'Gestor'),
    ]
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil',
        verbose_name='Usuário'
    )
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default='passageiro',
        verbose_name='Tipo de perfil'
    )
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    cpf = models.CharField(
        max_length=14, unique=True, blank=True, null=True,
        verbose_name='CPF'
    )
    data_nascimento = models.DateField(
        null=True, blank=True, verbose_name='Data de nascimento'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['usuario__first_name']

    def __str__(self):
        nome = self.usuario.get_full_name() or self.usuario.username
        return f'{nome} ({self.get_tipo_display()})'
