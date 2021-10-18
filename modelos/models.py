from django.db import models
from django.contrib.auth.models import User, Group


class Persona(models.Model):
    nuid = models.CharField(max_length=64, unique=True, blank=False, null=False)
    direccion = models.CharField(max_length=128, blank=False, null=False)
    telefono = models.CharField(max_length=128, blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.usuario.first_name + ' (' + self.nuid + ')'
    class Meta:
        ordering = ('nuid',)

class OpcionMenu(models.Model):
    label = models.CharField(max_length=256, blank=False, null=False)
    ruta = models.CharField(max_length=256, blank=True, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.PROTECT)
    opcion_padre = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return '[' + self.grupo.name + '] ' + self.label
    class Meta:
        ordering = ('label',)
