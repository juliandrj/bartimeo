from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from .models import *

admin.site.site_header = 'Sistema de Gestión Agrícola'
admin.site.index_title = 'Administración general'

@admin.register(Persona)
class PersonaModelAdmin(admin.ModelAdmin):
    list_display = ('get_user_name','get_user_firstname','get_user_lastname')

    @admin.display(description='Usuario')
    def get_user_name(self, obj):
        return obj.usuario.username
    
    @admin.display(description='Nombre')
    def get_user_firstname(self, obj):
        return obj.usuario.first_name
    
    @admin.display(description='Apellido')
    def get_user_lastname(self, obj):
        return obj.usuario.last_name

@admin.register(Departamento)
class DepartamentoModelAdmin(admin.ModelAdmin):
    list_display = ('get_pais', 'departamento')
    list_display_links = ('departamento',)

    @admin.display(description='País')
    def get_pais(self, obj):
        return obj.pais.pais

@admin.register(Municipio)
class MunicipioModelAdmin(admin.ModelAdmin):
    list_display = ('get_pais', 'get_departamento', 'municipio')
    list_display_links = ('municipio',)
    list_filter = ('departamento',)

    @admin.display(description='País')
    def get_pais(self, obj):
        return obj.departamento.pais.pais

    @admin.display(description='Departamento')
    def get_departamento(self, obj):
        return obj.departamento.departamento

@admin.register(Insumo)
class InsumoModelAdmin(admin.ModelAdmin):
    list_display = ('nombreInsumo', 'get_tipo_insumo', 'get_unidad_medida')
    list_display_links = ('nombreInsumo',)
    list_filter = ('tipoInsumo',)
    search_fields = ('nombreInsumo',)

    @admin.display(description='Tipo Insumo')
    def get_tipo_insumo(self, obj):
        return obj.tipoInsumo.tipoInsumo

    @admin.display(description='Unidad')
    def get_unidad_medida(self, obj):
        return obj.unidadMedida.abreviatura

class InsumoTareaPlantillaTabularInline(admin.TabularInline):
    model = InsumoTareaPlantilla
    extra = 0

@admin.register(TareaPlantilla)
class TareaPlantillaModelAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_cultivo', 'get_fase', 'orden', 'tareaPlantilla', 'esMIPE',)
    list_display_links = ('tareaPlantilla',)
    list_filter = ('faseCultivo',)
    inlines = [InsumoTareaPlantillaTabularInline,]

    @admin.display(description='Tipo de Cultivo')
    def get_tipo_cultivo(self, obj):
        return obj.faseCultivo.tipoCultivo.tipoCultivo

    @admin.display(description='Fase')
    def get_fase(self, obj):
        return obj.faseCultivo.faseCultivo

@admin.register(FaseCultivo)
class FaseCultivoModelAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_cultivo', 'orden', 'faseCultivo')
    list_display_links = ('faseCultivo',)

    @admin.display(description='Tipo cultivo')
    def get_tipo_cultivo(self, obj):
        return obj.tipoCultivo.tipoCultivo

@admin.register(Hito)
class HitoModelAdmin(admin.ModelAdmin):
    list_display = ('hito', 'duracionEstimada', 'get_unidad_tiempo')

    @admin.display(description='Unidad de tiempo')
    def get_unidad_tiempo(self, obj):
        return obj.unidadTiempo.unidadTiempo

@admin.register(Cultivo)
class CultivoModelAdmin(admin.ModelAdmin):
    list_display = ('get_finca', 'get_tipo_cultivo', 'fechaInicio')

    @admin.display(description='Finca')
    def get_finca(self, obj):
        return obj.finca.nombreFinca
    
    @admin.display(description='Tipo de cultivo')
    def get_tipo_cultivo(self, obj):
        return obj.tipoCultivo.tipoCultivo

class EstadoPlantaObservacionTabularInline(admin.TabularInline):
    model = EstadoPlantaObservacion
    readonly_fields = ('fecha',)
    extra = 0

@admin.register(Planta)
class PlantaModelAdmin(admin.ModelAdmin):
    list_display = ('get_cultivo', 'fechaSiembra', 'generacion', 'linea', 'consecutivo')
    list_display_links = ('fechaSiembra', 'generacion', 'linea', 'consecutivo',)
    list_filter = ('cultivo','linea','consecutivo',)
    inlines = [EstadoPlantaObservacionTabularInline,]

    @admin.display(description='Cultivo')
    def get_cultivo(self, obj):
        return str(obj.cultivo)

@admin.register(Tarea)
class TareaModelAdmin(admin.ModelAdmin):
    list_display = ('get_tarea', 'fechaInicial', 'fechaFinal', 'observacion')
    list_filter = ('tareaPlantilla', 'fechaInicial', 'fechaFinal',)

    @admin.display(description='Tarea')
    def get_tarea(self, obj):
        return str(obj.tareaPlantilla)

@admin.register(Empleado)
class EmpleadoModelAdmin(admin.ModelAdmin):
    list_display = ('get_finca', 'get_nombres', 'fechaContrato',)
    list_display_links = ('get_nombres', 'fechaContrato',)
    list_filter = ('finca',)

    @admin.display(description='Finca')
    def get_finca(self, obj):
        return str(obj.finca)
    
    @admin.display(description='Nombres')
    def get_nombres(self, obj):
        return str(obj.persona)

class CriterioFincaTabularInline(admin.TabularInline):
    model = CriterioFinca
    fields = ('criterio','fechaRegistro','fechaCaduca','ficheroSoporte','linkSoporte','aprobado',)
    readonly_fields = ('criterio',)
    extra = 0

@admin.register(Finca)
class FincaModelAdmin(admin.ModelAdmin):
    list_display = ('nombreFinca', 'vereda', 'get_municipio',)
    list_display_links = ('nombreFinca',)
    list_filter = ('municipio',)
    inlines = [CriterioFincaTabularInline,]

    @admin.display(description='Municipio')
    def get_municipio(self, obj):
        return str(obj.municipio)

@admin.register(Criterio)
class CriterioModelAdmin(admin.ModelAdmin):
    list_display = ('numero', 'textoCriterio', 'get_nivel_criterio',)
    list_display_links = ('numero', 'textoCriterio',)
    list_filter = ('numero',)
    inlines = [CriterioFincaTabularInline,]

    @admin.display(description='Nivel')
    def get_nivel_criterio(self, obj):
        return str(obj.nivelCriterio)

admin.site.register(OpcionMenu)
admin.site.register(UnidadMedida)
admin.site.register(UnidadTiempo)
admin.site.register(Distribucion)
admin.site.register(TipoInsumo)
admin.site.register(Periodicidad)
admin.site.register(TipoCultivo)
admin.site.register(Posicion)
admin.site.register(Pais)
admin.site.register(TipoFormulacion)
admin.site.register(CategoriaToxicologica)
admin.site.register(Agroquimico)
admin.site.register(TipoFertilizante)
admin.site.register(UsoFertilizante)
admin.site.register(Fertilizante)
admin.site.register(Plaguicida)
admin.site.register(Herramienta)
admin.site.register(Semilla)
admin.site.register(Inventario)
admin.site.register(EstadoPlanta)
admin.site.register(NivelCriterio)

admin.site.unregister(TokenProxy)
