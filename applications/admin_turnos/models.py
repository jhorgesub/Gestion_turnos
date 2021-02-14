from django.db import models
from applications.autenticacion.models import User
from django.contrib.auth import get_user_model

class Turno(models.Model):
    """Model definition for Turno."""

    #date = models.DateTimeField('fecha', auto_now=False, auto_now_add=False)
    date = models.DateField('date', auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,default=get_user_model())


    class Meta:
        """Meta definition for Turno."""

        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self):
        return str(self.date)
