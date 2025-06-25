import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afirmaciones_web.settings')
django.setup()

from afirmaciones.models import Afirmacion

def populate_affirmations():
    # Eliminar afirmaciones existentes para evitar duplicados al correr el script
    print("Eliminando afirmaciones antiguas...")
    Afirmacion.objects.all().delete()
    print("Afirmaciones antiguas eliminadas.")

    # Cargar desde el archivo JSON
    json_path = os.path.join('data', 'affirmations.json')
    if not os.path.exists(json_path):
        print(f"Error: No se encontró el archivo en {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        affirmations_list = data.get('affirmations', [])

    # Poblar la base de datos
    print(f"Poblando la base de datos con {len(affirmations_list)} afirmaciones...")
    for texto_afirmacion in affirmations_list:
        try:
            Afirmacion.objects.create(texto=texto_afirmacion)
        except django.db.utils.IntegrityError:
            print(f"  -> La afirmación '{texto_afirmacion[:50]}...' ya existe. Omitiendo.")

    print("\n¡Listo! La base de datos ha sido poblada con las afirmaciones.")

if __name__ == "__main__":
    populate_affirmations() 