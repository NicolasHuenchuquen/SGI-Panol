from django import forms
from .models import SolicitudArticulo
from django.forms import DateInput, TimeInput

class SolicitudArticuloForm(forms.ModelForm):
    class Meta:
        model = SolicitudArticulo
        fields = ['nombre_apellido', 'rut', 'asignatura', 'fecha_salida', 'hora_salida', 'fecha_devolucion', 'hora_devolucion', 'cod_articulo', 'cantidad']
        widgets = {
            'fecha_salida': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_salida': TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'fecha_devolucion': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_devolucion': TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if SolicitudArticulo.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")
        return rut
