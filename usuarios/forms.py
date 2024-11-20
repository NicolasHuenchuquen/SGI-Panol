from django import forms
from django.contrib.auth.models import User
from .models import Perfil
import re

from django.core.exceptions import ValidationError

class PanoleroCreationForm(forms.ModelForm):
    rut = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user.is_staff = False 

        if commit:
            user.save() 
            Perfil.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                tipo_usuario=Perfil.PANOLERO  # Se establece directamente a 'Pañolero'
            )
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        return cleaned_data

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        # Eliminar espacios y validar longitud máxima
        rut = rut.replace(" ", "").upper()  # Convertir a mayúsculas y quitar espacios
        if len(rut) > 9:
            raise ValidationError("El RUT no puede tener más de 9 caracteres.")

        # Validar que sólo tenga caracteres permitidos (números y 'K')
        if not re.match(r'^\d{1,8}[0-9K]$', rut):
            raise ValidationError("El RUT debe contener solo números o la letra K, sin puntos ni guiones.")

        # Validar el dígito verificador (opcional, si deseas verificar su corrección)
        if not self.validar_digito_verificador(rut):
            raise ValidationError("El RUT ingresado no es válido.")

        # Verificar unicidad
        if Perfil.objects.filter(rut=rut).exists():
            raise ValidationError("Este RUT ya está registrado.")

        return rut

    def validar_digito_verificador(self, rut):
        """
        Valida el dígito verificador de un RUT chileno.
        """
        cuerpo = rut[:-1]
        dv = rut[-1]

        # Calcular dígito verificador
        suma = 0
        multiplicador = 2

        for numero in reversed(cuerpo):
            suma += int(numero) * multiplicador
            multiplicador = 9 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)
        dv_calculado = "K" if resto == 10 else "0" if resto == 11 else str(resto)

        return dv == dv_calculado