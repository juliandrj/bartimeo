from django.contrib.auth.models import User, Group
from rest_framework import serializers
from modelos.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class OpcionMenuSerializer(serializers.ModelSerializer):
    opcion_padre = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')
    class Meta:
        model = OpcionMenu
        fields = ('id', 'label', 'ruta', 'grupo', 'opcion_padre')
