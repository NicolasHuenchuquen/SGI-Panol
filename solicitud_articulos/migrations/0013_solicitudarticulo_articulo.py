# Generated by Django 5.0.9 on 2024-11-14 00:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_inventario', '0006_alter_articulo_cod_articulo'),
        ('solicitud_articulos', '0012_remove_solicitudarticulo_articulo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudarticulo',
            name='articulo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestor_inventario.articulo'),
        ),
    ]
