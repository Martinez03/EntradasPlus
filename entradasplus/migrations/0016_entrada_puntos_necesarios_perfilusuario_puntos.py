# Generated by Django 5.1.1 on 2024-11-16 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradasplus', '0015_reseña_empresa_alter_reseña_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='puntos_necesarios',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='puntos',
            field=models.IntegerField(default=50),
        ),
    ]
