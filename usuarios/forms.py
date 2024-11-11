from django import forms
from django.contrib.auth.models import User
from .models import Perfil

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
        if Perfil.objects.filter(rut=rut).exists():
            raise ValidationError("Este RUT ya está registrado.")
        return rut
