# Generated by Django 5.0.9 on 2024-11-10 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud_articulos', '0003_alter_solicitudarticulo_fecha_devolucion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='rut',
            field=models.CharField(max_length=12),
        ),
    ]
