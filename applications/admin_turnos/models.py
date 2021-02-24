from django.db import models
from applications.autenticacion.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from datetime import datetime, time



class Horario(models.Model):
  
    time = models.TimeField('time', auto_now=False, auto_now_add=False)


    # TODO: Define fields here

    class Meta:
        

        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return str(self.time)



class Cancha(models.Model):



    

    """Model definition for Cancha."""
    tipo = models.CharField('tipo', max_length=50)
    numero = models.IntegerField('numero')

    # TODO: Define fields here

    class Meta:
        """Meta definition for Cancha."""

        verbose_name = 'Cancha'
        verbose_name_plural = 'Canchas'

    def __str__(self):
        """Unicode representation of Cancha."""
        return self.tipo +" - Nro: "+ str(self.numero)








class Turno(models.Model):
    """Model definition for Turno."""



    STATUS =(
       ('pendiente', _('El turno se encuentra pendiente')),
       ('finalizado', _('El turno se encuentra finalizado')),
        )



    date = models.DateField('date', auto_now=False, auto_now_add=False)
    time = models.ForeignKey(Horario, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    status = models.CharField(
       max_length=32,
       choices=STATUS,
       default='pendiente',
   )



    class Meta:
        """Meta definition for Turno."""

        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self):
        return str(self.date) + "- "+ str(self.time) + "- "+ str(self.cancha)
