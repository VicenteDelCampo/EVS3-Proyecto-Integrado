from django.shortcuts import render
from datetime import datetime
from .models import Usuario, Historial, Mesa, Clases, PuntodeVenta, Producto, Estado, Venta, DetalleVenta, JornadaCaja
from django.db.models import Sum, Count, F

def mostrar_index(request):
    return render(request, 'index.html')

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
            return render(request, "index.html", datos)
    else:
        datos = { "r2" : "¡ No se Puede Procesar la Solicitud !" }
        return render(request, "index.html", datos)
    return render(request, 'index.html')

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
        if claseUsuario.upper() == "MESERO" or claseUsuario.upper() == "ADMINISTRADOR":
            mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
            opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
            datos = {"mesa" : mesa, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv, "claseUsuario" : claseUsuario}
            return render(request, 'administrar_mesas.html', datos)
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
        if claseUsuario.upper() == "MESERO" or claseUsuario.upper() == "ADMINISTRADOR" :
            if request.method == "POST":
                nom = request.POST["txtnommes"].upper()
                pdv = request.POST["cbopunven"]
                est = request.POST["cboest"]
                comprobarNombreMesa = Mesa.objects.select_related('pdv').filter(nombre = nom, pdv = pdv, estado_id = 1)
                if comprobarNombreMesa:
                    mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                    datos ={
                        "r2" : "¡ La Mesa ya Existe ("+str(nom).upper()+") ya Existe !",
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv,
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_mesas.html", datos)
                else:
                    mesa = Mesa(
                        nombre=nom, 
                        pdv_id = pdv,
                        usuario_id= idUsuario,
                        estado_mesa= est,
                        estado_id=1,
                    )
                    mesa.save()
                    mesa_id = mesa.id
                    descripcion = f"Mesa Registrada ({ mesa_id })"
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
                    mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                    datos = {
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Mesa Creada ({ mesa_id }) !",
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_mesas.html", datos)
            else:
                opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                datos ={
                    "r2" : "¡ Debe Presionar el Botón del Formulario !",
                    "mesa" : mesa,
                    "opciones_pdv" : opciones_pdv,
                    "claseUsuario" : claseUsuario
                }
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
        

def form_act_mes(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    rs = Mesa.objects.filter(id = id)
    if estadoSesion is True:
        if claseUsuario.upper() == "MESERO" or claseUsuario.upper() == "ADMINISTRADOR"  :
            if rs :
                mes = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                datos = { "rs":rs,"mes" : mes, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv, "claseUsuario" : claseUsuario} 
                return render(request, "actualizar_mesas.html", datos)
            else:
                mes = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                datos = { "r2" : "El id de la Mesa ("+str(id)+") No Existe. Imposibre Eliminar" , "mes" : mes, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv, "claseUsuario" : claseUsuario} 
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def actualizar_mesa(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "MESERO" or claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnommes"].upper()
                pdv = request.POST["cbopunven"]
                est = request.POST["cboest"]
                comprobarNombreMesa = Mesa.objects.select_related('pdv').filter(nombre = nom, pdv = pdv, estado_id = 1)
                if comprobarNombreMesa:
                    mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                    datos ={
                        "r2" : "¡ La Mesa ya Existe ("+str(nom).upper()+") ya Existe !",
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv,
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_mesas.html", datos)
                else:
                    mes = Mesa.objects.get(id=id)
                    mes.nombre = nom
                    mes.pdv_id = pdv
                    mes.estado_mesa = est
                    mes.estado_id =1
                    mes.save()
                    id_mes = mes.id
                    descripcion = f"Mesa modificada ({ id_mes })"
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
                    mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().filter(estado_id=1).order_by("nombre")
                    datos = {
                        "opciones_pdv": opciones_pdv,
                        "nomUsuario" : nomUsuario,
                        "mesa" : mesa,
                        "r" : f"¡ Mesa ({ id_mes }) Modificada Correctamente !",
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_mesas.html", datos)
            else:
                mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().filter(estado_id=1).order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r2" : "¡ No Se Puede Procesar La Solicitud !",
                    "claseUsuario" : claseUsuario
                }
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
        
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def eliminar_mesas(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    idUsuario = request.session.get("idUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "MESERO" or claseUsuario.upper() == "ADMINISTRADOR":
            mes = Mesa.objects.filter(id = id).first()
            if mes is not None:
                mes.estado_id=2
                mes.save()
                descripcion = f"Mesa eliminada ({ id })"
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
                mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r" : "¡ Mesa Eliminada Correctamente !",
                    "claseUsuario" : claseUsuario
                }
                return render(request, "administrar_mesas.html", datos)
            else:
                mesa = Mesa.objects.select_related('pdv').filter(estado_id=1).order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().filter(estado_id=1).order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !",
                    "claseUsuario" : claseUsuario
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
            usu = Usuario.objects.select_related('clase').all().filter(estado_id=1).order_by("nombre")
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
                nom = request.POST["txtnomusu"].upper()
                con = request.POST["txtconusu"]
                cla = request.POST["cboclausu"]
                comprobarNombreUsu = Usuario.objects.filter(nombre = nom,estado_id =1)
                if comprobarNombreUsu:
                    usu = Usuario.objects.select_related('clase').filter(estado_id=1).order_by("nombre")
                    opciones_clases = Clases.objects.all().values().filter().order_by("nombre")
                    datos ={
                        "r2" : "¡ El usuario ("+str(nom).upper()+") ya Existe !",
                        "usu" : usu,
                        "opciones_clases" : opciones_clases,
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_usuarios.html", datos)            
                else:
                    usu = Usuario(
                            nombre=nom,
                            password=con,
                            clase_id=cla,
                            estado_id =1
                        )
                    usu.save()
                    usu_id = usu.id
                    descripcion = f"Usuario ({ usu_id }) creado correctamente"
                    tabla = "safari.usuario"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = usuario
                    )
                    his.save()
                    usu = Usuario.objects.select_related('clase').filter(estado_id=1).order_by("nombre")
                    opciones_clases = Clases.objects.all().values().order_by("nombre")
                    datos = {
                        "usu" : usu,
                        "opciones_clases": opciones_clases,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Usuario Creado ({ usu_id }) !",
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_usuarios.html", datos)
            else:
                usu = Usuario.objects.select_related('clase').filter(estado_id=1).order_by("nombre")
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "opciones_clases" : opciones_clases, "usu" : usu }
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
                usu = Usuario.objects.select_related('clase').filter(estado_id = 1).order_by("nombre")
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = { "rs":rs,"usu" : usu, "nomUsuario" : nomUsuario, "opciones_clases" : opciones_clases} 
                return render(request, "actualizar_usuarios.html", datos)
            else:
                usu = Usuario.objects.select_related('clase').filter(estado_id = 1).order_by("nombre")
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = { "r2" : "El id del Usuario ("+str(id)+") No Existe. Imposibre Actualizar" , "usu" : usu, "nomUsuario" : nomUsuario, "opciones_clases" : opciones_clases} 
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
                nom = request.POST["txtnomusu"].upper()
                con = request.POST["txtconusu"]
                cla = request.POST["cboclausu"]
                comprobarNombreUsu = Usuario.objects.filter(nombre = nom, estado_id =1)
                if comprobarNombreUsu:
                    usu = Usuario.objects.select_related('clase').filter(estado_id=1).order_by("nombre")
                    opciones_clases = Clases.objects.all().values().filter().order_by("nombre")
                    datos ={
                        "r2" : "¡ El usuario ("+str(nom).upper()+") ya Existe !",
                        "usu" : usu,
                        "opciones_clases" : opciones_clases,
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_usuarios.html", datos)       
                else: 
                    usu = Usuario.objects.get(id=id)
                    usu.nombre = nom
                    usu.password = con
                    usu.clase_id = cla
                    usu.estado_id = 1
                    usu.save()
                    id_usu = usu.id
                    descripcion = f"Usuario modificado ({ id })"
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
                    usu = Usuario.objects.select_related('clase').filter(estado_id = 1).order_by("-id")
                    datos = {
                        "opciones_clases": opciones_clases,
                        "nomUsuario" : nomUsuario,
                        "usu" : usu,
                        "r" : f"¡ Usuario ({ id_usu }) Modificado Correctamente !"
                    }

                    return render(request, "administrar_usuarios.html", datos)
            else:
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                usu = Usuario.objects.select_related('clase').filter(usuario__nombre=nomUsuario, estado_id = 1).order_by("-id")
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
    
def eliminar_usuario(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    idUsuario = request.session.get("idUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            usu = Usuario.objects.filter(id = id).first()
            if usu is not None:
                usu.estado_id =2
                usu.save()
                descripcion = f"Usuario eliminado ({ id })"
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
                usu = Usuario.objects.select_related('clase').filter(estado_id = 1).order_by("-id")
                datos = {
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "usu" : usu,
                    "r" : "¡ Usuario Eliminado Correctamente !"
                }
                return render(request, "administrar_usuarios.html", datos)
            else:
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                usu = Usuario.objects.select_related('clase').filter(estado_id = 1).order_by("-id")
                datos = {
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "usu" : usu,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !"
                }
                return render(request, "administrar_usuarios.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
    
    
def administrar_pdv(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            pdv = PuntodeVenta.objects.select_related('usuario').all().filter(estado_id = 1).order_by("nombre")
            datos = {"pdv" : pdv,
                    "nomUsuario": nomUsuario}
            return render(request, 'administrar_pdv.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def registrar_pdv(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnompdv"].upper()
                comprobarNombrePdv = PuntodeVenta.objects.filter(nombre = nom, estado_id=1)
                if comprobarNombrePdv:
                    pdv = PuntodeVenta.objects.select_related('usuario').filter(estado_id=1).order_by("nombre")
                    datos ={
                        "r2" : "¡ El Punto de Venta ("+str(nom).upper()+") ya Existe !",
                        "pdv" : pdv,
                        "claseUsuario" : claseUsuario,
                        "nomUsuario" : nomUsuario
                    }
                    return render(request, "administrar_pdv.html", datos)           
                else:
                    pdv = PuntodeVenta(
                        nombre=nom,
                        usuario_id = idUsuario,
                        estado_id = 1
                    )
                    pdv.save()
                    pdv_id = pdv.id
                    descripcion = f"Punto de Venta creado ({ pdv_id })"
                    tabla = "safari.puntodeventa"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = usuario
                    )
                    his.save()
                    pdv = PuntodeVenta.objects.select_related('usuario').all().filter(estado_id=1).order_by("nombre")
                    datos = {
                        "pdv" : pdv,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Punto de venta Creado ({ pdv_id }) !"
                    }
                    return render(request, "administrar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').all().order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "pdv" : pdv, "nomUsuario" : nomUsuario }
                return render(request, "administrar_pdv.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def form_act_pdv(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    rs = PuntodeVenta.objects.filter(id = id)
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if rs :
                pdv = PuntodeVenta.objects.select_related('usuario').filter(estado_id = 1).order_by("nombre")
                datos = { "rs":rs,"pdv" : pdv, "nomUsuario" : nomUsuario} 
                return render(request, "actualizar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').filter(estado_id = 1).order_by("nombre")
                datos = { "r2" : "El id del Usuario ("+str(id)+") No Existe. Imposibre Eliminar" , "pdv" : pdv, "nomUsuario" : nomUsuario} 
                return render(request, "administrar_pdv.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
    
    

def actualizar_pdv(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnompdv"].upper()
                comprobarNombrePdv = PuntodeVenta.objects.filter(nombre = nom, estado_id=1)
                if comprobarNombrePdv:
                    pdv = PuntodeVenta.objects.select_related('usuario').filter(estado_id=1).order_by("nombre")
                    datos ={
                        "r2" : "¡ El Punto de Venta ("+str(nom).upper()+") ya Existe !",
                        "pdv" : pdv,
                        "claseUsuario" : claseUsuario,
                        "nomUsuario" : nomUsuario
                    }
                    return render(request, "administrar_pdv.html", datos)          
                else:
                    pdv = PuntodeVenta.objects.get(id=id)
                    pdv.nombre = nom
                    pdv.usuario_id = idUsuario
                    pdv.estado_id = 1
                    pdv.save()
                    pdv_id = pdv.id
                    descripcion = f"Punto de Venta actualizado ({ pdv_id })"
                    tabla = "safari.puntodeventa"
                    fechayhora = datetime.now()
                    usuario = request.session["idUsuario"]
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = usuario
                    )
                    his.save()
                    pdv = PuntodeVenta.objects.select_related('usuario').all().filter(estado_id = 1).order_by("nombre")
                    datos = {
                        "pdv" : pdv,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Punto de venta actualizado ({ pdv_id }) !"
                    }
                    return render(request, "administrar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').all().filter(estado_id = 1).order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "pdv" : pdv }
                return render(request, "administrar_pdv.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def eliminar_pdv(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    idUsuario = request.session.get("idUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            pdv = PuntodeVenta.objects.filter(id = id).first()
            if pdv is not None:
                pdv.estado_id = 2
                pdv.save()
                descripcion = f"Punto de Venta eliminado ({ id })"
                tabla = "safari_puntodeventa"
                fechayhora = datetime.now()
                usuario = request.session["idUsuario"]
                his = Historial(
                    descripcion_historial = descripcion,
                    tabla_afectada_historial = tabla,
                    fecha_hora_historial = fechayhora,
                    usuario_id = usuario
                )
                his.save()
                pdv = PuntodeVenta.objects.select_related('usuario').filter(estado_id = 1).order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pdv" : pdv,
                    "r" : "¡ Punto de venta Eliminado Correctamente !"
                }
                return render(request, "administrar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').filter(estado_id = 1).order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pdv" : pdv,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !"
                }
                return render(request, "administrar_pdv.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)
    

def ver_ventas(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            puntos = PuntodeVenta.objects.all().filter(estado_id = 1).order_by("nombre")
            ventas = Venta.objects.select_related('puntoventa').all().order_by("-fecha")

            punto = request.GET.get("cbo_punto")
            fecha_venta = request.GET.get("fecha_venta")
            estado_venta = request.GET.get("estado_venta")

            if punto:
                ventas = ventas.filter(puntoventa_id=punto)
            if fecha_venta:
                ventas = ventas.filter(fecha__date=fecha_venta)
            if estado_venta:
                ventas = ventas.filter(estado=estado_venta)

            datos = {
                "nomUsuario": nomUsuario,
                "puntos": puntos,
                "ventas": ventas
            }
            return render(request, 'ver_ventas.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def ver_estadisticas(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            hoy = datetime.now().date()
            ventas_hoy = Venta.objects.filter(fecha__date=hoy, estado_v="PAGADA")
            total_ventas_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or 0

            cantidad_ordenes = ventas_hoy.count()

            productos_top = (
                DetalleVenta.objects.filter(venta__estado_v="PAGADA").values(id_producto=F('producto__id'), nombre=F('producto__nombre'))
                .annotate(cantidad=Sum('cantidad'), recaudado=Sum('subtotal')).order_by('-cantidad')[:10]
            )

            mesas_ocupadas = Mesa.objects.filter(estado_mesa="OCUPADA").count()
            mesas_libres = Mesa.objects.filter(estado_mesa="LIBRE").count()

            datos = {
                "nomUsuario": nomUsuario,
                "total_ventas_hoy": total_ventas_hoy,
                "cantidad_ordenes": cantidad_ordenes,
                "productos_top": productos_top,
                "mesas_ocupadas": mesas_ocupadas,
                "mesas_libres": mesas_libres,
            }
            return render(request, 'ver_estadisticas.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)


def administrar_productos(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR" or claseUsuario.upper() == "CAJERO":
            pro = Producto.objects.select_related('usuario').filter(estado_id = 1).all().order_by("nombre")
            datos = {"pro" : pro, "nomUsuario": nomUsuario, "claseUsuario" : claseUsuario}
            return render(request, 'administrar_productos.html', datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def registrar_producto(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR" or claseUsuario.upper() == "CAJERO":
            if request.method == "POST":
                nom = request.POST["txtnompro"].upper()
                des = request.POST["txtdespro"]
                pre = request.POST["numprepro"]
                comprobarNombreProducto = Producto.objects.filter(nombre = nom, estado_id=1)
                if comprobarNombreProducto:
                    pro = Producto.objects.select_related('usuario').filter(estado_id=1).order_by("nombre")
                    datos ={
                        "r2" : "¡ El Producto ("+str(nom).upper()+") ya Existe !",
                        "pro" : pro,
                        "claseUsuario" : claseUsuario,
                        "nomUsuario" : nomUsuario
                    }
                    return render(request, "administrar_productos.html", datos)   
                else:
                    pro = Producto(
                        nombre=nom,
                        descripcion=des,
                        precio=pre,
                        estado_id = 1,
                        usuario_id=idUsuario,
                    )
                    pro.save()
                    pro_id = pro.id
                    
                    descripcion = f"Producto registrado ({ pro_id })"
                    tabla = "safari_producto"
                    fechayhora = datetime.now()
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = request.session["idUsuario"]
                    )
                    his.save()
                    
                    pro_lista = Producto.objects.select_related('usuario').filter(estado_id = 1).all().order_by("nombre")
                    datos = {
                        "pro" : pro_lista,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Producto Creado Exitosamente ({ pro_id }) !",
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_productos.html", datos)
            else:
                pro_lista = Producto.objects.select_related('usuario').all().filter(estado_id = 1).order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "pro" : pro_lista, "nomUsuario": nomUsuario, "claseUsuario" : claseUsuario }
                return render(request, "administrar_productos.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def form_act_producto(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    rs = Producto.objects.filter(id = id)
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR" or claseUsuario.upper() == "CAJERO":
            if rs:
                pro = Producto.objects.select_related('usuario').filter(estado_id = 1).order_by("nombre")
                datos = { "rs": rs, "nomUsuario" : nomUsuario, "pro" : pro, "claseUsuario" : claseUsuario} 
                return render(request, "actualizar_productos.html", datos)
            else:
                pro = Producto.objects.select_related('usuario').filter(estado_id = 1).order_by("nombre")
                datos = { "r2" : f"El id del Producto ({id}) No Existe.", "pro" : pro, "nomUsuario" : nomUsuario, "claseUsuario" : claseUsuario} 
                return render(request, "administrar_productos.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def actualizar_producto(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR" or claseUsuario.upper() == "CAJERO" :
            if request.method == "POST":
                nom = request.POST["txtnompro"].upper()
                des = request.POST["txtdespro"]
                pre = request.POST["numprepro"]
                comprobarNombreProducto = Producto.objects.filter(nombre = nom, estado_id=1)
                if comprobarNombreProducto:
                    pro = Producto.objects.select_related('usuario').filter(estado_id=1).order_by("nombre")
                    datos ={
                        "r2" : "¡ El Producto ("+str(nom).upper()+") ya Existe !",
                        "pro" : pro,
                        "claseUsuario" : claseUsuario,
                        "nomUsuario" : nomUsuario
                    }
                    return render(request, "administrar_productos.html", datos)   
                else:
                    pro = Producto.objects.get(id=id)
                    pro.nombre = nom
                    pro.descripcion = des
                    pro.precio = pre
                    pro.estado_id = 1
                    # Mantenemos registro de quién hizo la última actualización
                    pro.usuario_id = idUsuario 
                    
                    pro.save()

                    descripcion = f"Producto modificado ({ id })"
                    tabla = "safari_producto"
                    fechayhora = datetime.now()
                    his = Historial(
                        descripcion_historial = descripcion,
                        tabla_afectada_historial = tabla,
                        fecha_hora_historial = fechayhora,
                        usuario_id = request.session["idUsuario"]
                    )
                    his.save()

                    pro = Producto.objects.select_related('usuario').all().filter(estado_id = 1).order_by("nombre")
                    datos = {
                        "nomUsuario" : nomUsuario,
                        "pro" : pro,
                        "r" : f"¡ Producto ({ id }) Modificado Correctamente !",
                        "claseUsuario" : claseUsuario
                    }
                    return render(request, "administrar_productos.html", datos)
            else:
                pro_lista = Producto.objects.select_related('usuario').all().filter(estado_id = 1).order_by("nombre")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro_lista" : pro_lista,
                    "r2" : "¡ No Se Puede Procesar La Solicitud !",
                    "claseUsuario" : claseUsuario
                }
                return render(request, "administrar_productos.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def eliminar_producto(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR" or claseUsuario.upper() == "CAJERO":
            pro = Producto.objects.filter(id = id, estado_id = 1).first()
            if pro is not None:
                pro.estado_id = 2
                pro.save()
                descripcion = f"Producto eliminado ({ id })"
                tabla = "safari_producto"
                fechayhora = datetime.now()
                his = Historial(
                    descripcion_historial = descripcion,
                    tabla_afectada_historial = tabla,
                    fecha_hora_historial = fechayhora,
                    usuario_id = request.session["idUsuario"]
                )
                his.save()
                pro_lista = Producto.objects.select_related('usuario').all().filter(estado_id = 1).order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro" : pro_lista,
                    "r" : "¡ Producto Eliminado Correctamente !",
                    "claseUsuario" : claseUsuario
                }
                return render(request, "administrar_productos.html", datos)
            else:
                pro_lista = Producto.objects.select_related('usuario').all().filter(estado_id = 1).order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro" : pro_lista,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !",
                    "claseUsuario" : claseUsuario
                }
                return render(request, "administrar_productos.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def jornada(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() in ["CAJERO", "ADMINISTRADOR"]:
            caja_abierta = JornadaCaja.objects.select_related('puntoventa').filter(usuario_id=idUsuario, estado_J="ABIERTA").first()
            puntos = PuntodeVenta.objects.all().filter(estado_id=1).order_by("nombre")
            historial_cajas = JornadaCaja.objects.select_related('puntoventa', 'usuario').filter(usuario_id=idUsuario).order_by("-id")[:10]
            if request.method == "POST":
                accion = request.POST.get("accion")

                # 1. ABRIR CAJA CON MONTO INICIAL (SENCILLO)
                if accion == "abrir" and not caja_abierta:
                    pdv_id = request.POST["cbopdv"]
                    monto_ini = int(request.POST["txtmontoini"])
                    nueva_caja = JornadaCaja(
                        usuario_id=idUsuario,
                        puntoventa_id=pdv_id,
                        monto_inicial=monto_ini,
                        estado_J="ABIERTA"
                    )
                    nueva_caja.save()

                    Historial.objects.create(
                        descripcion_historial=f"Apertura de caja #{nueva_caja.id} con ${monto_ini}",
                        tabla_afectada_historial="safari_jornadacaja",
                        fecha_hora_historial=datetime.now(),
                        usuario_id=idUsuario
                    )
                    caja_abierta = nueva_caja
                    mensaje = f"¡ Caja #{nueva_caja.id} Abierta Correctamente con ${monto_ini} !"
                    return render(request, 'jornada.html', {"nomUsuario": nomUsuario, "caja_abierta": caja_abierta, "puntos": puntos, "historial_cajas": historial_cajas, "r": mensaje})

                # 2. CERRAR CAJA Y REALIZAR CUADRATURA DE BILLETES Y MONEDAS
                elif accion == "cerrar" and caja_abierta:
                    b20000 = int(request.POST.get("b20000", 0)) * 20000
                    b10000 = int(request.POST.get("b10000", 0)) * 10000
                    b5000  = int(request.POST.get("b5000", 0))  * 5000
                    b1000  = int(request.POST.get("b1000", 0))  * 1000
                    m500   = int(request.POST.get("m500", 0))   * 500
                    m100   = int(request.POST.get("m100", 0))   * 100
                    m50    = int(request.POST.get("m50", 0))    * 50
                    m10    = int(request.POST.get("m10", 0))    * 10
                    m5     = int(request.POST.get("m5", 0))     * 5
                    m1     = int(request.POST.get("m1", 0))     * 1

                    monto_fisico_contado = b20000 + b10000 + b5000 + b1000 + m500 + m100 + m50 + m10 + m5 + m1

                    # Calcular ventas pagadas durante esta sesión de caja en ese punto de venta
                    ventas_sesion = Venta.objects.filter(
                        puntoventa_id=caja_abierta.puntoventa_id,
                        fecha__gte=caja_abierta.fecha_apertura,
                        estado_v="PAGADA"
                    ).aggregate(total=Sum('total'))['total'] or 0

                    esperado = caja_abierta.monto_inicial + ventas_sesion
                    diferencia = monto_fisico_contado - esperado

                    caja_abierta.fecha_cierre = datetime.now()
                    caja_abierta.total_ventas = ventas_sesion
                    caja_abierta.monto_contado = monto_fisico_contado
                    caja_abierta.diferencia = diferencia
                    caja_abierta.estado = "CERRADA"
                    caja_abierta.save()

                    Historial.objects.create(
                        descripcion_historial=f"Cierre y cuadratura de caja #{caja_abierta.id} (Diferencia: ${diferencia})",
                        tabla_afectada_historial="safari_jornadacaja",
                        fecha_hora_historial=datetime.now(),
                        usuario_id=idUsuario
                    )
                    return render(request, 'jornada.html', {
                        "nomUsuario": nomUsuario,
                        "caja_abierta": None,
                        "puntos": puntos,
                        "historial_cajas": JornadaCaja.objects.select_related('puntoventa').filter(usuario_id=idUsuario).order_by("-id")[:10],
                        "r": f"¡ Caja Cerrada ! Contado: ${monto_fisico_contado} | Esperado: ${esperado} | Diferencia: ${diferencia}"
                    })

            datos = {
                "nomUsuario": nomUsuario,
                "caja_abierta": caja_abierta,
                "puntos": puntos,
                "historial_cajas": historial_cajas
            }
            return render(request, 'jornada.html', datos)
        else:
            return render(request, 'index.html', {"r2": "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !"})
    else:
        return render(request, "index.html", {"r2": "¡ Debe Iniciar Sesión Para Acceder !"})

def ver_ventas_caja(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() in ["CAJERO", "ADMINISTRADOR"]:
            ventas = Venta.objects.select_related('puntoventa', 'mesa', 'usuario').all().order_by("-fecha")
            return render(request, 'ver_ventas_caja.html', {"nomUsuario": nomUsuario, "ventas": ventas})
        else:
            return render(request, 'index.html', {"r2": "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !"})
    else:
        return render(request, "index.html", {"r2": "¡ Debe Iniciar Sesión Para Acceder !"})

def registrar_ventas(request):
    return render(request, 'registrar_ventas.html')

def registrar_pedido(request):
    return render(request, 'registrar_pedido.html')

def exportar_excel(request):
    estadoSesion = request.session.get("estadoSesion")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True and claseUsuario.upper() == "ADMINISTRADOR":
        from django.http.response import HttpResponse
        from openpyxl import Workbook
        from openpyxl.styles import Border, Side, Font
        import random

        wb = Workbook()
        hoja = wb.active
        hoja.title = "Listado de Ventas"
        hoja.append(("FOLIO", "FECHA", "PUNTO DE VENTA", "TIPO", "ESTADO", "TOTAL"))

        ventas = Venta.objects.select_related('puntoventa').all().order_by("-id")
        cant = 0
        suma = 0
        prom = 0

        for v in ventas:
            fecha_str = v.fecha.strftime("%d/%m/%Y %H:%M") if v.fecha else ""
            hoja.append((v.id, fecha_str, v.puntoventa.nombre, v.tipo_venta, v.estado, v.total))
            if v.estado == "PAGADA":
                cant += 1
                suma += v.total
                prom = suma / cant

        hoja2 = wb.create_sheet("Estadística")
        hoja2.append(("Cantidad Pagadas", "Suma Recaudada", "Promedio por Venta"))
        hoja2.append((cant, suma, prom))

        bordes = Border(
            left=Side(border_style="thin", color="FF000000"),
            top=Side(border_style="thin", color="FF000000"),
            right=Side(border_style="thin", color="FF000000"),
            bottom=Side(border_style="thin", color="FF000000")
        )
        encabezados = Font(name="Calibri", size=12, bold=True)

        for col in ["A1", "B1", "C1", "D1", "E1", "F1"]:
            hoja[col].border = bordes
            hoja[col].font = encabezados

        for col in ["A1", "B1", "C1"]:
            hoja2[col].border = bordes
            hoja2[col].font = encabezados

        hoja.column_dimensions["A"].width = 10
        hoja.column_dimensions["B"].width = 20
        hoja.column_dimensions["C"].width = 22
        hoja.column_dimensions["D"].width = 15
        hoja.column_dimensions["E"].width = 15
        hoja.column_dimensions["F"].width = 15

        aleatorio = random.randint(1000, 999999)
        nombreArchivo = f"reporte_safari_{aleatorio}.xlsx"
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = f"attachment; filename={nombreArchivo}"
        wb.save(response)
        return response
    else:
        return render(request, "index.html", {"r2": "¡ No Tiene Permisos Para Exportar Reportes !"})


def mostrar_listado_historial(request, orden):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")

    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            match orden:
                case 1:
                    his = Historial.objects.select_related('usuario').all().order_by("id")
                case 2:
                    his = Historial.objects.select_related('usuario').all().order_by("-id")
                case 3:
                    his = Historial.objects.select_related('usuario').all().order_by("descripcion_historial")
                case 4:
                    his = Historial.objects.select_related('usuario').all().order_by("-descripcion_historial")
                case 5:
                    his = Historial.objects.select_related('usuario').all().order_by("tabla_afectada_historial")
                case 6:
                    his = Historial.objects.select_related('usuario').all().order_by("-tabla_afectada_historial")
                case 7:
                    his = Historial.objects.select_related('usuario').all().order_by("fecha_hora_historial")
                case 8:
                    his = Historial.objects.select_related('usuario').all().order_by("-fecha_hora_historial")
                case 9:
                    his = Historial.objects.select_related('usuario').all().order_by("usuario__nombre")
                case 10:
                    his = Historial.objects.select_related('usuario').all().order_by("-usuario__nombre")
                case _:
                    his = Historial.objects.select_related('usuario').all().order_by("-id")
            datos = {
                "nomUsuario": nomUsuario,
                "his": his
            }
            return render(request, "listado_historial.html", datos)
        else:
            datos = { 'r2': "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, "index.html", datos)
    else:
        datos = { 'r2': "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)


def mostrar_error_404(request, exception):
    return render(request, 'error404.html', status=404)

def mostrar_error_500(request):
    return render(request, 'error500.html', status=500)