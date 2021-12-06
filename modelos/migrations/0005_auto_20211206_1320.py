# Generated by Django 3.2.8 on 2021-12-06 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0004_auto_20211206_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='fechaFinal',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='observacion',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='plantas',
            field=models.ManyToManyField(blank=True, to='modelos.Planta'),
        ),
    ]
