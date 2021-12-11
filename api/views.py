import django
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import *
from modelos.models import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class OpcionMenuViewSet(viewsets.ModelViewSet):
    queryset = OpcionMenu.objects.all()
    serializer_class = OpcionMenuSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = OpcionMenu.objects.all()
    serializer_class = OpcionMenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        id_grupos = []
        for g in self.request.user.groups.all():
            id_grupos.append(g.pk)
        queryset = OpcionMenu.objects.filter(grupo_id__in=id_grupos).order_by('opcion_padre','pk')
        return queryset


class EstadoPlantaObservacionViewSet(viewsets.ModelViewSet):
    queryset = EstadoPlantaObservacion.objects.all()
    serializer_class = EstadosPlantaObservacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        plantaId = self.request.query_params.get('planta', None)
        if plantaId is not None:
            queryset = EstadoPlantaObservacion.objects.filter(planta_id=plantaId).order_by('-fecha')
        else:
            queryset = EstadoPlantaObservacion.objects.all()
        return queryset


class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    permission_classes = [permissions.IsAuthenticated]


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        responsableId = self.request.query_params.get('responsable', None)
        plantaId = self.request.query_params.get('planta', None)
        if responsableId is not None:
            queryset = Tarea.objects.filter(responsables__id=responsableId).order_by('-fechaInicial')
        elif plantaId is not None:
            queryset = Tarea.objects.filter(plantas__id=plantaId).order_by('-fechaInicial')
        else:
            queryset = Tarea.objects.all()
        return queryset

