from django.db import models
from django.utils import timezone
from django import forms
import re

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

    #Es la cosa más ineficiente que he hecho en mi vida. Se puede optimizar creando 2 modelos, uno para el solicitante, y otro para el/los articulos. 
    #La idea es que se vincule la solicitud del articulo al solicitante mediante ids, y que se manejen solo dos variables con diccionarios dentro.
    #No se pudo realizar de esa forma, pero probablemente se puede mejorar, para quien se anime a realizarlo

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

    def __str__(self):
        return f"{self.nombre_apellido} - RUT: {self.rut} - Asignatura: {self.asignatura}"

    