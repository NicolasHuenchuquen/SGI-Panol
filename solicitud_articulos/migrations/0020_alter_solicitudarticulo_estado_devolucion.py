# Generated by Django 5.0.9 on 2024-11-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud_articulos', '0019_alter_solicitudarticulo_cantidad4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='estado_devolucion',
            field=models.CharField(choices=[('Devuelto', 'Devuelto'), ('Parcialmente devuelto', 'Parcialmente devuelto'), ('No devuelto', 'No devuelto')], default='no devuelto', max_length=50),
        ),
    ]