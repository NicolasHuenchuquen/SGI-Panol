from django import forms
from .models import Articulo
from django.core.exceptions import ValidationError
from django.core import validators

def validate_cod_articulo(value):
    if not (value.startswith('CFTN') or value.startswith('IPN')):
        raise ValidationError(
            'El código de artículo debe comenzar con "CFTN" o "IPN".'
        )

class FormArticulo(forms.ModelForm):
    
    cod_articulo = forms.CharField(
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(8),validate_cod_articulo],
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-top: 13px'}),
    )

    nombre = forms.CharField(
        validators=[validators.MinLengthValidator(3), validators.MaxLengthValidator(100)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    cantidad = forms.IntegerField(
        min_value=1,  # Asegúrate de que la cantidad sea al menos 1
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_value': 'La cantidad debe ser un número positivo.'
        }
    )

    grupo = forms.ChoiceField(
        choices=[('CFTN', 'CFTN'), ('IPN', 'IPN')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tipo_articulo = forms.ChoiceField(
        choices=[('Insumo', 'INSUMO'), ('Activo', 'ACTIVO')],
        widget=forms.Select(attrs={'class': 'form-select', 'style':'margin-top: 13px'})
    )

    ubicacion = forms.CharField(
        validators=[validators.MinLengthValidator(2), validators.MaxLengthValidator(8)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    observacion = forms.CharField(
        required=False,
        validators=[validators.MinLengthValidator(0)],
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    class Meta:
        model = Articulo
        fields = '__all__'