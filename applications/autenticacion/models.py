from django.contrib.auth.models import User

from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('username').error_messages={'unique':"El DNI ingresado ya se encuentra registrado"}

class Perfil(models.Model):
    usuario = models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/')
    bloqueado = models.BooleanField(default=False)

    class Meta:
        

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return str(self.usuario.first_name + ' ' + self.usuario.last_name + ' DNI: ' + self.usuario.username)


class Noticia(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()

    def __str__(self):
        return self.title


