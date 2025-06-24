from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Comentario, Voto
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
import json
import os
import time

# Cargar afirmaciones desde JSON
def load_affirmations_from_json():
    json_path = os.path.join('data', 'affirmations.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            affirmations = data.get('affirmations', [])
            return affirmations
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
        afirmacion_elegida = votos_hoy.first().afirmacion_texto
        return afirmacion_elegida
    
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
                # Verificar si no existe ya un comentario idéntico del mismo usuario hoy
                hoy = timezone.now().date()
                comentario_existente = Comentario.objects.filter(
                    nombre_usuario=nombre,
                    afirmacion_texto=afirmacion_texto,
                    texto=texto,
                    fecha_creacion__date=hoy
                ).exists()
                
                if not comentario_existente:
                    # Simular tiempo de procesamiento para el efecto
                    time.sleep(0.5)
                    Comentario.objects.create(
                        nombre_usuario=nombre,
                        afirmacion_texto=afirmacion_texto,
                        texto=texto
                    )
                    mensaje = '¡Gracias por tu comentario!'
                else:
                    mensaje = 'Ya has enviado este comentario hoy.'
                
                # Si es AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'mensaje': mensaje})
                return redirect('.')
                
        if 'voto' in request.POST:
            nombre = request.POST.get('nombre_voto', '').strip()
            valor = request.POST.get('voto')
            if nombre and valor in ['positivo', 'neutral', 'negativo']:
                # Verificar si el usuario ya votó hoy
                hoy = timezone.now().date()
                voto_existente = Voto.objects.filter(
                    nombre_usuario=nombre,
                    afirmacion_texto=afirmacion_texto,
                    fecha=hoy
                ).exists()
                
                if not voto_existente:
                    # Simular tiempo de procesamiento
                    time.sleep(0.3)
                    Voto.objects.create(
                        nombre_usuario=nombre,
                        afirmacion_texto=afirmacion_texto,
                        valor=valor
                    )
                    mensaje = '¡Gracias por tu voto!'
                else:
                    mensaje = 'Ya has votado hoy.'
                
                # Si es AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'mensaje': mensaje})
                return redirect('.')

    return render(request, 'afirmaciones/index.html', {
        'afirmacion': afirmacion_texto,
        'comentarios': comentarios,
        'votos': votos_dict,
        'mensaje': mensaje,
    })

@staff_member_required
def estadisticas(request):
    """Vista para ver estadísticas y comentarios (solo para staff)"""
    
    # Estadísticas generales
    total_comentarios = Comentario.objects.count()
    total_votos = Voto.objects.count()
    usuarios_unicos = Comentario.objects.values('nombre_usuario').distinct().count()
    
    # Comentarios recientes (últimos 50)
    comentarios_recientes = Comentario.objects.order_by('-fecha_creacion')[:50]
    
    # Votos por tipo
    votos_stats = Voto.objects.values('valor').annotate(count=Count('id'))
    votos_dict = {v['valor']: v['count'] for v in votos_stats}
    
    # Usuarios más activos (comentarios)
    usuarios_activos = (Comentario.objects
                       .values('nombre_usuario')
                       .annotate(total=Count('id'))
                       .order_by('-total')[:10])
    
    # Afirmaciones más comentadas
    afirmaciones_populares = (Comentario.objects
                             .values('afirmacion_texto')
                             .annotate(total=Count('id'))
                             .order_by('-total')[:10])
    
    context = {
        'total_comentarios': total_comentarios,
        'total_votos': total_votos,
        'usuarios_unicos': usuarios_unicos,
        'comentarios_recientes': comentarios_recientes,
        'votos_stats': votos_dict,
        'usuarios_activos': usuarios_activos,
        'afirmaciones_populares': afirmaciones_populares,
    }
    
    return render(request, 'afirmaciones/estadisticas.html', context)
