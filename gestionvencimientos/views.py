from django.shortcuts import render, redirect
from django.http.response import HttpResponse
import holidays_co
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from gestionvencimientos.models import *
from regional.models import Regional

@login_required
def index(request):
    return render(request,  "index.html")

@login_required
def ir_a_seleccion_region(request):
    regiones = Regional.objects.all()
    return render(request,  "seleccionar_regional.html", {'regiones':regiones})

def calculo_dia_actutal():
    
    fecha_actual = datetime.now()
    dia = 0

    if fecha_actual.weekday() == 1:
        dia = 1

    if fecha_actual.weekday() == 2:
        dia = 2

    if fecha_actual.weekday() == 3:
        dia = 3

    if fecha_actual.weekday() == 4:
        dia = 4
    
    if fecha_actual.weekday() == 5:
        dia = 5
    
    if fecha_actual.weekday() == 6:
        dia = 6

    return dia

def calculo_dia_semana_2():
    
    fecha_actual = datetime.now()
    lunes = datetime.now()

    if fecha_actual.weekday() == 0:
        lunes = datetime.now()

    if fecha_actual.weekday() == 1:
        lunes = datetime.now()-timedelta(days=1)

    if fecha_actual.weekday() == 2:
        lunes = datetime.now()-timedelta(days=2)

    if fecha_actual.weekday() == 3:
        lunes = datetime.now()-timedelta(days=3)

    if fecha_actual.weekday() == 4:
        lunes = datetime.now()-timedelta(days=4)
    
    if fecha_actual.weekday() == 5:
        lunes = datetime.now()+timedelta(days=2)
    
    if fecha_actual.weekday() == 6:
        lunes = datetime.now()+timedelta(days=1)

    return lunes

@login_required
def menu_pendientes(self):
    id_dia = calculo_dia_actutal()+1
    
    return redirect('pendientes', id_dia)

@login_required
def limpiar_base(request):

    aneses = Ans.objects.all().only('Subzona', 'Actividad')

    if request.method == 'POST':
        id = request.POST["id_region"]

    for ans in aneses:
        if ans.Subzona != Regional.objects.get(id=id).regional:
            ans.delete()

        elif ans.Actividad != "FSE" and ans.Actividad != "INFSM" and ans.Actividad != "ACREV" and ans.Actividad != "AEJDO" and ans.Actividad != "ARTER" and ans.Actividad != "DIPRE" and ans.Actividad != "INPRE" and ans.Actividad != "REEQU" and ans.Actividad != "APLIN" and ans.Actividad != "ALEGA" and ans.Actividad != "ALEGN" and ans.Actividad != "ALECA" and ans.Actividad != "ACAMN" and ans.Actividad != "AMRTR":
            ans.delete()

    return redirect("gestionbd")

@login_required
def calculo_pendientes(request, id_dia):

    lunes = calculo_dia_semana_2()
    encargados = Encargado.objects.all()

    if id_dia == 1:

        list_ans = busqueda_pendientes(lunes.strftime('%Y-%m-%d'))

        return render(request, "pendientes_lunes.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': lunes.strftime('%Y-%m-%d')})

    if id_dia == 2:

        list_ans = busqueda_pendientes((lunes+timedelta(days=1)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_lunes.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=1)).strftime('%Y-%m-%d')})

    if id_dia == 3:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=2)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_lunes.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=2)).strftime('%Y-%m-%d')})

    if id_dia == 4:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=3)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_lunes.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=3)).strftime('%Y-%m-%d')})

    if id_dia == 5:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=4)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_lunes.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=4)).strftime('%Y-%m-%d')})
    
    if id_dia == 6 or id_dia == 7:
    
        list_ans = busqueda_pendientes(
            (lunes).strftime('%Y-%m-%d'))

        return render(request, "pendientes_lunes.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes).strftime('%Y-%m-%d')})

@login_required
def busqueda_vencidos(request):
    aneses = Ans.objects.filter(Estado="PENDI")
    list_ans = []
    for ans in aneses:
        if ans.Estado == "PENDI" and ans.Concepto == "PENDI":
            continue
        if ans.Estado == "PENDI" and ans.Concepto == "592":
            continue
        if ans.Tipo_Elemento_ID == "ENEGED":
            continue
        try:
            fecha_vence_ans = datetime.strptime(ans.fecha_vencimiento, "%Y-%m-%d %H:%M:%S")
            if fecha_vence_ans < datetime.today():
                if ans.estado_cierre == 0:
                    list_ans.append(ans)
        except Exception as e: 
            print("An exception occurred in fecha vencimiento 2") 
            print(repr(e))                              

    return render(request, "vencidos-todos.html" , {"aneses": list_ans})

def busqueda_pendientes(fecha_vence_buscar):
    aneses = Ans.objects.filter(Estado="PENDI")
    list_ans = []
    for ans in aneses:
        if ans.Estado == "PENDI" and ans.Concepto == "PENDI":
            continue
        if ans.Estado == "PENDI" and ans.Concepto == "592":
            continue
        try:
            fecha_vence_ans = datetime.strptime(ans.fecha_vencimiento, "%Y-%m-%d %H:%M:%S")
            if fecha_vence_ans.strftime('%Y-%m-%d') == fecha_vence_buscar:
                if ans.estado_cierre == 0:
                    list_ans.append(ans) 
        except Exception as e: 
            print("An exception occurred in busqueda pendientes") 
            print(repr(e)) 

    list_ans = cambiar_formato_fecha(list_ans) 
    
    return list_ans

def cambiar_formato_fecha(fecha_a_cambiar):
    for l in fecha_a_cambiar:
        if l.fecha_vencimiento==None or l.fecha_vencimiento=='0' :
            pass
        else:
            fecha = l.fecha_vencimiento.replace('-','/')
            fecha_vencimiento   = datetime.strptime(fecha, "%Y/%m/%d %H:%M:%S")
            l.fecha_vencimiento = fecha_vencimiento.strftime("%d/%m/%Y %H:%M:%S")
    
    return fecha_a_cambiar

def cambiar_formato_fecha_epm(fecha_a_cambiar):
    for l in fecha_a_cambiar:
        if l.fecha_vencimiento==None or l.fecha_vencimiento=='0' :
            pass
        else:
            fecha = l.fecha_vencimiento.replace('-','/')
            fecha_vencimiento   = datetime.strptime(fecha, "%Y/%m/%d %H:%M:%S")
            l.fecha_vencimiento = fecha_vencimiento.strftime("%d/%m/%Y %H:%M:%S")

            fecha2 = l.fecha_vence_epm.replace('-','/')
            fecha_vencimiento_epm   = datetime.strptime(fecha2, "%Y/%m/%d %H:%M:%S")
            l.fecha_vence_epm = fecha_vencimiento_epm.strftime("%d/%m/%Y %H:%M:%S")

            l.fecha_vence_sin_hora = fecha_vencimiento_epm.strftime("%d/%m/%Y")
    
    return fecha_a_cambiar

@login_required
def eliminar_bd(request):
    Ans.objects.all().delete()

    return redirect('home')

def fechas(fecha_inic, dias):

    fecha_vencimiento = datetime. strptime(fecha_inic, '%Y-%m-%d %H:%M:%S')
    cont = 0

    while cont < dias:

        fecha_vencimiento = fecha_vencimiento+timedelta(days=1)

        if es_festivo_o_fin_de_semana(fecha_vencimiento):
            continue
        else:
            cont = cont+1

    return fecha_vencimiento

def es_festivo_o_fin_de_semana(fecha):
    if holidays_co.is_holiday_date(fecha):
        return True
    if fecha.weekday() == 5 or fecha.weekday() == 6:
        return True

@login_required
def gestion_bd(request): 
     
    lista_ans = []
    Ans.objects.filter(Estado ="ANULA").delete()
    Ans.objects.filter(Estado = "PENDI").filter(Concepto = "PENDI").delete()
    
    anses = Ans.objects.all()
    
    for ans in anses:
        
        if ans.Actividad != "DSPRE"  and ans.Actividad != "AEJDO" and ans.Actividad != "ACREV" and ans.Actividad != "ARTER" and ans.Actividad != "DIPRE" and ans.Actividad != "ACREV" and ans.Actividad != "INPRE" and ans.Actividad != "REEQU" and ans.Actividad != "APLIN" and ans.Actividad != "ALEGA" and ans.Actividad != "ALEGN" and ans.Actividad != "ALECA" and ans.Actividad != "ACAMN" and ans.Actividad != "AMRTR":
            ans.delete()
            
        if ans.Concepto != "INFSM" and ans.Concepto != "498" and ans.Concepto != "406" and ans.Concepto != "414" and ans.Concepto != "430" and ans.Concepto != "495" and ans.Concepto != "PENDI" and ans.Concepto != "FSE" and ans.Concepto != "PPRG" and ans.Concepto != "PROG":
            ans.delete()

    aneses = Ans.objects.all()

    for ans in aneses:

        try:
            if ans.Instalación[7:10] == "100":
                ans.Tipo_Dirección = "Urbano"
                ans.save()
            if ans.Instalación[7:10] == "200":
                ans.Tipo_Dirección = "Rural"
                ans.save()

            if ans.Fecha_Inicio_ANS == "":
                ans.Fecha_Inicio_ANS = ans.Fecha_Concepto
                ans.save()

            actividad = Actividad.objects.get(nombre=ans.Actividad)
            actividad_epm = Actividad_epm.objects.get(nombre=ans.Actividad)
            
            if ans.Tipo_Dirección == "Urbano":
                ans.dias_vencimiento = int(actividad.dias_urbano)
                ans.dias_vencimiento_epm = int(actividad_epm.dias_urbano)
            if ans.Tipo_Dirección == "Rural":
                ans.dias_vencimiento = int(actividad.dias_rural)
                ans.dias_vencimiento_epm = int(actividad_epm.dias_rural)

            fecha = fechas(ans.Fecha_Inicio_ANS, ans.dias_vencimiento)
            ans.fecha_vencimiento = fecha
            
            fecha_epm = fechas(ans.Fecha_Inicio_ANS, ans.dias_vencimiento_epm)
            ans.fecha_vence_epm = fecha_epm
            ans.fecha_vence_sin_hora = fecha.date().strftime("%d-%m-%Y")
            
            # inicio calculo vence epm
            
            # fin calculo vence epm
    
            ans.hora_vencimiento= fecha.time()

            ans.encargado = str(actividad.encargado)

            ans.save()

        except Exception as e: 
            print("error gestion bd")
            print(e)  

    return redirect('menu_pendientes')

@login_required
def cerrar_pedido(request, id_pedido):
   
    ans_cerrar = Ans.objects.get(id=id_pedido)

    ans_cerrar.estado_cierre = 1
    ans_cerrar.save()

    return redirect('menu_pendientes')

@login_required
def calculo_next_week(request, id_dia):
    
    lunes = calculo_dia_semana_2()
    encargados = Encargado.objects.all()
    if id_dia == 10:

        list_ans =  list_ans = busqueda_pendientes(
            (lunes+timedelta(days=7)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_next_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=7)).strftime('%Y-%m-%d')})

    if id_dia == 20:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=8)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_next_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=8)).strftime('%Y-%m-%d')})

    if id_dia == 30:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=9)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_next_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=9)).strftime('%Y-%m-%d')})

    if id_dia == 40:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=10)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_next_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=10)).strftime('%Y-%m-%d')})

    if id_dia == 50:

        list_ans = busqueda_pendientes(
            (lunes+timedelta(days=11)).strftime('%Y-%m-%d'))

        return render(request, "pendientes_next_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=11)).strftime('%Y-%m-%d')})

@login_required
def vencidos(request):
    aeneses = Vencido.objects.all()
        
    return render(request, "vencidos.html", {"aneses":aeneses})

@login_required
def vencimientos_epm(request, inicio, final):
    fecha_inicio = inicio+" "+"00:00:00"
    fecha_final = final+" "+"23:59:59"
    aeneses=[]
    ans = Ans.objects.all()
    for a in ans:
        if a.fecha_vence_epm>fecha_inicio and a.fecha_vence_epm<fecha_final:
            aeneses.append(a)
    aeneses = cambiar_formato_fecha_epm(aeneses)    
    return render(request, "pendientes_epm.html", {"aneses":aeneses})

@login_required
def pedidos_week(request, id_week):
    
    lunes = calculo_dia_semana_2()
    
    encargados = Encargado.objects.all()
    
    dia=0
    
    if id_week==2:
        dia=7
        list_ans_lunes = busqueda_pendientes((lunes+timedelta(days=dia)).strftime('%Y-%m-%d'))
    else:
        list_ans_lunes = busqueda_pendientes(lunes.strftime('%Y-%m-%d'))
        
    
    list_ans_martes = busqueda_pendientes((lunes+timedelta(days=dia+1)).strftime('%Y-%m-%d'))
    list_ans_lunes.extend(list_ans_martes)
    
    list_ans_miercoles = busqueda_pendientes((lunes+timedelta(days=dia+2)).strftime('%Y-%m-%d'))
    list_ans_miercoles.extend(list_ans_lunes)
    
    list_ans_jueves = busqueda_pendientes((lunes+timedelta(days=dia+3)).strftime('%Y-%m-%d'))
    list_ans_miercoles.extend(list_ans_jueves)
    
    
    list_ans_viernes = busqueda_pendientes((lunes+timedelta(days=dia+4)).strftime('%Y-%m-%d'))
    list_ans_miercoles.extend(list_ans_viernes)
    
    if id_week==2:
        viernes = (lunes+timedelta(days=dia+4)).strftime('%d-%m-%Y')
        lunes = (lunes+timedelta(days=7)).strftime('%d-%m-%Y')
    else:
        viernes = (lunes+timedelta(days=dia+4)).strftime('%d-%m-%Y')
        lunes = lunes.strftime('%d-%m-%Y') 
    
    lista_pedidos = list_ans_miercoles

    return render(request, "pedidos_week.html", {"aneses":lista_pedidos, "lunes":lunes, "viernes":viernes})

@login_required
def otros_pedidos(request, cliente, apla, pendi):
    
    if cliente == 1 and apla == 0 and pendi == 0:
          vencidos = Ans.objects.filter(Estado = "CLIEN")
          return render(request, "otros_pedidos.html", {"aneses": vencidos})
        
    if cliente == 0 and apla == 2 and pendi == 0:
        vencidos = Ans.objects.filter(Estado = "APLAZ")
        return render(request, "otros_pedidos.html", {"aneses": vencidos})
        
    if cliente == 0 and apla == 0 and pendi == 3:
        vencidos = Ans.objects.filter(Estado = "PENDI")
        return render(request, "otros_pedidos.html", {"aneses": vencidos})
            
    if cliente == 1 and apla == 2 and pendi == 0:
        vencidos = Ans.objects.filter(Q(Estado="CLIEN") | Q(Estado="APLAZ"))
        return render(request, "otros_pedidos.html", {"aneses": vencidos})
                
    if cliente == 0 and apla == 2 and pendi == 3:
        vencidos = Ans.objects.filter(Q(Estado="PENDI") | Q(Estado="APLAZ"))
        return render(request, "otros_pedidos.html", {"aneses": vencidos})
            
    if cliente == 1 and apla == 0 and pendi == 3:
        vencidos = Ans.objects.filter(Q(Estado="PENDI") | Q(Estado="CLIEN"))
        return render(request, "otros_pedidos.html", {"aneses": vencidos})
            
    if cliente == 1 and apla == 2 and pendi == 3:
        vencidos = Ans.objects.filter(Q(Estado="PENDI") | Q(Estado="CLIEN") | Q(Estado="APLAZ"))
        return render(request, "otros_pedidos.html", {"aneses": vencidos})
    
    return HttpResponse("Error en la consulta de otros pedidos")

@login_required
def acrev(request):
    
    aeneses = Ans.objects.filter(Actividad = "ACREV").filter(Q(Estado="PENDI") | Q(Concepto="406") | Q(Concepto="414")| Q(Concepto="495")| Q(Concepto="430"))
    aeneses = cambiar_formato_fecha(aeneses)
    return render(request, "acrev.html", {"aneses": aeneses} )

@login_required
def inconsistencias(request):
    
    aeneses1 = Ans.objects.filter(Concepto='FSE') 
    aeneses2 = Ans.objects.filter(Concepto='INFSM')
    aenese=[]
    print(len(aeneses2))
    for a in aeneses1:
        aenese.append(a)
    for ae in aeneses2:
        aenese.append(ae)
    
    aeneses = cambiar_formato_fecha(aenese)
    return render(request, "inconsistencias.html", {"aneses": aeneses} )

@login_required
def calculo_last_week(request, id_dia):
    
    lunes = calculo_dia_semana_2()
    encargados = Encargado.objects.all()
    if id_dia == 10:

        list_ans =  list_ans = busqueda_pendientes((lunes-timedelta(days=7)).strftime('%Y-%m-%d'))
        return render(request, "pendientes_last_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=7)).strftime('%Y-%m-%d')})

    if id_dia == 20:

        list_ans = busqueda_pendientes((lunes-timedelta(days=6)).strftime('%Y-%m-%d'))
        return render(request, "pendientes_last_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=8)).strftime('%Y-%m-%d')})

    if id_dia == 30:

        list_ans = busqueda_pendientes((lunes-timedelta(days=5)).strftime('%Y-%m-%d'))
        return render(request, "pendientes_last_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=9)).strftime('%Y-%m-%d')})

    if id_dia == 40:

        list_ans = busqueda_pendientes((lunes-timedelta(days=4)).strftime('%Y-%m-%d'))
        return render(request, "pendientes_last_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=10)).strftime('%Y-%m-%d')})

    if id_dia == 50:

        list_ans = busqueda_pendientes((lunes-timedelta(days=3)).strftime('%Y-%m-%d'))
        return render(request, "pendientes_last_week.html", {'id_dia':id_dia,'encargados': encargados,'aneses': list_ans, 'total': len(list_ans), 'fecha': (lunes+timedelta(days=11)).strftime('%Y-%m-%d')})


