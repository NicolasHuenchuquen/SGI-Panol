from django import forms
from .models import Articulo
from django.core.exceptions import ValidationError
from django.core import validators

def validar_cod_articulo(value):

    value=value.upper()

    if not (value.startswith('CFTN') or value.startswith('IPN')):
        raise ValidationError(
            'El código del artículo debe comenzar con "CFTN" o "IPN".'
        )
    return value  

class FormArticuloInsumo(forms.ModelForm):
    
    cod_articulo = forms.CharField(
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(15),validar_cod_articulo],
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-top: 13px'}),
    )

    nombre = forms.CharField(
        validators=[validators.MinLengthValidator(3), validators.MaxLengthValidator(100)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    cantidad = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_value': 'La cantidad debe ser un número positivo.'
        }
    )

    grupo = forms.ChoiceField(
        choices=[('CFTN', 'CFTN'), ('IPN', 'IPN')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tipo_articulo = forms.CharField(
    initial='Insumo',  # Valor predeterminado
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':'margin-top: 13px',
        'readonly': 'readonly', 
    })
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
    
    #CLEAN FORMS INSUMO

    #Convierte el valor ingresado en mayusculas
    def clean_cod_articulo(self):
        cod_articulo = self.cleaned_data['cod_articulo']
        return cod_articulo.upper()  
    
    class Meta:
        model = Articulo
        fields = '__all__'

class FormArticuloActivo(forms.ModelForm):
    
    cod_articulo = forms.CharField(
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(15),validar_cod_articulo],
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-top: 13px'}),
    )

    nombre = forms.CharField(
        validators=[validators.MinLengthValidator(3), validators.MaxLengthValidator(100)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    cantidad = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_value': 'La cantidad debe ser un número positivo.'
        }
    )

    grupo = forms.ChoiceField(
        choices=[('CFTN', 'CFTN'), ('IPN', 'IPN')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tipo_articulo = forms.CharField(
    initial='Activo',  
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':'margin-top: 13px',
        'readonly': 'readonly', 
    })
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
    
    #CLEAN FORMS ACTIVO

    #Convierte el valor ingresado en mayusculas
    def clean_cod_articulo(self):
        cod_articulo = self.cleaned_data['cod_articulo']
        return cod_articulo.upper()  

    class Meta:
        model = Articulo
        fields = '__all__'

class FormArticuloEditar(forms.ModelForm):
    
    cod_articulo = forms.CharField(
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(15),validar_cod_articulo],
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'margin-top: 13px','readonly': 'readonly'}),
    )

    nombre = forms.CharField(
        validators=[validators.MinLengthValidator(3), validators.MaxLengthValidator(100)],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
        
    cantidad = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control', }),
        error_messages={
            'min_value': 'La cantidad debe ser un número positivo.'
        }
    )

    grupo = forms.ChoiceField(
        choices=[('CFTN', 'CFTN'), ('IPN', 'IPN')],
        widget=forms.Select(attrs={'class': 'form-select', 'readonly': 'readonly'})
    )

    tipo_articulo = forms.CharField(
    initial='Activo',  
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style':'margin-top: 13px',
        'readonly': 'readonly', 
    })
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
        fields = ['cod_articulo', 'grupo', 'tipo_articulo', 'nombre', 'cantidad', 'ubicacion', 'observacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Establecer el valor inicial del grupo si hay una instancia
            self.fields['grupo'].initial = self.instance.grupo