# Generated by Django 5.1.1 on 2024-10-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradasplus', '0011_alter_grupo_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='foto',
            field=models.ImageField(blank=True, default='grupos/default.webp', null=True, upload_to='grupos/'),
        ),
    ]
