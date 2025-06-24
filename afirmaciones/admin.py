from django.contrib import admin
from .models import Afirmacion, Comentario, Voto

# Register your models here.
admin.site.register(Afirmacion)
admin.site.register(Comentario)
admin.site.register(Voto)
