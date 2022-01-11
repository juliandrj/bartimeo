import django
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import *
from modelos.models import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class OpcionMenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OpcionMenu.objects.all()
    serializer_class = OpcionMenuSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OpcionMenu.objects.all()
    serializer_class = OpcionMenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        id_grupos = []
        for g in self.request.user.groups.all():
            id_grupos.append(g.pk)
        queryset = OpcionMenu.objects.filter(grupo_id__in=id_grupos).order_by('opcion_padre','pk')
        return queryset


class EmpleadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Empleado.objects.filter(id=self.request.user.id)


class FincaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializer
    permission_classes = [permissions.IsAuthenticated]


class CultivoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cultivo.objects.all()
    serializer_class = CultivoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        fincaId = self.request.query_params.get('finca', None)
        if fincaId is not None:
            queryset = Cultivo.objects.filter(finca__id=fincaId)
        else:
            queryset = Cultivo.objects.all()
        return queryset


class PlantaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        cultivoId = self.request.query_params.get('cultivo', None)
        if cultivoId is not None:
            queryset = Planta.objects.filter(cultivo__id=cultivoId)
        else:
            queryset = Planta.objects.all()
        return queryset


class TareaViewSet(viewsets.ReadOnlyModelViewSet):
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


class MisTareasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Tarea.objects.filter(responsables__id=self.request.user.id).order_by('-fechaInicial')
