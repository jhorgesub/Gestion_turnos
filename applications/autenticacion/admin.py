from django.contrib import admin
from django.contrib.auth.models import User
from .models import Perfil, Noticia

admin.site.register(Perfil)
admin.site.register(Noticia)

