# Generated by Django 5.0.9 on 2024-11-14 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_inventario', '0005_alter_articulo_cod_articulo'),
        ('solicitud_articulos', '0009_alter_solicitudarticulo_estado_devolucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudarticulo',
            name='articulo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestor_inventario.articulo'),
        ),
    ]
