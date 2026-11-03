from django.db import models

class Clases(models.Model):
    nombre = models.TextField(max_length=12)
    def __str__(self):
        return self.nombre
    

class Usuario(models.Model):
    nombre = models.TextField(max_length=12)
    password = models.TextField(max_length=20)
    clase = models.ForeignKey(Clases, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion_historial = models.TextField(max_length=200)
    tabla_afectada_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField()

class PuntodeVenta(models.Model):
    nombre = models.TextField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    nombre = models.TextField(max_length=30)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pdv = models.ForeignKey(PuntodeVenta, on_delete=models.CASCADE)
    estado = models.TextField(max_length=15)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.TextField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=255)
    precio = models.IntegerField(default=0)
    def __str__(self):
        return self.nombre
    
class Ticket(models.Model):
    correo = models.TextField(max_length=255)
    tipo = models.TextField(max_length=255)
    descripcion = models.TextField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    
class JornadaCaja(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntoventa = models.ForeignKey(PuntodeVenta, on_delete=models.CASCADE)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_inicial = models.IntegerField(default=0) # Sencillo / vuelto inicial
    total_ventas = models.IntegerField(default=0)
    monto_contado = models.IntegerField(default=0) # Cuadratura física en billetes/monedas
    diferencia = models.IntegerField(default=0)    # monto_contado - (monto_inicial + total_ventas)
    estado = models.TextField(max_length=15, default="ABIERTA")
    
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    puntoventa = models.ForeignKey(PuntodeVenta, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    tipo_venta = models.TextField(max_length=20, default="BARRA") # BARRA (inmediata) o MESA (garzón)
    estado = models.TextField(max_length=20, default="PENDIENTE") # PAGADA, PENDIENTE, ANULADA
    def __str__(self):
        return f"Folio #{self.id} - {self.estado}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    subtotal = models.IntegerField(default=0)