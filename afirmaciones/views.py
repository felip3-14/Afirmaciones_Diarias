from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Comentario, Voto
from django.db.models import Count
import json
import os

# Cargar afirmaciones desde JSON
def load_affirmations_from_json():
    json_path = os.path.join('data', 'affirmations.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('affirmations', [])
    return []

# Utilidad: obtener la afirmación del día (secuencial, sin repetir las últimas 4)
def get_daily_affirmation():
    affirmations = load_affirmations_from_json()
    if not affirmations:
        return None
    
    hoy = timezone.now().date()
    
    # Buscar si ya hay votos para hoy (significa que ya se eligió afirmación)
    votos_hoy = Voto.objects.filter(fecha=hoy)
    if votos_hoy.exists():
        return votos_hoy.first().afirmacion_texto
    
    # Si no hay votos hoy, elegir nueva afirmación evitando las últimas 4
    ultimas_afirmaciones = list(Voto.objects.order_by('-fecha').values_list('afirmacion_texto', flat=True)[:4])
    
    for afirmacion in affirmations:
        if afirmacion not in ultimas_afirmaciones:
            return afirmacion
    
    # Si todas han sido usadas recientemente, usar la primera
    return affirmations[0]

def index(request):
    afirmacion_texto = get_daily_affirmation()
    
    # Obtener comentarios y votos para esta afirmación
    comentarios = Comentario.objects.filter(afirmacion_texto=afirmacion_texto).order_by('-fecha_creacion') if afirmacion_texto else []
    votos = Voto.objects.filter(afirmacion_texto=afirmacion_texto) if afirmacion_texto else Voto.objects.none()
    
    # Contar votos
    votos_count = votos.values('valor').annotate(c=Count('id'))
    votos_dict = {v['valor']: v['c'] for v in votos_count}
    mensaje = None

    if request.method == 'POST' and afirmacion_texto:
        if 'comentario' in request.POST:
            nombre = request.POST.get('nombre_comentario', '').strip()
            texto = request.POST.get('comentario', '').strip()
            if nombre and texto:
                Comentario.objects.create(
                    nombre_usuario=nombre,
                    afirmacion_texto=afirmacion_texto,
                    texto=texto
                )
                mensaje = '¡Gracias por tu comentario!'
                return redirect('.')
                
        if 'voto' in request.POST:
            nombre = request.POST.get('nombre_voto', '').strip()
            valor = request.POST.get('voto')
            if nombre and valor in ['positivo', 'neutral', 'negativo']:
                Voto.objects.create(
                    nombre_usuario=nombre,
                    afirmacion_texto=afirmacion_texto,
                    valor=valor
                )
                mensaje = '¡Gracias por tu voto!'
                return redirect('.')

    return render(request, 'afirmaciones/index.html', {
        'afirmacion': afirmacion_texto,
        'comentarios': comentarios,
        'votos': votos_dict,
        'mensaje': mensaje,
    })
