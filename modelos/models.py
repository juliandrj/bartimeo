from django.db import models
from django.contrib.auth.models import User, Group
 
'''
AUTENTICACION
'''
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

'''
PLANTILLA TAREAS
''' 
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
    tipoInsumoPadre = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
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

class Distribucion(models.Model):
    distanciaLinea = models.IntegerField(null=False)
    distanciaPlanta = models.IntegerField(null=False)
    def __str__(self):
        return str(self.distanciaLinea) + 'x' + str(self.distanciaPlanta)

class TipoCultivo(models.Model):
    tipoCultivo = models.CharField(max_length=256, blank=False, null=False)
    distribucion = models.ForeignKey(Distribucion, on_delete=models.PROTECT)
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
    tareaPlantilla = models.CharField(max_length=256, blank=False, null=False)
    descripcion = models.CharField(max_length=2048, blank=False, null=False)
    duracion = models.IntegerField(null=False, default=0)
    unidadTiempo = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT)
    jornalesHectarea = models.IntegerField(null=False, default=0)
    periodicidad = models.ForeignKey(Periodicidad, on_delete=models.PROTECT, default=1)
    orden = models.IntegerField(null=False, default=0)
    def __str__(self):
        return str(self.faseCultivo) + ', ' + str(self.orden) + ') ' + self.tareaPlantilla
    class Meta:
        ordering = ('orden','tareaPlantilla',)
 
class InsumoTareaPlantilla(models.Model):
    tareaPlantilla = models.ForeignKey(TareaPlantilla, on_delete=models.PROTECT)
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    cantidadInsumo = models.IntegerField(null=False, default=0)
    def __str__(self):
        return str(self.tareaPlantilla) + ': ' + self.insumo.nombreInsumo + ' -> ' + str(self.cantidadInsumo)

'''
FINCA
'''
class Posicion(models.Model):
    latitud = models.DecimalField(max_digits=15, decimal_places=15, null=False)
    longitud = models.DecimalField(max_digits=15, decimal_places=15, null=False)
    altura = models.IntegerField(null=False)
    def __str__(self):
       return '(' + str(self.latitud) + ', ' + str(self.longitud) + ', ' + str(self.altura) + ')'

class Pais(models.Model):
    pais = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
       return self.pais

class Departamento(models.Model):
    departamento = models.CharField(max_length=512, blank=False, null=False)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    def __str__(self):
       return str(self.pais) + ' ' + self.departamento

class Municipio(models.Model):
    municipio = models.CharField(max_length=512, blank=False, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    def __str__(self):
       return str(self.departamento) + ' ' + self.municipio

class Finca(models.Model):
    nombreFinca = models.CharField(max_length=2048, blank=False, null=False)
    vereda = models.CharField(max_length=2048, blank=False, null=False)
    posicion = models.ForeignKey(Posicion, on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.tareaPlantilla) + ': ' + self.insumo.nombreInsumo + ' -> ' + str(self.cantidadInsumo)

'''
INSUMOS
'''
class TipoFormulacion(models.Model):
    codigo = models.CharField(max_length=4, blank=False, null=False)
    denominacion = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
        return '(' + self.codigo + ') ' + self.denominacion

class CategoriaToxicologica(models.Model):
    codigo = models.CharField(max_length=4, blank=False, null=False)
    denominacion = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
        return '(' + self.codigo + ') ' + self.denominacion

class Agroquimico(Insumo):
    registroICA = models.IntegerField(null=False)
    fechaRegistro = models.DateField(null=False)
    empresa = models.CharField(max_length=2048, blank=False, null=False)
    tipoFormulacion = models.ForeignKey(TipoFormulacion, on_delete=models.PROTECT)
    categoriaToxico = models.ForeignKey(CategoriaToxicologica, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.tipoFormulacion) + str(self.categoriaToxico) + ' ' + self.nombreInsumo

class TipoFertilizante(models.Model):
    tipoFertilizante = models.CharField(max_length=64, blank=False, null=False)
    def __str__(self):
        return self.tipoFertilizante

class UsoFertilizante(models.Model):
    usoFertilizante = models.CharField(max_length=64, blank=False, null=False)
    def __str__(self):
        return self.usoFertilizante

class Fertilizante(Agroquimico):
    tipoFertilizante = models.ForeignKey(TipoFertilizante, on_delete=models.PROTECT)
    usoFertilizante = models.ForeignKey(UsoFertilizante, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.tipoFormulacion) + str(self.categoriaToxico) + ' ' + self.nombreInsumo + ' - ' + str(self.tipoFertilizante)

class Plaguicida(Agroquimico):
    modificaciones = models.CharField(max_length=2048, blank=False, null=False)
    ingredienteActivo = models.CharField(max_length=512, blank=False, null=False)
    cencentracion = models.CharField(max_length=512, blank=False, null=False)
    paisesOrigen = models.CharField(max_length=2048, blank=False, null=False)
    cultivos = models.CharField(max_length=2048, blank=False, null=False)
    def __str__(self):
        return str(self.tipoFormulacion) + str(self.categoriaToxico) + ' ' + self.nombreInsumo + ' - ' + self.ingredienteActivo

class Herramienta(Insumo):
    fechaCompra: models.DateField(null=False)
    tmanteminiento = models.ForeignKey(UsoFertilizante, on_delete=models.PROTECT)
    def __str__(self):
        return self.nombreInsumo

'''
INVENTARIO
'''
class Inventario(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT)
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    fechaActualizacion = models.DateTimeField(null=False)
    def __str__(self):
        return str(self.insumo) + ' (' + str(self.cantidad) + ')'

'''
PERSONAL
'''
class Empleado(Persona):
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT)
    fechaContrato = models.DateTimeField(null=False)
    def __str__(self):
        return str(self.finca) + ' ' + str(self.usuario)

'''
CULTIVO
'''
class Cultivo(TipoCultivo):
    fechaInicio = models.DateField(null=False)
    def __str__(self):
        return str(self.tipoCultivo) + ': ' + str(self.fechaInicio)

class EstadoPlanta(models.Model):
    estadoPlanta = models.CharField(max_length=128, blank=False, null=False)
    def __str__(self):
        return self.estadoPlanta

class Planta(models.Model):
    linea = models.IntegerField(default=0)
    consecutivo = models.IntegerField(default=0)
    viva = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=2048, blank=False, null=False)
    ultimaActualizacion = models.DateTimeField(null=True)
    estadoPlanta = models.ForeignKey(EstadoPlanta, on_delete=models.PROTECT)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.estadoPlanta) + ' | ' + str(self.cultivo) + ': ' + str(self.linea) + ', ' + str(self.consecutivo)
    class Meta:
        ordering = ('linea','consecutivo',)

'''
TAREAS
'''
class Tarea(TareaPlantilla):
    fechaInicio = models.DateTimeField(null=False)
    fechaFin = models.DateTimeField(null=False)
    finalizada = models.BooleanField(default=False)
    def __str__(self):
        return self.tarea + ': ' + str(self.fechaInicio) + ' - ' + str(self.fechaFin)

class Responsable(Empleado):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.tarea) + ': ' + str(self.usuario)

class Reserva(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT)
    inventario = models.ForeignKey(Inventario, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=0)
    cantidadUsada = models.IntegerField(default=0)
    def __str__(self):
        return str(self.tarea) + ': ' + str(self.inventario) + '(' + str(self.cantidadUsada) + '/' + str(self.cantidad) + ')'

class TareaPlanta(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT)
    realizada = models.BooleanField(default=False)
    fechaRealizada = models.DateTimeField(null=True)
    observaciones = models.CharField(max_length=2048, blank=False, null=False)
    def __str__(self):
        return str(self.tarea) + ': ' + str(self.planta)
