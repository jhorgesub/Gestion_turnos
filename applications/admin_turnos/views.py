from django.shortcuts import render,redirect
from datetime import datetime
from .forms import TurnoForm
from .models import Turno
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def registrar_turno(request):

    if request.method=='GET':
        form=TurnoForm()

        return render(request,"turnos/form_registro.html",{'form':form})
    else:
        
        
        
        form= TurnoForm(request.POST)
        form.save()
        return redirect('/')





    """ 
    turno = Turno(date=datetime.now())
    turno.save() """



        
    



@login_required(login_url='login')
def lista_turnos(request):
    context ={'listado_turnos':Turno.objects.all().order_by('date')}
   

    return render(request,"turnos/turnos.html",context)



@login_required(login_url='login')
def guardar_turnos(request):
  
    return render(request,"turnos/form_registro.html")

