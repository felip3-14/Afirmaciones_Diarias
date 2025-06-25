from django.contrib import admin
from .models import Afirmacion, Comentario, Voto

# Register your models here.
@admin.register(Afirmacion)
class AfirmacionAdmin(admin.ModelAdmin):
    list_display = ('texto', 'fecha_creacion', 'activa')
    list_filter = ('activa', 'fecha_creacion')
    search_fields = ('texto',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'texto_corto', 'afirmacion', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'afirmacion__texto')
    search_fields = ('nombre_usuario', 'texto', 'afirmacion__texto')
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
    
    def texto_corto(self, obj):
        return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
    texto_corto.short_description = 'Comentario'

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'valor', 'afirmacion', 'fecha')
    list_filter = ('valor', 'fecha', 'afirmacion__texto')
    search_fields = ('nombre_usuario', 'afirmacion__texto')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)

# Personalizar el título del admin
admin.site.site_header = "Afirmaciones Diarias - Panel de Administración"
admin.site.site_title = "Admin Afirmaciones"
admin.site.index_title = "Gestión de Afirmaciones, Comentarios y Votos"
