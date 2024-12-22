from django.db import models
from django.utils import timezone
from django import forms
import re
from datetime import datetime

class SolicitudArticulo(models.Model):
    TIPO_SOLICITANTE_CHOICES = [
        ('docente', 'Docente'),
        ('otro', 'Otro'),
    ]

    ESTADO_DEVOLUCION_CHOICES = [
        ('devuelto', 'Devuelto'),
        ('parcialmente devuelto', 'Parcialmente devuelto'),
        ('no devuelto', 'No devuelto'),
    ]

    nombre_apellido = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    asignatura = models.CharField(max_length=255)
    fecha_salida = models.DateField() 
    hora_salida = models.TimeField()   
    fecha_devolucion = models.DateField()  
    hora_devolucion = models.TimeField()
    

    cod_articulo1 = models.CharField(max_length=50)
    cantidad1 = models.PositiveIntegerField()

    cod_articulo2 = models.CharField(max_length=50, blank=True, null=True)
    cantidad2 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo3 = models.CharField(max_length=50, blank=True, null=True)
    cantidad3 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo4 = models.CharField(max_length=50, blank=True, null=True)
    cantidad4 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo5 = models.CharField(max_length=50, blank=True, null=True)
    cantidad5 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo6 = models.CharField(max_length=50, blank=True, null=True)
    cantidad6 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo7 = models.CharField(max_length=50, blank=True, null=True)
    cantidad7 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo8 = models.CharField(max_length=50, blank=True, null=True)
    cantidad8 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo9 = models.CharField(max_length=50, blank=True, null=True)
    cantidad9 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo10 = models.CharField(max_length=50, blank=True, null=True)
    cantidad10 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo11 = models.CharField(max_length=50, blank=True, null=True)
    cantidad11 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo12 = models.CharField(max_length=50, blank=True, null=True)
    cantidad12 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo13 = models.CharField(max_length=50, blank=True, null=True)
    cantidad13 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo14 = models.CharField(max_length=50, blank=True, null=True)
    cantidad14 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo15 = models.CharField(max_length=50, blank=True, null=True)
    cantidad15 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo16 = models.CharField(max_length=50, blank=True, null=True)
    cantidad16 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo17 = models.CharField(max_length=50, blank=True, null=True)
    cantidad17 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo18 = models.CharField(max_length=50, blank=True, null=True)
    cantidad18 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo19 = models.CharField(max_length=50, blank=True, null=True)
    cantidad19 = models.PositiveIntegerField(blank=True, null=True)

    cod_articulo20 = models.CharField(max_length=50, blank=True, null=True)
    cantidad20 = models.PositiveIntegerField(blank=True, null=True)


    tipo_solicitante = models.CharField(max_length=10, choices=TIPO_SOLICITANTE_CHOICES, default='otro',)
    estado_devolucion = models.CharField(max_length=50, choices=ESTADO_DEVOLUCION_CHOICES, default='no devuelto',)
    atrasado = models.BooleanField(default=False)#PARA VER LOS ARTICULOS ATRASADOS
    encargado = models.CharField(max_length=255, blank=True)  # Campo para almacenar el nombre y apellido del encargado

    def save(self, *args, **kwargs):
            # Obtener el usuario de los argumentos adicionales
            user = kwargs.pop('user', None)

            # Si el usuario existe, guardar su nombre y apellido
            if user:
                self.encargado = f"{user.first_name} {user.last_name}".strip()

            # Transformar todos los campos cod_articulo1 a cod_articulo20 a mayúsculas antes de guardar
            for i in range(1, 21):
                cod_articulo_field = f'cod_articulo{i}'
                cod_articulo_value = getattr(self, cod_articulo_field, None)
                if cod_articulo_value:
                    setattr(self, cod_articulo_field, cod_articulo_value.strip().upper())

            # Llamar al método `save` del modelo para guardar la instancia
            super(SolicitudArticulo, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.nombre_apellido} - RUT: {self.rut} - Asignatura: {self.asignatura}"

    