# Generated by Django 5.0.9 on 2024-11-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud_articulos', '0008_remove_solicitudarticulo_articulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='estado_devolucion',
            field=models.CharField(choices=[('devuelto', 'Devuelto'), ('parcialmente devuelto', 'Parcialmente devuelto'), ('no devuelto', 'No devuelto')], default='no devuelto', max_length=50),
        ),
    ]
