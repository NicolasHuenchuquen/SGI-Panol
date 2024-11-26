from django import forms
from .models import SolicitudArticulo
from django.forms import DateInput, TimeInput
import re
from gestor_inventario.models import Articulo

class SolicitudArticuloForm(forms.ModelForm):
    class Meta:
        model = SolicitudArticulo
        fields = ['rut', 'nombre_apellido', 'asignatura', 'fecha_salida', 'hora_salida',
                  'fecha_devolucion', 'hora_devolucion', 'tipo_solicitante'] + \
                 [f'cod_articulo{i}' for i in range(1, 21)] + \
                 [f'cantidad{i}' for i in range(1, 21)]
        widgets = {
            'fecha_salida': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_salida': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'fecha_devolucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_devolucion': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean_cod_articulo(self):
        cod_articulos_existentes = set(Articulo.objects.values_list('cod_articulo', flat=True))

        for i in range(1, 21):
            cod_articulo_field = f'cod_articulo{i}'
            cod_articulo = self.cleaned_data.get(cod_articulo_field)
            if cod_articulo:
                if not cod_articulo.startswith(('CFTN', 'cftn', 'IPN', 'ipn')):
                    raise forms.ValidationError(
                        f"El código del artículo en {cod_articulo_field} debe comenzar con "
                        "'CFTN', 'cftn', 'IPN' o 'ipn'."
                    )
                if cod_articulo not in cod_articulos_existentes:
                    raise forms.ValidationError(
                        f"El código {cod_articulo} ingresado en {cod_articulo_field} no está en el sistema."
                    )
        return self.cleaned_data

    def clean_rut(self):
        rut = self.cleaned_data.get('rut').strip()
        if len(rut) > 9 or not re.match(r'^\d{1,8}[kK0-9]$', rut):
            raise forms.ValidationError(
                "El RUT debe contener máximo 9 caracteres, solo números y un dígito verificador ('k' o número), sin puntos ni guiones."
            )
        return rut

    def clean_nombre_apellido(self):
        nombre_apellido = self.cleaned_data.get('nombre_apellido').strip()
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_apellido):
            raise forms.ValidationError(
                "El nombre solo puede contener letras y espacios, sin números ni caracteres especiales."
            )
        return nombre_apellido
    
    def clean(self):
        cleaned_data = super().clean()
        errores_generales = []

        for i in range(1, 21):
            cod_articulo_field = f'cod_articulo{i}'
            cantidad_field = f'cantidad{i}'
            cod_articulo = cleaned_data.get(cod_articulo_field)
            cantidad = cleaned_data.get(cantidad_field)

            # Validar que si hay un artículo, la cantidad sea mayor a 0
            if cod_articulo and (cantidad is None or cantidad <= 0):
                mensaje_error = f"La cantidad para {cod_articulo_field} no puede ser 0 o estar vacía."
                # Asociar error al campo cantidad correspondiente
                self.add_error(cantidad_field, mensaje_error)
                # También agregar el error a una lista global, por si se quiere mostrar como mensaje general
                errores_generales.append(mensaje_error)

        # Si hay errores generales, asociarlos al formulario
        if errores_generales:
            # Usamos ValidationError para mostrar los errores generales
            raise forms.ValidationError(errores_generales)

        return cleaned_data