from django.contrib.auth.models import User

from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('username').error_messages={'unique':"El DNI ingresado ya se encuentra registrado"}




""" 

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('avatar', upload_to=None, height_field=None, width_field=None, max_length=None)

    class Meta:
        

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.usuario.username + self.usuario.first_name + self.usuario.last_name
"""