from django.shortcuts import render,redirect
from datetime import datetime
from .forms import TurnoForm
from .models import Turno,User
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def buscarTurno(request):
    
        consulta = Turno.objects.filter(date=fecha, time=hora)





        return redirect('lista_turnos')





@login_required(login_url='login')
def registrar_turno(request):

 
    
    

    if request.method=='GET':
        form=TurnoForm()

        return render(request,"turnos/form_registro.html",{'form':form})
    else:

        # 2020-04-20

        fecha = request.POST['date']
        hora = request.POST['time']


        

    
        consulta = Turno.objects.filter(date=fecha, time=hora)

        if consulta==0 :
                turnoNuevo = Turno(time=hora,date=fecha)
                turnoNuevo.save()
        else :
            print("El turno se encuentra ocupado")



        print(consulta.count())
        return redirect('lista_turnos')

        

        





        form= TurnoForm(request.POST)

        ## Remover los horarios que ya esta en turno pendiente




        if form.is_valid:
            turno = form.save(commit=False)
            turno.usuario = request.user
            turno.save() 
            return redirect('lista_turnos')
        
        else:
            print(form.errors)
            return redirect('registro_turnos')


        """ form.save()
        t = Turno(date=datetime.now(),usuario=request.user)
        t.save() """





    """ 
    turno = Turno(date=datetime.now())
    turno.save() """



        
    



@login_required(login_url='login')
def lista_turnos(request):


    if request.user.is_staff:
        context ={'listado_turnos':Turno.objects.all().order_by('date')}
    
    else:
        context ={'listado_turnos':Turno.objects.filter(usuario=request.user).order_by('date')}
    
   

    return render(request,"turnos/turnos.html",context)



@login_required(login_url='login')
def guardar_turnos(request):
  
    return render(request,"turnos/form_registro.html")

