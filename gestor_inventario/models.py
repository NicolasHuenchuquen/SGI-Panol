from django.db import models

# Create your models here.

class Articulo(models.Model):
    cod_articulo=models.CharField(primary_key=True,max_length=8,verbose_name="Código Artículo")
    grupo=models.CharField(max_length=4, verbose_name="Grupo")
    tipo_articulo=models.CharField(max_length=6, verbose_name="Tipo de Artículo")
    nombre=models.CharField(max_length=100, verbose_name="Nombre")
    cantidad=models.PositiveIntegerField(verbose_name="Cantidad")
    ubicacion=models.CharField(max_length=100, verbose_name="Ubicación")
    observacion=models.TextField(verbose_name="Observación")

    def __str__(self):
        return self.nombre