from django.shortcuts import render, redirect
from .forms import TurnoForm,CanchaForm
from .models import Turno, User,Cancha,Horario
from datetime import date,datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def buscarTurno(request):
        
    """ select admin_turnos_horario.id , admin_turnos_horario."time" from admin_turnos_horario  where admin_turnos_horario.id 
    NOT IN (select admin_turnos_turno.time_id from admin_turnos_turno where admin_turnos_turno.date='2021-02-24')


    select  * from admin_turnos_turno inner join admin_turnos_horario on admin_turnos_horario.id = admin_turnos_turno.time_id
    where  admin_turnos_turno.date='2021-02-24'


    select * from admin_turnos_horario """

    form = TurnoForm()

    if request.method=='GET':
        context = {'form':form}
        return render(request, "turnos/buscar_turno.html", context)

    
    
    


    fecha = request.POST.get('date')
    cancha = request.POST.get('cancha')
 

    if fecha==None or cancha==None:
        return render(request, "turnos/buscar_turno.html", {'form':form,'errors':'Ingrese datos correctos'})
    
    try :
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
    except Exception  :
        error = "Ingrese una fecha correcta "
        return render(request, "turnos/buscar_turno.html", {'form':form, 'errors':error})


    if fecha_dt.isoweekday()==7:
        return render(request, "turnos/buscar_turno.html", {'form':form, 'errors':"Las canchas no se encuentran disponibles el día domingo"})
    
    

    horarios_ocupados=[]

    try:
        consulta_turnos = Turno.objects.filter(date=fecha , cancha=cancha).values('time')
    except Exception as e :
        e= "Ingrese datos correctos"
        return render(request, "turnos/buscar_turno.html", {'form':form, 'errors':e})
    

    

    for h in consulta_turnos:

        horarios_ocupados.append(h['time'])



    horarios_disponibles = Horario.objects.exclude(id__in=horarios_ocupados).order_by('time')
    

    ## Si la fecha es igual al dia actual filtro los horarios disponibles posterior a la hora en que se esta solicitando 
    if str(date.today())==fecha:
        for h2 in horarios_disponibles :
           
            if h2.time < datetime.now().time():
                
                horarios_disponibles=horarios_disponibles.exclude(time=h2.time)

    
    context = {'form':form , 'horarios_disponibles': horarios_disponibles,'fecha':fecha, 'cancha':cancha}
    return render(request, "turnos/buscar_turno.html", context)
    



@login_required(login_url='login')
def registrar_turno(request):


    print(request.POST)
    fecha=request.POST['fecha']
    hora=request.POST['hora']
    cancha=request.POST['cancha']

   

    turnoNuevo = Turno(date=fecha,time=Horario.objects.get(pk=hora),cancha=Cancha.objects.get(pk=cancha),usuario=request.user)
    turnoNuevo.save()

            
    return redirect('lista_turnos')


 

@login_required(login_url='login')
def lista_turnos(request):

    ## Antes de listar modifico el estado de los turnos de la fecha actual cuyo horario ha pasado 
    lista = Turno.objects.all()
    fecha_actual = date.today()
    hora_actual = datetime.now().time()
    for l in lista : 
        if l.date==fecha_actual and hora_actual> l.time.time:
            Turno.objects.filter(pk=l.id).update(status='finalizado')
            
            
            
     


    if request.user.is_staff:
        context ={'listado_turnos':Turno.objects.all().order_by('-date')}
    
    else:
        context ={'listado_turnos':Turno.objects.filter(usuario=request.user).order_by('-date')}
    
   

    return render(request,"turnos/turnos.html",context)



@login_required(login_url='login')
def cancelarTurno(request,id=0):
    ## Elimino el turno

    turno=Turno.objects.filter(pk=id)
    if turno.exists():
        turno.delete()
    
    return redirect('lista_turnos')
  

## Finaliza el turno (cambia el estado pendiente a finalizado)
@login_required(login_url='login')
def finalizarTurno(request,id=0):
    

    turno=Turno.objects.filter(pk=id)
    if turno.exists():
        turno.update(status='finalizado')
    
    return redirect('lista_turnos')
  
