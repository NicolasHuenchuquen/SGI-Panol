from django import forms
from .models import SolicitudArticulo
from django.forms import DateInput, TimeInput

class SolicitudArticuloForm(forms.ModelForm):
    class Meta:
        model = SolicitudArticulo
        fields = ['rut', 'nombre_apellido', 'asignatura', 'fecha_salida', 'hora_salida', 'fecha_devolucion', 'hora_devolucion', 'cod_articulo', 'cantidad']
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
