from django.db import models
from django.utils import timezone

class SolicitudArticulo(models.Model):
    nombre_apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    asignatura = models.CharField(max_length=255)
    fecha_salida = models.DateField() 
    hora_salida = models.TimeField()   
    fecha_devolucion = models.DateField()  
    hora_devolucion = models.TimeField()   
    cod_articulo = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre_apellido} - RUT: {self.rut} - Asignatura: {self.asignatura}"
