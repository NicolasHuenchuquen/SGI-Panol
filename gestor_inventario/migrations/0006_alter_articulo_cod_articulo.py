# Generated by Django 5.0.9 on 2024-11-14 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_inventario', '0005_alter_articulo_cod_articulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='cod_articulo',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, unique=True, verbose_name='Código Artículo'),
        ),
    ]