

from django.shortcuts import render,redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm
)
from django.contrib.auth.models import User
from .forms import CreateUserForm, EditProfileForm, NoticiaForm, ImagenPerfilForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Noticia,Perfil
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def index(request):
    return render(request,"home.html")

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('lista_turnos')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(request, username=username,password=password)

        if user is not None :
            login(request,user)
            return redirect('lista_turnos')
        else:
            messages.error(request,'Usuario o Password incorrecto')
            return render(request,"autenticacion/login.html")
    else :
        return render(request,"autenticacion/login.html")

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('lista_turnos')

    form = CreateUserForm()
    print(form.is_valid())

    if request.method=='POST':
        form = CreateUserForm(request.POST)
        print(form.error_messages)

        if form.is_valid():
            form.save()
            user_last= User.objects.last()
            perfil = Perfil(usuario=user_last)
            perfil.save()
            messages.success(request,"La cuenta fue creada exitosamente")
            return redirect('login')

    context = {'form':form}
    return render(request,"autenticacion/register.html",context)

def editar_perfil(request):
    if request.method=='POST':
        form=EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('lista_turnos')
        else:
            errors = form.errors
            form = EditProfileForm(instance=request.user)
            args = {'form': form, "errors": errors}
            return render(request, "autenticacion/form_edit_user.html", args)
    else :
        form=EditProfileForm(instance=request.user)
        args={'form':form}
        return render(request,"autenticacion/form_edit_user.html", args)

def cambiar_contraseña(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('lista_turnos')
        else:
            return redirect('cambiar_contraseña')
    else :
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,"autenticacion/cambiar_contraseña.html", args)

def noticia(request):
    lista_noticia= Noticia.objects.all().order_by('-created')
    page = request.GET.get('page', '1')
    paginator = Paginator(lista_noticia, 5)

    try:
        noticia = paginator.page(page)
    except PageNotAnInteger:
        noticia = paginator.page(1)
    except EmptyPage:
        noticia = paginator.page(paginator.num_pages)

    return render(request, 'autenticacion/noticias.html', {'noticia': noticia})

def mostrar_noticia(request, id):
    noticia= Noticia.objects.get(id=id)
    return render(request, 'autenticacion/detalle_noticias.html', {'noticia':noticia})

def nueva_noticia(request):
    if request.method=='POST':
        form=NoticiaForm(request.POST)

        if form.is_valid():
            noticia=form.save(commit=False)
            noticia.created=timezone.now()
            noticia.save()
            return redirect('detalle_noticias', id=noticia.pk)
    else:
        form=NoticiaForm()
    return render(request, 'autenticacion/nueva_noticia.html', {'form': form})

def editar_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)

    if request.method == "POST":
        form = NoticiaForm(request.POST, instance=noticia)

        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.created = timezone.now()
            noticia.save()
            return redirect('detalle_noticias', id=noticia.pk)
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'autenticacion/nueva_noticia.html', {'form': form})

def imagen_perfil(request):
    if request.method=='POST':
        form=ImagenPerfilForm(request.POST, request.FILES, instance=request.user.perfil)

        if form.is_valid():
            form.save()
            return redirect('imagen_perfil')
    else:
        form=ImagenPerfilForm(instance=request.user.perfil)
    return render(request, 'autenticacion/insertar_imagen.html', {'form': form})

def listado_usuarios(request):
    if(request.user.is_authenticated):
        if (request.user.is_staff):
            if request.GET.get('dni')!=None:
                usuarios= User.objects.filter(is_staff=False,username=request.GET.get('dni'))
                context= {'usuarios':usuarios,'count':usuarios.count()}
                return render(request, "turnos/listado_usuarios.html", context)
            else:
                lista_usuarios= User.objects.filter(is_staff=False)
                page = request.GET.get('page', '1')
                paginator = Paginator(lista_usuarios, 5)

                try:
                    usuarios = paginator.page(page)
                except PageNotAnInteger:
                    usuarios = paginator.page(1)
                except EmptyPage:
                    usuarios = paginator.page(paginator.num_pages)
                context= {'usuarios':usuarios}
                return render(request, "turnos/listado_usuarios.html", context)
        else:
            return redirect('lista_turnos')
    else:
        return redirect('home')

def bloquear_usuario(request,id):
    perfil = Perfil.objects.get(usuario=id)
    perfil.bloqueado = not perfil.bloqueado
    perfil.save()
    return redirect('listado_usuarios')

def quienes_somos(request):
    return render (request,'autenticacion/quienes_somos.html')

def ayuda (request):
    return render (request, 'autenticacion/ayuda.html')

