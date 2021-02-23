from django.shortcuts import render, redirect
from datetime import datetime
from .forms import TurnoForm,CanchaForm
from .models import Turno, User,Cancha,Horario
from datetime import date
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
    fecha = request.POST.get('date')
    cancha = request.POST.get('cancha')
     
    if fecha==None or cancha==None:
        return render(request, "turnos/buscar_turno.html", {'form':form})


    horarios_ocupados=[]

    try:
        consulta_turnos = Turno.objects.filter(date=fecha , cancha=cancha).values('time')
        consulta_turnos2 = Turno.objects.filter(date=fecha , cancha=cancha).order_by('time')
    except Exception as e :
        e= "Ingrese una fecha correcta"
        return render(request, "turnos/buscar_turno.html", {'form':form, 'errors':e})


    for h in consulta_turnos:
        horarios_ocupados.append(h['time'])



    horarios_disponibles = Horario.objects.exclude(id__in=horarios_ocupados).order_by('time')
    

    
    context = {'form':form , 'horarios_disponibles': horarios_disponibles,'fecha':fecha, 'cancha':cancha}
    return render(request, "turnos/buscar_turno.html", context)
  

    if request.GET.get('date')=='' or request.GET.get('cancha')=='':
        context = {'form':form , 'errors':'Ingrese datos correctos'}
        return render(request, "turnos/buscar_turno.html", context)


    if request.method =='GET':


        if request.GET.get('date') != None and request.GET.get('cancha') != None:
            fecha = request.GET.get('date')
            cancha = request.GET.get('cancha')
            

            
            ## Hago una copia de los horarios para cada turno
            horarios = Turno.HORARIOS.copy()

            
            try:
                turnos_disponibles = Turno.objects.filter(date=fecha,cancha=cancha)
            except Exception as e: 
                context = {'form':form ,'errors':'Los datos ingresados son incorrectos incorrecta.'}
                return render(request, "turnos/buscar_turno.html", context)
            

            fecha = datetime.strptime(fecha,'%Y-%m-%d')

            if (fecha.date() - date.today()).days <0 :
                context = {'form':form ,'errors':'La fecha ingresada es antigua.'}

                return render(request, "turnos/buscar_turno.html", context)


            

            if turnos_disponibles.count()!=0:
                
                for t in turnos_disponibles:
                    for h in horarios:
                        if t.time == h[0]:
                            horarios.remove(h)
                            break

            
            
            return render(request, "turnos/buscar_turno.html", {'fecha':fecha,'horarios':horarios})

        else:
            return render(request, "turnos/buscar_turno.html", {'form':form})

    else:
        return redirect('lista_turnos')

    consulta = Turno.objects.filter(date=fecha)


        





    return redirect('registro_turnos')





@login_required(login_url='login')
def registrar_turno(request):


    print(request.POST)
    fecha=request.POST['fecha']
    hora=request.POST['hora']
    cancha=request.POST['cancha']

   

    turnoNuevo = Turno(date=fecha,time=Horario.objects.get(pk=hora),cancha=Cancha.objects.get(pk=cancha),usuario=request.user)
    turnoNuevo.save()


    
            
    return redirect('lista_turnos')


 
    
    

    if request.method=='GET':
        form=TurnoForm()
        print(request.GET)
    
            
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

        # Remover los horarios que ya esta en turno pendiente




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

