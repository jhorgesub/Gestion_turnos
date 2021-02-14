

from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

# Create your views here.



def index(request):

    return render(request,"turnos/base_turnos.html")




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
    return redirect('login')
   

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
            
            messages.success(request,"La cuenta fue creada exitosamente")
            return redirect('login')
           
            
    
    context = {'form':form}

            
    return render(request,"autenticacion/register.html",context)
  



    

