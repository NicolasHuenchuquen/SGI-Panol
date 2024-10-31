from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    ADMINISTRADOR = 'administrador'
    PANOLERO = 'panolero'
    TIPOS_USUARIO = [
        (ADMINISTRADOR, 'Administrador'),
        (PANOLERO, 'Pañolero'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default=PANOLERO)
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario} - RUT: {self.rut}"
