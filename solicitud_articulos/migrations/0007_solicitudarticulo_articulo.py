# Generated by Django 5.0.9 on 2024-11-13 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_inventario', '0005_alter_articulo_cod_articulo'),
        ('solicitud_articulos', '0006_solicitudarticulo_estado_devolucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudarticulo',
            name='articulo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestor_inventario.articulo'),
        ),
    ]
