# Generated by Django 3.2.8 on 2021-12-01 20:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0002_auto_20211128_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cultivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.DateField()),
                ('finca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.finca')),
                ('tipoCultivo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.tipocultivo')),
            ],
            options={
                'verbose_name_plural': 'Cultivo - 01 Cultivos',
                'ordering': ('finca', 'tipoCultivo', 'fechaInicio'),
            },
        ),
        migrations.CreateModel(
            name='EstadoPlanta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=512)),
                ('icono', models.CharField(max_length=64)),
                ('nivel', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Estados planta',
                'ordering': ('nivel',),
            },
        ),
        migrations.CreateModel(
            name='EstadoPlantaObservacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('observacion', models.CharField(max_length=64)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.empleado')),
                ('estadoPlanta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.estadoplanta')),
            ],
            options={
                'verbose_name_plural': 'Estados de la planta',
                'ordering': ('fecha',),
            },
        ),
        migrations.AddField(
            model_name='tareaplantilla',
            name='insumos',
            field=models.ManyToManyField(blank=True, through='modelos.InsumoTareaPlantilla', to='modelos.Insumo'),
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generacion', models.IntegerField(default=1)),
                ('linea', models.IntegerField(default=1)),
                ('consecutivo', models.IntegerField(default=1)),
                ('fechaSiembra', models.DateField()),
                ('cultivo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.cultivo')),
                ('estadosPlanta', models.ManyToManyField(blank=True, through='modelos.EstadoPlantaObservacion', to='modelos.EstadoPlanta')),
                ('posicion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.posicion')),
            ],
            options={
                'verbose_name_plural': 'Plantas',
                'ordering': ('fechaSiembra',),
            },
        ),
        migrations.AddField(
            model_name='estadoplantaobservacion',
            name='planta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.planta'),
        ),
    ]
