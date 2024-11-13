from django.db import models
from django.utils import timezone

class SolicitudArticulo(models.Model):
    TIPO_SOLICITANTE_CHOICES = [
        ('docente', 'Docente'),
        ('otro', 'Otro'),
    ]

    ESTADO_DEVOLUCION_CHOICES = [
        ('devuelto', 'Devuelto'),
        ('no devuelto', 'No devuelto'),
    ]

    nombre_apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    asignatura = models.CharField(max_length=255)
    fecha_salida = models.DateField() 
    hora_salida = models.TimeField()   
    fecha_devolucion = models.DateField()  
    hora_devolucion = models.TimeField()   
    cod_articulo = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    tipo_solicitante = models.CharField(max_length=10, choices=TIPO_SOLICITANTE_CHOICES, default='otro',)
    estado_devolucion = models.CharField(max_length=20, choices=ESTADO_DEVOLUCION_CHOICES, default='no devuelto',)

    def __str__(self):
        return f"{self.nombre_apellido} - RUT: {self.rut} - Asignatura: {self.asignatura}"
