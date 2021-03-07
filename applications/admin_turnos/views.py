from django.shortcuts import render, redirect
from .forms import TurnoForm,CanchaForm
from .models import Turno, User,Cancha,Horario
from datetime import date,datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url='login')
def buscarTurno(request):
        
    if request.user.is_staff:
        return redirect('lista_turnos')


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
        if (l.date==fecha_actual and hora_actual> l.time.time) or fecha_actual>l.date:
            Turno.objects.filter(pk=l.id).update(status='finalizado')
        



    ## Verifico si hay un numero de pagina especificado
    if request.method=='GET':
        npagina=request.GET.get('page')
    else:
        npagina=1

    
    ## Si el user es administrador permito la busqueda por fecha o dni o todos los turnos si dni y fecha no se especifica
    ## caso contrario listo todos los turnos correspondientes al usuario


    

    if request.user.is_staff==False:
        if request.GET.get('fecha')!=None:
            fecha=request.GET.get('fecha')
            print(fecha)

            try:
                context ={'listado_turnos':Turno.objects.filter(date=fecha,usuario=request.user).order_by('-date')}
            except Exception as e :
                return redirect('lista_turnos')  
        else : 
            context ={'listado_turnos':Turno.objects.filter(usuario=request.user).order_by('-date')}
    
    else :
        if request.GET.get('fecha')!=None:
            fecha=request.GET.get('fecha')
            print(fecha)

            try:
                context ={'listado_turnos':Turno.objects.filter(date=fecha).order_by('-date')}
            except Exception as e :
                return redirect('lista_turnos')  
        
        elif request.GET.get('dni')!=None:
            dni=request.GET.get('dni')
            try:
                context ={'listado_turnos':Turno.objects.filter(usuario=User.objects.get(username=dni)).order_by('-date')}
            except Exception as e :
                
                context ={'listado_turnos':[],'errors':"No existe el usuario buscado"}
        
        else : 
            context ={'listado_turnos':Turno.objects.all().order_by('-date')}
    

    
        




    ### Pagino los resultados 

    paginacion = Paginator(context['listado_turnos'],5)

    

    
    try:
        pag  = paginacion.page(npagina)
        context['listado_turnos']=pag
        context['current_page']=int(npagina)

    except Exception as e :

        ## Si se presenta algun inconvenietne en la paginacion (por ej una pagina que no existe ) vuelvo a la primer pagina
        if request.GET.get('fecha')!=None:
            return redirect('/turnos?page=1&fecha='+request.GET.get('fecha'))
         
        elif request.GET.get('dni')!=None:
            return redirect('/turnos?page=1&dni='+request.GET.get('dni'))
            
        else:
            return redirect('/turnos?page=1')

    
                    
        

        
    
   ## Envio la cantidad de turnos
    context['count']=paginacion.count

    return render(request,"turnos/turnos.html",context)



@login_required(login_url='login')
def cancelarTurno(request,id=0):
    ## Elimino el turno

    turno=Turno.objects.filter(pk=id)
    if turno.exists():
        turno.delete()
    
    return redirect('lista_turnos')
  



def vistante_index(request):
    if(request.user.is_authenticated):
        return redirect('lista_turnos')
    else:
        return render(request,'turnos/visitante_gestion.html')



def vistante_buscar(request):

    if(request.user.is_authenticated):

        return redirect('lista_turnos')
    
    
    else:
        form = TurnoForm()
        context = {'form':form}
        if request.method=='GET' : 
            return render(request,'turnos/visitante_busqueda.html',context)
        else :
            fecha = request.POST.get('date')
            cancha = request.POST.get('cancha')

        

            if fecha==None or cancha==None:
                return render(request, "turnos/visitante_busqueda.html", {'form':form,'errors':'Ingrese datos correctos'})
            
            try :
                fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
            except Exception  :
                error = "Ingrese una fecha correcta "
                return render(request, "turnos/visitante_busqueda.html", {'form':form, 'errors':error})


            if fecha_dt.isoweekday()==7:
                return render(request, "turnos/visitante_busqueda.html", {'form':form, 'errors':"Las canchas no se encuentran disponibles el día domingo"})
            
            

            horarios_ocupados=[]

            try:
                consulta_turnos = Turno.objects.filter(date=fecha , cancha=cancha).values('time')
            except Exception as e :
                e= "Ingrese datos correctos"
                return render(request, "turnos/visitante_busqueda.html", {'form':form, 'errors':e})
            

            

            for h in consulta_turnos:

                horarios_ocupados.append(h['time'])



            horarios_disponibles = Horario.objects.exclude(id__in=horarios_ocupados).order_by('time')
            

            ## Si la fecha es igual al dia actual filtro los horarios disponibles posterior a la hora en que se esta solicitando 
            if str(date.today())==fecha:
                for h2 in horarios_disponibles :
                
                    if h2.time < datetime.now().time():
                        
                        horarios_disponibles=horarios_disponibles.exclude(time=h2.time)

            
            context = {'form':form , 'horarios_disponibles': horarios_disponibles,'fecha':fecha, 'cancha':cancha}
            return render(request, "turnos/visitante_busqueda.html", context)






def busqueda_horarios(request):

    
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




    

    


