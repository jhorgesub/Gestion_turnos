from django.contrib import admin
from django.urls import path
from . import views
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('', views.lista_turnos,name='lista_turnos'),
    path('jsi18n',JavaScriptCatalog.as_view(),name='js-catalog'),
    path('registrar/', views.registrar_turno,name='registro_turnos'),
    path('buscar/', views.buscarTurno,name='buscar_turno'),
    path('cancelar/<int:id>/', views.cancelarTurno,name='cancelar_turno'),
    path('visitante', views.vistante_index,name='user_visitante'),
    path('visitante/buscar/', views.vistante_buscar,name='user_visitante_buscar'),
]
