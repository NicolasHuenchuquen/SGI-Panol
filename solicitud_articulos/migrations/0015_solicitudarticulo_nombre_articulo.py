# Generated by Django 5.0.9 on 2024-11-14 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud_articulos', '0014_remove_solicitudarticulo_articulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudarticulo',
            name='nombre_articulo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
