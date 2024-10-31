from django import forms
from django.contrib.auth.models import User
from .models import Perfil

from django.core.exceptions import ValidationError

class PanoleroCreationForm(forms.ModelForm):
    rut = forms.CharField(max_length=12)  # Campo para el RUT
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    tipo_usuario = forms.ChoiceField(choices=Perfil.TIPOS_USUARIO, initial=Perfil.ADMINISTRADOR)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'rut', 'confirm_password', 'tipo_usuario']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        # Establecer is_staff dependiendo del tipo de usuario
        if self.cleaned_data['tipo_usuario'] == Perfil.ADMINISTRADOR:
            user.is_staff = True
        else:
            user.is_staff = False

        if commit:
            user.save()
            # Crear perfil después de guardar el usuario
            Perfil.objects.create(user=user, rut=self.cleaned_data['rut'], tipo_usuario=self.cleaned_data['tipo_usuario'])
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
