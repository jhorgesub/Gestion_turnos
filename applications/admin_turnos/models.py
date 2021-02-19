from django.db import models
from applications.autenticacion.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from datetime import datetime, time




class Turno(models.Model):
    """Model definition for Turno."""



    STATUS =(
       ('pendiente', _('El turno se encuentra pendiente')),
       ('finalizado', _('El turno se encuentra finalizado')),
       ('cancelado', _('El turno se encuentra cancelado')),
        )

    HORARIOS =[
       (time(8, 00, 00), '8:00 hs'),
       (time(9, 00, 00), '9:00 hs'),
       (time(10, 00, 00), '10:00 hs'),
       (time(11, 00, 00), '11:00 hs'),
       (time(17, 00, 00), '17:00 hs'),
       (time(18, 00, 00), '18:00 hs'),
       (time(19, 00, 00), '19:00 hs'),
    ]


    date = models.DateField('date', auto_now=False, auto_now_add=False)
    time = models.TimeField('time', auto_now=False, auto_now_add=False,default=datetime.now(),choices=HORARIOS)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return str(self.date)



