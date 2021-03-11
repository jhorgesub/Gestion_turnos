from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('', views.index,name='home'),


    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutPage,name='logout'),

    path('register/', views.register,name='register'),

    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='autenticacion/password_reset.html'),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='autenticacion/password_reset_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='autenticacion/password_reset_form.html'),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='autenticacion/password_reset_done.html'),name="password_reset_complete"),
    path('usuario/editar', views.editar_perfil, name="perfil-edit"),
    path('cambiar_contraseña/', views.cambiar_contraseña, name="cambiar_contraseña"),
    path('novedades/', views.noticia, name="novedades"),
    path('novedades/<int:id>/', views.mostrar_noticia, name="detalle_noticias"),
    path('novedades/nueva', views.nueva_noticia, name="nueva_noticia"),
    path('novedades/<int:id>/editar', views.editar_noticia, name="editar_noticia"),
    path('usuarios/', views.listado_usuarios,name='listado_usuarios'),
    path('usuario/bloquear/<id>', views.bloquear_usuario,name='bloquear_usuario'),
    path('quienes_somos', views.quienes_somos, name='quienes_somos'),  
    path('usuario/avatar', views.imagen_perfil, name="imagen_perfil"),
    path('ayuda', views.ayuda, name='ayuda'),  

    

]
