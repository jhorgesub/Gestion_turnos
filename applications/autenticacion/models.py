from django.contrib.auth.models import User

from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('username').error_messages={'unique':"El DNI ingresado ya se encuentra registrado"}







""" 



class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dni= models.CharField('dni', max_length=50,unique=True)
    role = models.CharField("role", max_length=50,default='ROLE_USER')

    class Meta:
        

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.usuario.username + " - ROL : " + self.role
 """