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
 
class UnidadMedida(models.Model):
   unidadMedida = models.CharField(max_length=256, blank=False, null=False)
   abreviatura = models.CharField(max_length=18, blank=False, null=False)
   def __str__(self):
       return self.unidadMedida
   class Meta:
       ordering = ('unidadMedida',)
 
class UnidadTiempo(models.Model):
   unidadTiempo = models.CharField(max_length=256, blank=False, null=False)
   minutos = models.IntegerField(null=False, default=0)
   def __str__(self):
       return self.unidadTiempo
   class Meta:
       ordering = ('minutos',)
 
class TipoInsumo(models.Model):
   tipoInsumo = models.CharField(max_length=256, blank=False, null=False)
   def __str__(self):
       return self.tipoInsumo
   class Meta:
       ordering = ('tipoInsumo',)
 
class Periodicidad(models.Model):
   periodicidad = models.CharField(max_length=256, blank=False, null=False)
   cantidad = models.IntegerField(null=False, default=0)
   unidadTiempo = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT)
   def __str__(self):
       return self.periodicidad
   class Meta:
       ordering = ('periodicidad',)
 
class Insumo(models.Model):
   nombreInsumo = models.CharField(max_length=256, blank=False, null=False)
   unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
   tipoInsumo = models.ForeignKey(TipoInsumo, on_delete=models.PROTECT)
   def __str__(self):
       return self.nombreInsumo
   class Meta:
       ordering = ('nombreInsumo',)
 
class TipoCultivo(models.Model):
   tipoCultivo = models.CharField(max_length=256, blank=False, null=False)
   def __str__(self):
       return self.tipoCultivo
   class Meta:
       ordering = ('tipoCultivo',)
 
class FaseCultivo(models.Model):
   tipoCultivo = models.ForeignKey(TipoCultivo, on_delete=models.PROTECT)
   faseCultivo = models.CharField(max_length=256, blank=False, null=False)
   orden = models.IntegerField(null=False, default=0)
   def __str__(self):
       return str(self.tipoCultivo) + ' ' + str(self.orden) + ' ' + self.faseCultivo
   class Meta:
       ordering = ('orden',)
 
class TareaPlantilla(models.Model):
   faseCultivo = models.ForeignKey(FaseCultivo, on_delete=models.PROTECT)
   tarea = models.CharField(max_length=256, blank=False, null=False)
   descripcion = models.CharField(max_length=2048, blank=False, null=False)
   duracion = models.IntegerField(null=False, default=0)
   unidadTiempo = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT)
   jornalesHectarea = models.IntegerField(null=False, default=0)
   periodicidad = models.ForeignKey(Periodicidad, on_delete=models.PROTECT, default=1)
   orden = models.IntegerField(null=False, default=0)
   def __str__(self):
       return str(self.faseCultivo) + ', ' + str(self.orden) + ') ' + self.tarea
   class Meta:
       ordering = ('orden','tarea',)
 
class InsumoTareaPlantilla(models.Model):
   tareaPlantilla = models.ForeignKey(TareaPlantilla, on_delete=models.PROTECT)
   insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
   cantidadInsumo = models.IntegerField(null=False, default=0)
   def __str__(self):
       return str(self.tareaPlantilla) + ': ' + self.insumo.nombreInsumo + ' -> ' + str(self.cantidadInsumo)
