# Generated by Django 5.0.9 on 2024-11-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='cod_articulo',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Código Artículo'),
        ),
    ]
