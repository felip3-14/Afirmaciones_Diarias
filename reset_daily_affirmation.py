import os
import django
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afirmaciones_web.settings')
django.setup()

from afirmaciones.models import Voto

def reset_affirmation():
    """
    Busca y elimina los votos registrados en la fecha actual para forzar
    una nueva selección de afirmación en la próxima carga de la página.
    """
    # Usar la zona horaria configurada en Django ('America/Argentina/Buenos_Aires')
    hoy = timezone.now().date()
    
    print(f"Buscando votos para la fecha: {hoy}...")
    
    votos_de_hoy = Voto.objects.filter(fecha=hoy)
    count = votos_de_hoy.count()
    
    if count > 0:
        print(f"Se encontraron {count} votos. La afirmación de hoy está bloqueada.")
        print("Procediendo a borrarlos para permitir una nueva selección...")
        
        # Guardar el texto de la afirmación para mostrarlo
        afirmacion_actual = votos_de_hoy.first().afirmacion_texto
        print(f"   -> Afirmación actual: '{afirmacion_actual}'")
        
        votos_de_hoy.delete()
        
        print("\n¡Listo! Los votos de hoy han sido eliminados.")
        print("La próxima vez que alguien visite la página, se seleccionará una nueva afirmación.")
    else:
        print("No hay votos registrados para hoy. La afirmación se seleccionará en la próxima visita.")
        print("No se necesita hacer nada.")

if __name__ == "__main__":
    reset_affirmation() 