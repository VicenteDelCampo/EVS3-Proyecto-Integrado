from django.shortcuts import render
from .models import Mesa

def login(request):
    return render(request, 'form_login.html')

def mostrar_index(request):
    return render(request, 'index.html')
        
def mostrar_panel_admin(request):
    if request.method == "POST":
        return render(request, 'panel_admin.html')
    else:
        return render(request, "form_login.html",)

def mostrar_panel_cajero(request):
    return render(request, 'panel_cajero.html')


def mostrar_panel_mesero(request):
    return render(request, 'panel_mesero.html')


def administrar_mesas(request):
    mesa = Mesa.objects.all().values().order_by("nombre")
    datos = {"mesa" : mesa}
    return render(request, 'administrar_mesas.html', datos)


def registrar_mesa(request):
    if request.method == "POST":
        nom = request.POST["txtnommes"]
        comprobarNombreMesa = Mesa.objects.filter(nombre = nom)
        if comprobarNombreMesa:
            mesa = Mesa.objects.all().values().order_by("nombre")
            datos ={
                "r2" : "¡ La Mesa ya Existe ("+str(nom).upper()+") ya Existe !",
                "mesa" : mesa
            }
            return render(request, "administrar_mesas.html", datos)
        else:
            mesa = Mesa(nombre = nom.upper())
            mesa.save()
            mesa = Mesa.objects.all().values().order_by("nombre")
            datos ={
                "r" : "¡ Mesa ("+str(nom).upper()+") Registrado !",
                "mesa" : mesa
            }
            return render(request, "administrar_mesas.html", datos)
    else:
        mesa = Mesa.objects.all().values().order_by("nombre")
        datos ={
            "r2" : "¡ Debe Presionar el Botón del Formulario !",
            "mesa" : mesa
        }
        return render(request, "administrar_mesas.html", datos)
    
def administrar_usuarios(request):
        # usu = Usuario.objects.all().values().order_by("nombre")
        # datos = {"usu" : usu}
    return render(request, 'administrar_usuarios.html')

def administrar_pdv(request):
        # pdv = Pun_Venta.objects.all().values().order_by("nombre")
        # datos = {"pdv" : pdv}
    return render(request, 'administrar_pdv.html')

def ver_ventas(request):
    return render(request, 'ver_ventas.html')

def ver_estadisticas(request):
    return render(request, 'ver_estadisticas.html')

def jornada(request):
    return render(request, 'jornada.html')

def ver_ventas_caja(request):
    return render(request, 'ver_ventas_caja.html')

def registrar_ventas(request):
    return render(request, 'registrar_ventas.html')

def registrar_pedido(request):
    return render(request, 'registrar_pedido.html')