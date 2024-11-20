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
    cod_articulo = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    tipo_solicitante = models.CharField(max_length=10, choices=TIPO_SOLICITANTE_CHOICES, default='otro',)
    estado_devolucion = models.CharField(max_length=50, choices=ESTADO_DEVOLUCION_CHOICES, default='no devuelto',)

    def __str__(self):
        return f"{self.nombre_apellido} - RUT: {self.rut} - Asignatura: {self.asignatura}"

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        # Eliminar espacios en blanco al principio y al final
        rut = rut.strip()

        # Verificar que no exceda los 9 caracteres
        if len(rut) > 9:
            raise forms.ValidationError("El RUT no puede exceder los 9 caracteres.")

        # Verificar que no contenga puntos ni guiones y solo números o 'k'
        if not re.match(r'^\d{1,8}[kK0-9]$', rut):
            raise forms.ValidationError("El RUT debe contener solo números y un dígito verificador ('k' o número), sin puntos ni guiones.")

        return rut
    
    def clean_nombre_apellido(self):
        nombre_apellido = self.cleaned_data.get('nombre_apellido')

        # Elimina espacios en blanco adicionales
        nombre_apellido = nombre_apellido.strip()

        # Verifica que solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_apellido):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios, sin números ni caracteres especiales.")

        return nombre_apellido