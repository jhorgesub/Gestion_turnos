

from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    PasswordChangeForm
)
from django.contrib.auth.models import User
from .forms import CreateUserForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Noticia,Perfil
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
            perfil = Perfil.objects.get(usuario=request.user)
            request.FILES.get('avatar')
            perfil.save()
            return redirect('lista_turnos')
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

def mostrar_noticia(request):
    noticia=Noticia.objects.all()
    return render(request, 'autenticacion/noticias.html', {'noticia':noticia})










    

def listado_usuarios(request):

    

    if(request.user.is_authenticated):
        if (request.user.is_staff):
            if request.GET.get('dni')!=None:

                usuarios= User.objects.filter(is_staff=False,username=request.GET.get('dni'))
               
                context= {'usuarios':usuarios,'count':usuarios.count()}
                return render(request, "turnos/listado_usuarios.html", context)
            
            else:

                usuarios= User.objects.filter(is_staff=False)
                context= {'usuarios':usuarios}
                return render(request, "turnos/listado_usuarios.html", context)
        else:
            return redirect('lista_turnos')

    
    else:
        
        return redirect('home')


def bloquear_usuario(request,id):

    perfil= Perfil.objects.get(usuario=id)
    perfil.bloqueado=not perfil.bloqueado
    perfil.save()


    return redirect('listado_usuarios')


