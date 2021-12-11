from django.contrib.auth.models import User, Group
from django.db.models import fields
from rest_framework import serializers
from modelos.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'groups']

class PersonaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Persona
        fields = ('nuid','usuario','direccion','telefono',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class OpcionMenuSerializer(serializers.ModelSerializer):
    opcion_padre = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')
    class Meta:
        model = OpcionMenu
        fields = ('id', 'label', 'ruta', 'grupo', 'opcion_padre')


class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = ('longitud','latitud','altura',)


class EstadoPlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPlanta
        fields = ('etiqueta','icono','nivel',)


class FincaSerializer(serializers.ModelSerializer):
    posicion = PosicionSerializer(many=False, read_only=True)
    class Meta:
        model = Finca
        fields = ('nombreFinca','vereda','posicion')


class EmpleadoSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(many=False, read_only=True)
    finca = FincaSerializer(many=False, read_only=True)
    class Meta:
        model = Empleado
        fields = ('finca','persona','fechaContrato','activo')


class EstadosPlantaObservacionSerializer(serializers.ModelSerializer):
    estadoPlanta = EstadoPlantaSerializer(many = False, read_only = True)
    empleado = EmpleadoSerializer(many = False, read_only = True)
    class Meta:
        model = EstadoPlantaObservacion
        fields = ('estadoPlanta','empleado','fecha','observacion',)


class PlantaSerializer(serializers.ModelSerializer):
    posicion = PosicionSerializer(many = False, read_only = True)
    class Meta:
        model = Planta
        fields = ('id','cultivo','generacion','linea','consecutivo','fechaSiembra','posicion',)


class TareaPlantillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaPlantilla
        fields = ('tareaPlantilla','descripcion',)


class TareaSerializer(serializers.ModelSerializer):
    tareaPlantilla = TareaPlantillaSerializer(many=False, read_only=True)
    class Meta:
        model = Tarea
        fields = ('tareaPlantilla','fechaInicial','fechaFinal','observacion',)
