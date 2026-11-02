from django.shortcuts import render
from datetime import datetime
from .models import Usuario, Historial, Mesa, Clases, PuntodeVenta, Producto, Ticket, Venta, DetalleVenta
from django.db.models import Sum, Count, F

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
            mesa = Mesa.objects.select_related('pdv').order_by("nombre")
            opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
            datos = {"mesa" : mesa, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv}
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
            mesa = Mesa.objects.select_related('pdv').order_by("nombre")
            opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
            datos = {"mesa" : mesa, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv}
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
                pdv = request.POST["cbopunven"]
                est = request.POST["cboest"]
                comprobarNombreMesa = Mesa.objects.filter(nombre = nom)
                if comprobarNombreMesa:
                    mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                    datos ={
                        "r2" : "¡ La Mesa ya Existe ("+str(nom).upper()+") ya Existe !",
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv
                    }
                    return render(request, "administrar_admin_mesas.html", datos)
                else:
                    mesa = Mesa(
                        nombre=nom, 
                        pdv_id = pdv,
                        usuario_id= idUsuario,
                        estado= est
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
                    mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                    datos = {
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Mesa Creada ({ mesa_id }) !"
                    }
                    return render(request, "administrar_admin_mesas.html", datos)
            else:
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                datos ={
                    "r2" : "¡ Debe Presionar el Botón del Formulario !",
                    "mesa" : mesa,
                    "opciones_pdv" : opciones_pdv
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
                pdv = request.POST["cbopunven"]
                est = request.POST["cboest"]
                comprobarNombreMesa = Mesa.objects.filter(nombre = nom)
                if comprobarNombreMesa:
                    mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                    datos ={
                        "r2" : "¡ La Mesa ya Existe ("+str(nom).upper()+") ya Existe !",
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv
                    }
                    return render(request, "administrar_mesas.html", datos)
                else:
                    mesa = Mesa(
                        nombre=nom, 
                        pdv_id = pdv,
                        usuario_id= idUsuario,
                        estado= est
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
                    mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                    opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                    datos = {
                        "mesa" : mesa,
                        "opciones_pdv" : opciones_pdv,
                        "nomUsuario" : nomUsuario,
                        "r" : f"¡ Mesa Creada ({ mesa_id }) !"
                    }
                    return render(request, "administrar_mesas.html", datos)
            else:
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                datos ={
                    "r2" : "¡ Debe Presionar el Botón del Formulario !",
                    "mesa" : mesa,
                    "opciones_pdv" : opciones_pdv
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
        if claseUsuario.upper() == "MESERO":
            if rs :
                mes = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = { "rs":rs,"mes" : mes, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv} 
                return render(request, "actualizar_mesas.html", datos)
            else:
                mes = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = { "r2" : "El id de la Mesa ("+str(id)+") No Existe. Imposibre Eliminar" , "mes" : mes, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv} 
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
        
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def form_act_mes_adm(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")

    rs = Mesa.objects.filter(id = id)
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if rs :
                mes = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = { "rs":rs,"mes" : mes, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv} 
                return render(request, "actualizar_mesas_admin.html", datos)
            else:
                mes = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = { "r2" : "El id de la Mesa ("+str(id)+") No Existe. Imposibre Eliminar" , "mes" : mes, "nomUsuario" : nomUsuario, "opciones_pdv" : opciones_pdv} 
                return render(request, "administrar_admin_mesas.html", datos)
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
        if claseUsuario.upper() == "MESERO":
            if request.method == "POST":
                nom = request.POST["txtnommes"]
                pdv = request.POST["cbopunven"]
                est = request.POST["cboest"]
                mes = Mesa.objects.get(id=id)
                mes.nombre = nom
                mes.pdv.id = pdv
                mes.estado = est
                mes.save()
                id_mes = mes.id
                descripcion = f"Registro modificado ({ id_mes })"
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
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r" : f"¡ Mesa ({ id_mes }) Modificado Correctamente !"
                }
                return render(request, "administrar_mesas.html", datos)
            else:
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r2" : "¡ No Se Puede Procesar La Solicitud !"
                }
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
        
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def actualizar_mesa_admin(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    idUsuario = request.session.get("idUsuario")
    claseUsuario = request.session.get("claseUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnommes"]
                pdv = request.POST["cbopunven"]
                est = request.POST["cboest"]
                mes = Mesa.objects.get(id=id)
                mes.nombre = nom
                mes.pdv.id = pdv
                mes.estado = est
                mes.save()
                id_mes = mes.id
                descripcion = f"Registro modificado ({ id_mes })"
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
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r" : f"¡ Mesa ({ id_mes }) Modificado Correctamente !"
                }
                return render(request, "administrar_admin_mesas.html", datos)
            else:
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r2" : "¡ No Se Puede Procesar La Solicitud !"
                }
                return render(request, "administrar_admin_mesas.html", datos)
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
        if claseUsuario.upper() == "MESERO":
            mes = Mesa.objects.filter(id = id)
            if mes.exists():
                mes.delete()
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
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r" : "¡ Mesa Eliminada Correctamente !"
                }
                return render(request, "administrar_mesas.html", datos)
            else:
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !"
                }
                return render(request, "administrar_mesas.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def eliminar_mesas_admin(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    idUsuario = request.session.get("idUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            mes = Mesa.objects.filter(id = id)
            if mes.exists():
                mes.delete()
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
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r" : "¡ Mesa Eliminada Correctamente !"
                }
                return render(request, "administrar_admin_mesas.html", datos)
            else:
                mesa = Mesa.objects.select_related('pdv').order_by("nombre")
                opciones_pdv = PuntodeVenta.objects.all().values().order_by("nombre")
                datos = {
                    "opciones_pdv": opciones_pdv,
                    "nomUsuario" : nomUsuario,
                    "mesa" : mesa,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !"
                }
                return render(request, "administrar_admin_mesas.html", datos)
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
                    clase_id=cla
                )
                usu.save()
                usu_id = usu.id
                descripcion = f"Registro insertado ({ usu_id })"
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
                usu = Usuario.objects.all().values().order_by("nombre")
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                datos = {
                    "usu" : usu,
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "r" : f"¡ Usuario Creado ({ usu_id }) !"
                }
                return render(request, "administrar_usuarios.html", datos)
            else:
                usu = Usuario.objects.all().values().order_by("nombre")
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


                descripcion = f"Registro modificado ({ id })"
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
    
def eliminar_usuario(request, id):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")
    claseUsuario = request.session.get("claseUsuario")
    idUsuario = request.session.get("idUsuario")
    if estadoSesion is True:
        if claseUsuario.upper() == "ADMINISTRADOR":
            usu = Usuario.objects.filter(id = id)
            if usu.exists():
                usu.delete()
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
                usu = Usuario.objects.select_related('clase').filter().order_by("-id")
                datos = {
                    "opciones_clases": opciones_clases,
                    "nomUsuario" : nomUsuario,
                    "usu" : usu,
                    "r" : "¡ Usuario Eliminado Correctamente !"
                }
                return render(request, "administrar_usuarios.html", datos)
            else:
                opciones_clases = Clases.objects.all().values().order_by("nombre")
                usu = Usuario.objects.select_related('clase').filter().order_by("-id")
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
            pdv = PuntodeVenta.objects.select_related('usuario').all().order_by("nombre")
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
                nom = request.POST["txtnompdv"]
                pdv = PuntodeVenta(
                    nombre=nom,
                    usuario_id = idUsuario
                )
                pdv.save()
                pdv_id = pdv.id
                descripcion = f"Punto de Venta insertado ({ pdv_id })"
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
                pdv = PuntodeVenta.objects.select_related('usuario').all().order_by("nombre")
                datos = {
                    "pdv" : pdv,
                    "nomUsuario" : nomUsuario,
                    "r" : f"¡ Punto de venta Creado ({ pdv_id }) !"
                }
                return render(request, "administrar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').all().order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "pdv" : pdv }
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
                pdv = PuntodeVenta.objects.select_related('usuario').order_by("nombre")
                datos = { "rs":rs,"pdv" : pdv, "nomUsuario" : nomUsuario} 
                return render(request, "actualizar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').order_by("nombre")
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
                nom = request.POST["txtnompdv"]
                pdv = PuntodeVenta.objects.get(id=id)
                pdv.nombre = nom
                pdv.usuario_id = idUsuario
                pdv.save()
                pdv_id = pdv.id
                descripcion = f"Punto de Venta insertado ({ pdv_id })"
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
                pdv = PuntodeVenta.objects.select_related('usuario').all().order_by("nombre")
                datos = {
                    "pdv" : pdv,
                    "nomUsuario" : nomUsuario,
                    "r" : f"¡ Punto de venta actualizado ({ pdv_id }) !"
                }
                return render(request, "administrar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').all().order_by("nombre")
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
            pdv = PuntodeVenta.objects.filter(id = id)
            if pdv.exists():
                pdv.delete()
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
                pdv = PuntodeVenta.objects.select_related('usuario').filter().order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pdv" : pdv,
                    "r" : "¡ Usuario Eliminado Correctamente !"
                }
                return render(request, "administrar_pdv.html", datos)
            else:
                pdv = PuntodeVenta.objects.select_related('usuario').filter().order_by("-id")
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
            puntos = PuntodeVenta.objects.all().order_by("nombre")
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
            ventas_hoy = Venta.objects.filter(fecha__date=hoy, estado="PAGADA")
            total_ventas_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or 0

            cantidad_ordenes = ventas_hoy.count()

            productos_top = (
                DetalleVenta.objects.filter(venta__estado="PAGADA").values(id_producto=F('producto__id'), nombre=F('producto__nombre'))
                .annotate(cantidad=Sum('cantidad'), recaudado=Sum('subtotal')).order_by('-cantidad')[:10]
            )

            mesas_ocupadas = Mesa.objects.filter(estado="OCUPADA").count()
            mesas_libres = Mesa.objects.filter(estado="LIBRE").count()

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
        if claseUsuario.upper() == "ADMINISTRADOR":
            pro = Producto.objects.select_related('usuario').all().order_by("nombre")
            datos = {"pro" : pro, "nomUsuario": nomUsuario}
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
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnompro"]
                des = request.POST["txtdespro"]
                pre = request.POST["numprepro"]
                
                pro = Producto(
                    nombre=nom,
                    descripcion=des,
                    precio=pre,
                    usuario_id=idUsuario
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
                
                pro_lista = Producto.objects.select_related('usuario').all().order_by("nombre")
                datos = {
                    "pro" : pro_lista,
                    "nomUsuario" : nomUsuario,
                    "r" : f"¡ Producto Creado Exitosamente ({ pro_id }) !"
                }
                return render(request, "administrar_productos.html", datos)
            else:
                pro_lista = Producto.objects.select_related('usuario').all().order_by("nombre")
                datos = { "r2" : "¡ No Se Puede Procesar La Solicitud !", "pro" : pro_lista, "nomUsuario": nomUsuario }
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
        if claseUsuario.upper() == "ADMINISTRADOR":
            if rs.exists():
                datos = { "rs": rs, "nomUsuario" : nomUsuario} 
                return render(request, "actualizar_productos.html", datos)
            else:
                pro = Producto.objects.select_related('usuario').order_by("nombre")
                datos = { "r2" : f"El id del Producto ({id}) No Existe.", "pro" : pro, "nomUsuario" : nomUsuario} 
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
        if claseUsuario.upper() == "ADMINISTRADOR":
            if request.method == "POST":
                nom = request.POST["txtnompro"]
                des = request.POST["txtdespro"]
                pre = request.POST["numprepro"]
                
                pro = Producto.objects.get(id=id)
                pro.nombre = nom
                pro.descripcion = des
                pro.precio = pre
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

                pro_lista = Producto.objects.select_related('usuario').all().order_by("nombre")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro" : pro_lista,
                    "r" : f"¡ Producto ({ id }) Modificado Correctamente !"
                }
                return render(request, "administrar_productos.html", datos)
            else:
                pro_lista = Producto.objects.select_related('usuario').all().order_by("nombre")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro" : pro_lista,
                    "r2" : "¡ No Se Puede Procesar La Solicitud !"
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
        if claseUsuario.upper() == "ADMINISTRADOR":
            pro = Producto.objects.filter(id = id)
            if pro.exists():
                pro.delete()
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
                
                pro_lista = Producto.objects.select_related('usuario').all().order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro" : pro_lista,
                    "r" : "¡ Producto Eliminado Correctamente !"
                }
                return render(request, "administrar_productos.html", datos)
            else:
                pro_lista = Producto.objects.select_related('usuario').all().order_by("-id")
                datos = {
                    "nomUsuario" : nomUsuario,
                    "pro" : pro_lista,
                    "r2" : f"¡ El ID ({str(id)}) No Existe. Imposible Eliminar !"
                }
                return render(request, "administrar_productos.html", datos)
        else:
            datos = { "r2" : "¡ No Tiene Permisos Para Acceder. Privilegios Insuficientes !" }
            return render(request, 'index.html', datos)
    else:
        datos = { "r2" : "¡ Debe Iniciar Sesión Para Acceder !" }
        return render(request, "index.html", datos)

def jornada(request):
    return render(request, 'jornada.html')

def ver_ventas_caja(request):
    return render(request, 'ver_ventas_caja.html')

def registrar_ventas(request):
    return render(request, 'registrar_ventas.html')

def registrar_pedido(request):
    return render(request, 'registrar_pedido.html')