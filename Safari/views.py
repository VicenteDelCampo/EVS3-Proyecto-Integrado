from django.shortcuts import render
from datetime import datetime
from .models import Usuario, Historial, Mesa, Clases, PuntodeVenta, Producto, Ticket


def mostrar_index(request):
    return render(request, 'index.html')

def mostrar_login(request):
    return render(request, 'form_login.html')

def login(request):
    if request.method == "POST":
        nom = request.POST["txtusu"]
        pas = request.POST["txtpas"]

        comprobar_login = Usuario.objects.filter(nombre=nom, password=pas).values('id', 'nombre', 'clase__nombre')
        if comprobar_login.exists():
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobar_login[0]["id"]
            request.session["nomUsuario"] = nom.upper()

            clas = comprobar_login[0]["clase__nombre"].upper()
            request.session["claseUsuario"] = clas

            descripcion = "Sesión iniciada"
            tabla = ""
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(
                descripcion_historial = descripcion,
                tabla_afectada_historial = tabla,
                fecha_hora_historial = fechayhora,
                usuario_id = usuario
            )
            his.save()
            
            if clas.upper() == "ADMINISTRADOR":
                datos = { "nomUsuario" : nom.upper() }
                return render(request, "panel_admin.html", datos)
            elif clas.upper() == "MESERO":
                datos = { "nomUsuario" : nom.upper() }
                return render(request, "panel_mesero.html", datos)
            elif clas.upper() == "CAJERO":
                datos = { "nomUsuario" : nom.upper() }
                return render(request, "panel_cajero.html", datos)
        else:
            datos = { "r2" : "¡ Error de Usuario y/o Contraseña !" }
            return render(request, "form_login.html", datos)

    else:
        datos = { "r2" : "¡ No se Puede Procesar la Solicitud !" }
        return render(request, "form_login.html", datos)
    return render(request, 'form_login.html')
        
def cerrar_sesion(request):
    try:
        descripcion = "Sesión cerrada"
        tabla = ""
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(
            descripcion_historial = descripcion,
            tabla_afectada_historial = tabla,
            fecha_hora_historial = fechayhora,
            usuario_id = usuario
        )
        his.save()

        #request.session.flush()
        del request.session["idUsuario"]
        del request.session["nomUsuario"]
        del request.session["estadoSesion"]
        del request.session["claseUsuario"]
        datos = { "r" : "¡ Sesión Cerrada Correctamente !" }
        return render(request, "index.html", datos)
    except:
        datos = { "r2" : "¡ No se Encuentra una Sesión Activa !" }
        return render(request, "index.html", datos)
        

def mostrar_panel_cajero(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "CAJERO":
            datos = { "nomUsuario" : nomUsuario }
            return render(request, 'panel_cajero.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
    
    
def mostrar_panel_mesero(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "MESERO":
            datos = { "nomUsuario" : nomUsuario }
            return render(request, 'panel_mesero.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def mostrar_panel_admin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            datos = { "nomUsuario" : nomUsuario }
            return render(request, 'panel_admin.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)


def administrar_mesas(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "MESERO":
            mesa = Mesa.objects.all().values().order_by("nombre")
            datos = {"mesa" : mesa, "nomUsuario" : nomUsuario}
            return render(request, 'administrar_mesas.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)


def administrar_admin_mesas(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            mesa = Mesa.objects.all().values().order_by("nombre")
            datos = {"mesa" : mesa, "nomUsuario" : nomUsuario}
            return render(request, 'administrar_admin_mesas.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)


def registrar_mesa_admin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnommes"]
                comprobarNombreMesa = Mesa.objects.filter(nombre = nom)
                if comprobarNombreMesa:
                    mesa = Mesa.objects.all().values().order_by("nombre")
                    datos ={
                        "r2" : "¡ La Mesa ya Existe ("+str(nom).upper()+") ya Existe !",
                        "mesa" : mesa
                    }
                    return render(request, "administrar_admin_mesas.html", datos)
                else:
                    mesa = Mesa(
                        nombre=nom, 
                        usuario_id=idUsuario
                    )
                    mesa.save()
                    descripcion = f"Mesa Registrada ({ mesa.id })"
                    tabla = "safari_mesa"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = usuario
                    )
                    his.save()
                    mesa = Mesa.objects.all().values().order_by("nombre")
                    datos = {
                        "mesa" : mesa,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Mesa Creada ({ mesa.id }) !"
                    }
                    return render(request, "administrar_admin_mesas.html", datos)
            else:
                mesa = Mesa.objects.all().values().order_by("nombre")
                datos ={
                    "r2" : "¡ Debe Presionar el Botón del Formulario !",
                    "mesa" : mesa
                }
                return render(request, "administrar_admin_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
        

def registrar_mesa(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "MESERO":
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
                    mesa = Mesa(
                        nombre=nom, 
                        usuario_id=idUsuario
                    )
                    mesa.save()
                    descripcion = f"Mesa Registrada ({ mesa.id })"
                    tabla = "safari_mesa"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = usuario
                    )
                    his.save()
                    mesa = Mesa.objects.all().values().order_by("nombre")
                    datos = {
                        "mesa" : mesa,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Mesa Creada ({ mesa.id }) !"
                    }
                    return render(request, "administrar_mesas.html", datos)
            else:
                mesa = Mesa.objects.all().values().order_by("nombre")
                datos ={
                    "r2" : "¡ Debe Presionar el Botón del Formulario !",
                    "mesa" : mesa
                }
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
    
    
def administrar_usuarios(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            usu = Usuario.objects.all().values().order_by("nombre")
            opciones_clases = Clases.objects.all().values().order_by("nombre")
            datos = {"usu" : usu,
                    "nomUsuario": nomUsuario, "opciones_clases" : opciones_clases}
            return render(request, 'administrar_usuarios.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def registrar_usuario(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnomusu"]
                con = request.POST["txtconusu"]
                cla = request.POST["cboclausu"]
                usu = Usuario(
                    nombre=nom,
                    password=con,
                    clase=cla
                )
                usu.save()

                descripcion = f"Registro insertado ({ usu.id })"
                tabla = "tickets_ticket"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(
                    descripcion_historial = descripcion,
                    tabla_afectada_historial = tabla,
                    fecha_hora_historial = fechayhora,
                    usuario_id = usuario
                )
                his.save()


                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "r" : f"¡ Usuario Creado ({ usu.id }) !"
                }
                return render(request, "administrar_usuarios.html", datos)
            
            else:
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "opciones_clases" : opciones_clases }
                return render(request, "administrar_usuarios.html", datos)
        
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def form_act_usu(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")

    rs = Usuario.objects.filter(id = id)
    
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if rs :
                usu = Usuario.objects.select_related('clase').order_by("nombre")
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = { "rs":rs,"usu" : usu, "nomUsuario" : nomUsuario, "opciones_clases" : opciones_clases} 
                return render(request, "actualizar_usuarios.html", datos)
            else:
                usu = Usuario.objects.select_related('clase').order_by("nombre")
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = { "r2" : "El id del Usuario ("+str(id)+") No Existe. Imposibre Eliminar" , "usu" : usu, "nomUsuario" : nomUsuario, "opciones_clases" : opciones_clases} 
                return render(request, "administrar_usuarios.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
        
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def actualizar_usuario(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":

            if request.method == "POST":
                nom = request.POST["txtnomusu"]
                con = request.POST["txtconusu"]
                cla = request.POST["cboclausu"]
                usu = Usuario.objects.get(id=id)
                usu.nombre = nom
                usu.password = con
                usu.clase_id = cla
                usu.save()

                id_usu = usu.id


                descripcion = f"Registro modificado ({ id_usu })"
                tabla = "safari_usuario"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(
                    descripcion_historial = descripcion,
                    tabla_afectada_historial = tabla,
                    fecha_hora_historial = fechayhora,
                    usuario_id = usuario
                )
                his.save()


                opciones_clases = Clases.objects.all().values().order_by("nombre")
                usu = Usuario.objects.select_related('clase').filter().order_by("-id")
                datos = {
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "usu" : usu,
                    "r" : f"¡ Usuario ({ id_usu }) Modificado Correctamente !"
                }

                return render(request, "administrar_usuarios.html", datos)
            
            else:
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                usu = Usuario.objects.select_related('clase').filter(usuario__nombre=nomUsuario).order_by("-id")
                datos = {
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "usu" : usu,
                    "r2" : "¡ No Se Puede Procesar La Solicitud !"
                }
                return render(request, "administrar_usuarios.html", datos)
        
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
        
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
    
    
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