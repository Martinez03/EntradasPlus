# Generated by Django 5.1.1 on 2024-10-27 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradasplus', '0009_perfilusuario_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='apellidos',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='nombre',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]