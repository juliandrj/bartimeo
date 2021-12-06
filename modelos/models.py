from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
 
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
        verbose_name_plural = 'Principal - Personas'

'''
MENU
''' 
class OpcionMenu(models.Model):
    label = models.CharField(max_length=256, blank=False, null=False)
    ruta = models.CharField(max_length=256, blank=True, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.PROTECT)
    opcion_padre = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return '[' + self.grupo.name + '] ' + self.label
    class Meta:
        ordering = ('label',)
        verbose_name_plural = 'Principal - Menú'

'''
UTILITARIAS GENERALES
'''
class Pais(models.Model):
    pais = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
       return self.pais
    class Meta:
        ordering = ('pais',)
        verbose_name_plural = 'Utilitarias - 01 Paises'

class Departamento(models.Model):
    departamento = models.CharField(max_length=512, blank=False, null=False)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    def __str__(self):
       return str(self.pais) + ' ' + self.departamento
    class Meta:
        ordering = ('pais','departamento',)
        verbose_name_plural = 'Utilitarias - 02 Departamentos'

class Municipio(models.Model):
    municipio = models.CharField(max_length=512, blank=False, null=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    def __str__(self):
       return str(self.departamento) + ' ' + self.municipio
    class Meta:
        ordering = ('departamento','municipio',)
        verbose_name_plural = 'Utilitarias - 03 Municipios'

class Posicion(models.Model):
    latitud = models.DecimalField(max_digits=22, decimal_places=16, null=False)
    longitud = models.DecimalField(max_digits=22, decimal_places=16, null=False)
    altura = models.IntegerField(null=False)
    def __str__(self):
       return '(' + str(self.latitud) + ', ' + str(self.longitud) + ', ' + str(self.altura) + ')'
    class Meta:
        verbose_name_plural = 'Utilitarias - 04 Posiciones globales (coordenadas)'

class UnidadMedida(models.Model):
    unidadMedida = models.CharField(max_length=256, blank=False, null=False)
    abreviatura = models.CharField(max_length=18, blank=False, null=False)
    def __str__(self):
        return self.unidadMedida
    class Meta:
        ordering = ('unidadMedida',)
        verbose_name_plural = 'Utilitarias - 05 Unidades de medida'

class UnidadTiempo(models.Model):
    unidadTiempo = models.CharField(max_length=256, blank=False, null=False)
    minutos = models.IntegerField(null=False, default=0)
    def __str__(self):
        return self.unidadTiempo
    class Meta:
        ordering = ('minutos',)
        verbose_name_plural = 'Utilitarias - 06 Unidades de tiempo'

class Periodicidad(models.Model):
    periodicidad = models.CharField(max_length=256, blank=False, null=False)
    cantidad = models.IntegerField(null=False, default=0)
    unidadTiempo = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT)
    def __str__(self):
        return self.periodicidad
    class Meta:
        ordering = ('periodicidad',)
        verbose_name_plural = 'Utilitarias - 07 Periodicidades'

'''
PLANTILLA TAREAS
''' 
class TipoInsumo(models.Model):
    tipoInsumo = models.CharField(max_length=256, blank=False, null=False)
    tipoInsumoPadre = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.tipoInsumo
    class Meta:
        ordering = ('tipoInsumo',)
        verbose_name_plural = 'Plantilla tareas - 01 Tipos de insumo'
 
class Insumo(models.Model):
    nombreInsumo = models.CharField(max_length=256, blank=False, null=False)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    tipoInsumo = models.ForeignKey(TipoInsumo, on_delete=models.PROTECT)
    def __str__(self):
        return self.nombreInsumo
    class Meta:
        ordering = ('nombreInsumo',)
        verbose_name_plural = 'Plantilla tareas - 02 Insumos'

class Distribucion(models.Model):
    distanciaLinea = models.IntegerField(null=False)
    distanciaPlanta = models.IntegerField(null=False)
    def __str__(self):
        return str(self.distanciaLinea) + 'x' + str(self.distanciaPlanta)
    class Meta:
        ordering = ('distanciaLinea','distanciaPlanta',)
        verbose_name_plural = 'Plantilla tareas - 03 Distribuciones de las plantas'

class TipoCultivo(models.Model):
    tipoCultivo = models.CharField(max_length=256, blank=False, null=False)
    distribucion = models.ForeignKey(Distribucion, on_delete=models.PROTECT)
    def __str__(self):
        return self.tipoCultivo
    class Meta:
        ordering = ('tipoCultivo',)
        verbose_name_plural = 'Plantilla tareas - 04 Tipos de cultivo'
 
class FaseCultivo(models.Model):
    tipoCultivo = models.ForeignKey(TipoCultivo, on_delete=models.PROTECT)
    faseCultivo = models.CharField(max_length=256, blank=False, null=False)
    orden = models.IntegerField(null=False, default=0)
    def __str__(self):
        return str(self.tipoCultivo) + ' ' + str(self.orden) + ' ' + self.faseCultivo
    class Meta:
        ordering = ('orden',)
        verbose_name_plural = 'Plantilla tareas - 05 Fases de cultivo'

class Hito(models.Model):
    hito = models.CharField(max_length=256, blank=False, null=False)
    duracionEstimada = models.IntegerField(null=False, default=0)
    unidadTiempo = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT, default=1)
    def __str__(self):
        return self.hito
    class Meta:
        ordering = ('hito',)
        verbose_name_plural = 'Plantilla tareas - 06 Hitos'

class TareaPlantilla(models.Model):
    tareaPlantilla = models.CharField(max_length=256, blank=False, null=False)
    descripcion = models.CharField(max_length=2048, blank=False, null=False)
    duracion = models.IntegerField(null=False, default=0)
    inicioDesde = models.IntegerField(null=False, default=0)
    plantasAfectadas = models.IntegerField(null=False, default=0)
    orden = models.IntegerField(null=False, default=0)
    faseCultivo = models.ForeignKey(FaseCultivo, on_delete=models.PROTECT)
    hito = models.ForeignKey(Hito, on_delete=models.PROTECT)
    unidadTiempo = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT)
    periodicidad = models.ForeignKey(Periodicidad, on_delete=models.PROTECT, default=1)
    insumos = models.ManyToManyField(Insumo, through = 'InsumoTareaPlantilla', blank = True)
    esMIPE = models.BooleanField(default=False, null=False)
    def __str__(self):
        return str(self.faseCultivo) + ', ' + str(self.orden) + ') ' + self.tareaPlantilla
    class Meta:
        ordering = ('orden','tareaPlantilla',)
        verbose_name_plural = 'Plantilla tareas - 07 Plantillas de tareas para el cultivo'
 
class InsumoTareaPlantilla(models.Model):
    tareaPlantilla = models.ForeignKey(TareaPlantilla, on_delete=models.PROTECT)
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    cantidadInsumo = models.IntegerField(null=False, default=0)
    def __str__(self):
        return str(self.tareaPlantilla) + ': ' + self.insumo.nombreInsumo + ' -> ' + str(self.cantidadInsumo)
    class Meta:
        verbose_name_plural = 'Plantilla tareas - 08 Asignación de Insumos a Tareas'

'''
FINCA
'''
class Finca(models.Model):
    nombreFinca = models.CharField(max_length=2048, blank=False, null=False)
    vereda = models.CharField(max_length=2048, blank=False, null=False)
    posicion = models.ForeignKey(Posicion, on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    def __str__(self):
        return self.nombreFinca
    class Meta:
        ordering = ('nombreFinca',)
        verbose_name_plural = 'Predio - Fincas'

'''
INSUMOS
'''
class TipoFormulacion(models.Model):
    codigo = models.CharField(max_length=4, blank=False, null=False)
    denominacion = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
        return '(' + self.codigo + ') ' + self.denominacion
    class Meta:
        ordering = ('denominacion',)
        verbose_name_plural = 'Inventario - 01 Tipos de formulación'

class CategoriaToxicologica(models.Model):
    codigo = models.CharField(max_length=4, blank=False, null=False)
    denominacion = models.CharField(max_length=512, blank=False, null=False)
    def __str__(self):
        return '(' + self.codigo + ') ' + self.denominacion
    class Meta:
        ordering = ('denominacion',)
        verbose_name_plural = 'Inventario - 02 Categorias toxicológicas'

class Agroquimico(Insumo):
    registroICA = models.IntegerField(null=False)
    fechaRegistro = models.DateField(null=False)
    empresa = models.CharField(max_length=2048, blank=False, null=False)
    tipoFormulacion = models.ForeignKey(TipoFormulacion, on_delete=models.PROTECT)
    categoriaToxico = models.ForeignKey(CategoriaToxicologica, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.tipoFormulacion) + str(self.categoriaToxico) + ' ' + self.nombreInsumo
    class Meta:
        ordering = ('registroICA',)
        verbose_name_plural = 'Inventario - 03 Agroquímicos'

class TipoFertilizante(models.Model):
    tipoFertilizante = models.CharField(max_length=64, blank=False, null=False)
    def __str__(self):
        return self.tipoFertilizante
    class Meta:
        ordering = ('tipoFertilizante',)
        verbose_name_plural = 'Inventario - 04 Tipos de fertilizante'

class UsoFertilizante(models.Model):
    usoFertilizante = models.CharField(max_length=64, blank=False, null=False)
    def __str__(self):
        return self.usoFertilizante
    class Meta:
        ordering = ('usoFertilizante',)
        verbose_name_plural = 'Inventario - 05 Usos de fertilizante'

class Fertilizante(Agroquimico):
    tipoFertilizante = models.ForeignKey(TipoFertilizante, on_delete=models.PROTECT)
    usoFertilizante = models.ForeignKey(UsoFertilizante, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.tipoFormulacion) + str(self.categoriaToxico) + ' ' + self.nombreInsumo + ' - ' + str(self.tipoFertilizante)
    class Meta:
        verbose_name_plural = 'Inventario - 06 Fertilizantes'

class Plaguicida(Agroquimico):
    modificaciones = models.CharField(max_length=2048, blank=False, null=False)
    ingredienteActivo = models.CharField(max_length=512, blank=False, null=False)
    concentracion = models.CharField(max_length=512, blank=False, null=False)
    paisesOrigen = models.CharField(max_length=2048, blank=False, null=False)
    cultivos = models.CharField(max_length=2048, blank=False, null=False)
    def __str__(self):
        return str(self.tipoFormulacion) + str(self.categoriaToxico) + ' ' + self.nombreInsumo + ' - ' + self.ingredienteActivo
    class Meta:
        verbose_name_plural = 'Inventario - 07 Plaguicidas'

class Herramienta(Insumo):
    fechaCompra = models.DateField(null=False)
    periodoManteminiento = models.ForeignKey(Periodicidad, on_delete=models.PROTECT)
    def __str__(self):
        return self.nombreInsumo
    class Meta:
        verbose_name_plural = 'Inventario - 08 Herramientas'

class Semilla(Insumo):
    nombreSemilla = models.CharField(max_length=512, blank=False, null=False)
    fechaCompra = models.DateField(null=False)
    proveedor = models.CharField(max_length=2048, blank=False, null=False)
    def __str__(self):
        return self.nombreInsumo
    class Meta:
        ordering = ('nombreSemilla',)
        verbose_name_plural = 'Inventario - 09 Semillas'

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
    class Meta:
        verbose_name_plural = 'Inventario - 10 Intentario'

'''
PERSONAL
'''
class Empleado(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT)
    fechaContrato = models.DateTimeField(null=False)
    def __str__(self):
        return str(self.finca) + ' ' + str(self.persona)
    class Meta:
        ordering = ('fechaContrato',)
        verbose_name_plural = 'RRHH - 01 Empleados'

'''
CULTIVO CONCRETO
'''
class Cultivo(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT)
    tipoCultivo = models.ForeignKey(TipoCultivo, on_delete=models.PROTECT)
    fechaInicio = models.DateField(null = False)
    def __str__(self):
        return str(self.finca) + ' ' + str(self.tipoCultivo)
    class Meta:
        ordering = ('finca','tipoCultivo','fechaInicio',)
        verbose_name_plural = 'Cultivo - 01 Cultivos'

class EstadoPlanta(models.Model):
    etiqueta = models.CharField(max_length=512, blank=False, null=False)
    icono = models.CharField(max_length=64, blank=False, null=False)
    nivel = models.IntegerField(null=False)
    def __str__(self):
        return str(self.nivel) + ')' + self.etiqueta
    class Meta:
        ordering = ('nivel',)
        verbose_name_plural = 'Cultivo - 02 Estados planta'

class Planta(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.PROTECT)
    generacion = models.IntegerField(null=False, default=1)
    linea = models.IntegerField(null=False, default=1)
    consecutivo = models.IntegerField(null=False, default=1)
    fechaSiembra = models.DateField(null = False)
    posicion = models.ForeignKey(Posicion, on_delete=models.PROTECT)
    estadosPlanta = models.ManyToManyField(EstadoPlanta, through='EstadoPlantaObservacion', blank=True)
    def __str__(self):
        return str(self.cultivo) + ')' + str(self.linea) + '/' + str(self.consecutivo)
    class Meta:
        ordering = ('cultivo','linea','consecutivo','fechaSiembra',)
        verbose_name_plural = 'Cultivo - 02 Plantas'

class EstadoPlantaObservacion(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT)
    estadoPlanta = models.ForeignKey(EstadoPlanta, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    observacion = models.CharField(max_length=64, blank=False, null=False)
    def __str__(self):
        return str(self.planta) + ' -> ' + str(self.estadoPlanta)
    class Meta:
        ordering = ('fecha',)
        verbose_name_plural = 'Cultivo - 03 Estados de la planta'

'''
TAREA CONCRETA
'''
class Tarea(models.Model):
    tareaPlantilla = models.ForeignKey(TareaPlantilla, on_delete=models.PROTECT)
    fechaInicial = models.DateField(null = False)
    fechaFinal = models.DateField(blank=True, null = True)
    observacion = models.CharField(max_length=1024, blank=True, null=True)
    responsables = models.ManyToManyField(Empleado, blank=False)
    plantas = models.ManyToManyField(Planta, blank=True)
    def __str__(self):
        return str(self.tareaPlantilla) + ' -> ' + str(self.fechaInicial)
    class Meta:
        ordering = ('fechaInicial',)
        verbose_name_plural = 'Cultivo - 04 Tareas'
