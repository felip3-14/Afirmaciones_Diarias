from django.contrib import admin
from .models import Afirmacion, Comentario, Voto

# Register your models here.
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'texto_corto', 'afirmacion_corta', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'afirmacion_texto')
    search_fields = ('nombre_usuario', 'texto', 'afirmacion_texto')
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
    
    def texto_corto(self, obj):
        return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
    texto_corto.short_description = 'Comentario'
    
    def afirmacion_corta(self, obj):
        return obj.afirmacion_texto[:40] + "..." if len(obj.afirmacion_texto) > 40 else obj.afirmacion_texto
    afirmacion_corta.short_description = 'Afirmación'

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'valor', 'afirmacion_corta', 'fecha')
    list_filter = ('valor', 'fecha', 'afirmacion_texto')
    search_fields = ('nombre_usuario', 'afirmacion_texto')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)
    
    def afirmacion_corta(self, obj):
        return obj.afirmacion_texto[:40] + "..." if len(obj.afirmacion_texto) > 40 else obj.afirmacion_texto
    afirmacion_corta.short_description = 'Afirmación'

# Personalizar el título del admin
admin.site.site_header = "Afirmaciones Diarias - Panel de Administración"
admin.site.site_title = "Admin Afirmaciones"
admin.site.index_title = "Gestión de Comentarios y Votos"
