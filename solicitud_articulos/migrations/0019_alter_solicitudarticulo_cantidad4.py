# Generated by Django 5.0.9 on 2024-11-23 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud_articulos', '0018_alter_solicitudarticulo_cantidad10_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudarticulo',
            name='cantidad4',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
