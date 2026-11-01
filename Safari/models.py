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
    
class Mesa(models.Model):
    nombre = models.TextField(max_length=30)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class PuntodeVenta(models.Model):
    nombre = models.TextField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Producto(models.Model):
    nombre = models.TextField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=255)
    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    correo = models.TextField(max_length=255)
    tipo = models.TextField(max_length=255)
    descripcion = models.TextField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)