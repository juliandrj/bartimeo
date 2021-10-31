# Generated by Django 3.2.8 on 2021-10-24 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaseCultivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faseCultivo', models.CharField(max_length=256)),
                ('orden', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('orden',),
            },
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreInsumo', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('nombreInsumo',),
            },
        ),
        migrations.CreateModel(
            name='Periodicidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodicidad', models.CharField(max_length=256)),
                ('cantidad', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('periodicidad',),
            },
        ),
        migrations.CreateModel(
            name='TipoCultivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoCultivo', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('tipoCultivo',),
            },
        ),
        migrations.CreateModel(
            name='TipoInsumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoInsumo', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('tipoInsumo',),
            },
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidadMedida', models.CharField(max_length=256)),
                ('abreviatura', models.CharField(max_length=18)),
            ],
            options={
                'ordering': ('unidadMedida',),
            },
        ),
        migrations.CreateModel(
            name='UnidadTiempo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidadTiempo', models.CharField(max_length=256)),
                ('minutos', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('minutos',),
            },
        ),
        migrations.CreateModel(
            name='TareaPlantilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarea', models.CharField(max_length=256)),
                ('descripcion', models.CharField(max_length=2048)),
                ('duracion', models.IntegerField(default=0)),
                ('jornalesHectarea', models.IntegerField(default=0)),
                ('orden', models.IntegerField(default=0)),
                ('faseCultivo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.fasecultivo')),
                ('periodicidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='modelos.periodicidad')),
                ('unidadTiempo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.unidadtiempo')),
            ],
            options={
                'ordering': ('orden', 'tarea'),
            },
        ),
        migrations.AddField(
            model_name='periodicidad',
            name='unidadTiempo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.unidadtiempo'),
        ),
        migrations.CreateModel(
            name='InsumoTareaPlantilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadInsumo', models.IntegerField(default=0)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.insumo')),
                ('tareaPlantilla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.tareaplantilla')),
            ],
        ),
        migrations.AddField(
            model_name='insumo',
            name='tipoInsumo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.tipoinsumo'),
        ),
        migrations.AddField(
            model_name='insumo',
            name='unidadMedida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.unidadmedida'),
        ),
        migrations.AddField(
            model_name='fasecultivo',
            name='tipoCultivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.tipocultivo'),
        ),
    ]
