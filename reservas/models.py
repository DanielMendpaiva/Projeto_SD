from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Reserva(models.Model):
    """Reserva de vaga em uma viagem por um passageiro."""
    STATUS_CHOICES = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('utilizada', 'Utilizada'),
    ]
    viagem = models.ForeignKey(
        'transporte.Viagem', on_delete=models.CASCADE, related_name='reservas',
        verbose_name='Viagem'
    )
    passageiro = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservas',
        verbose_name='Passageiro'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='confirmada',
        verbose_name='Status'
    )
    quantidade_vagas = models.PositiveIntegerField(
        default=1, verbose_name='Quantidade de vagas'
    )
    data_reserva = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da reserva'
    )
    data_cancelamento = models.DateTimeField(
        null=True, blank=True, verbose_name='Data do cancelamento'
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-data_reserva']
        unique_together = [('viagem', 'passageiro')]

    def __str__(self):
        nome = self.passageiro.get_full_name() or self.passageiro.username
        return f'Reserva #{self.pk} - {nome}'


class Avaliacao(models.Model):
    """Avaliação de uma viagem realizada por um passageiro."""
    viagem = models.ForeignKey(
        'transporte.Viagem', on_delete=models.CASCADE, related_name='avaliacoes',
        verbose_name='Viagem'
    )
    passageiro = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='avaliacoes',
        verbose_name='Passageiro'
    )
    nota = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Nota (1-5)'
    )
    comentario = models.TextField(blank=True, verbose_name='Comentário')
    criada_em = models.DateTimeField(
        auto_now_add=True, verbose_name='Criada em'
    )

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-criada_em']
        unique_together = [('viagem', 'passageiro')]

    def __str__(self):
        nome = self.passageiro.get_full_name() or self.passageiro.username
        return f'Avaliação de {nome} - Nota: {self.nota}'
