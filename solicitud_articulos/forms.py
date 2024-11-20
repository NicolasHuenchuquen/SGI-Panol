from django import forms
from .models import SolicitudArticulo
from django.forms import DateInput, TimeInput
from django import forms
import re
from gestor_inventario.models import Articulo
from solicitud_articulos.models import SolicitudArticulo

class SolicitudArticuloForm(forms.ModelForm):
    class Meta:
        model = SolicitudArticulo
        fields = ['rut', 'nombre_apellido', 'asignatura', 'fecha_salida', 'hora_salida', 'fecha_devolucion', 'hora_devolucion', 'cod_articulo', 'cantidad', 'tipo_solicitante']
        widgets = {
            'fecha_salida': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_salida': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'fecha_devolucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_devolucion': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }
        
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        # Se elimina la validación que impedía que el mismo RUT haga varias solicitudes
        return rut

    def clean_cod_articulo(self):
        cod_articulo = self.cleaned_data.get('cod_articulo')
        fecha_salida = self.cleaned_data.get('fecha_salida')
        hora_salida = self.cleaned_data.get('hora_salida')

        # Validación para permitir el mismo RUT, pero solo si la fecha y hora son diferentes
        existing_requests = SolicitudArticulo.objects.filter(rut=self.cleaned_data.get('rut'), cod_articulo=cod_articulo, fecha_salida=fecha_salida, hora_salida=hora_salida)
        if existing_requests.exists():
            raise forms.ValidationError("Ya se ha solicitado este artículo para la misma fecha y hora.")

        return cod_articulo
    
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
    
    def clean_cod_articulo(self):
        cod_articulo = self.cleaned_data.get('cod_articulo')

        # Validar que el código comience con los prefijos permitidos
        if not cod_articulo.startswith(('CFTN', 'cftn', 'IPN', 'ipn')):
            raise forms.ValidationError(
                "El código del artículo debe comenzar con uno de los siguientes prefijos: 'CFTN', 'cftn', 'IPN', 'ipn'."
            )

        # Comprobar si el código existe en la base de datos
        if not Articulo.objects.filter(cod_articulo=cod_articulo).exists():
            raise forms.ValidationError("El código ingresado no está en el sistema.")

        return cod_articulo

