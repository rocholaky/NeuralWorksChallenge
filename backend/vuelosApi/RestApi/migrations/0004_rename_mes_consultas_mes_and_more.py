# Generated by Django 4.1 on 2023-02-25 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestApi', '0003_consultas_vuelo_i'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consultas',
            old_name='mes',
            new_name='MES',
        ),
        migrations.RenameField(
            model_name='consultas',
            old_name='opera',
            new_name='OPERA',
        ),
        migrations.RenameField(
            model_name='consultas',
            old_name='tipovuelo',
            new_name='TIPOVUELO',
        ),
        migrations.RenameField(
            model_name='consultas',
            old_name='vuelo_i',
            new_name='VLO_I',
        ),
        migrations.RemoveField(
            model_name='consultas',
            name='fecha_vuelo',
        ),
        migrations.AddField(
            model_name='consultas',
            name='PREDICCION',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
