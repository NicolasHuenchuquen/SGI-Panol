# Generated by Django 5.0.9 on 2024-11-10 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud_articulos', '0002_alter_solicitudarticulo_fecha_devolucion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='fecha_devolucion',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='fecha_salida',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='hora_devolucion',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='hora_salida',
            field=models.TimeField(),
        ),
    ]
