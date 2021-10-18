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


class MenuViewSet(viewsets.ModelViewSet):
    queryset = OpcionMenu.objects.all()
    serializer_class = OpcionMenuSerializer
    def get_queryset(self):
        id_grupos = []
        for g in self.request.user.groups.all():
            id_grupos.append(g.pk)
        queryset = OpcionMenu.objects.filter(grupo_id__in=id_grupos).order_by('opcion_padre','pk')
        return queryset
