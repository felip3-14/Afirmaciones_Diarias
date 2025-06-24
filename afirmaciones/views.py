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
        # Detectar si es un envío de fallback
        is_fallback = request.POST.get('fallback_submit') == '1'
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        print(f"DEBUG - Tipo de envío: AJAX={is_ajax}, Fallback={is_fallback}")
        
        if 'comentario' in request.POST:
            nombre = request.POST.get('nombre_comentario', '').strip()
            texto = request.POST.get('comentario', '').strip()
            
            print(f"DEBUG - Recibido comentario: nombre='{nombre}', texto='{texto[:50]}...'")
            print(f"DEBUG - User Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')[:100]}")
            
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
                    try:
                        # Simular tiempo de procesamiento para el efecto
                        time.sleep(0.5)
                        nuevo_comentario = Comentario.objects.create(
                            nombre_usuario=nombre,
                            afirmacion_texto=afirmacion_texto,
                            texto=texto
                        )
                        print(f"DEBUG - Comentario creado exitosamente: ID={nuevo_comentario.id}")
                        mensaje = '¡Gracias por tu comentario!'
                        
                        # Si es fallback, redirigir directamente al dashboard
                        if is_fallback:
                            print("DEBUG - Redirigiendo por fallback...")
                            return redirect('.')
                            
                    except Exception as e:
                        print(f"ERROR - Al crear comentario: {e}")
                        mensaje = 'Error al guardar el comentario. Inténtalo de nuevo.'
                        # Si es AJAX, devolver error
                        if is_ajax:
                            return JsonResponse({'success': False, 'mensaje': mensaje})
                        # Si es fallback, mostrar error en la página
                        elif is_fallback:
                            return render(request, 'afirmaciones/index.html', {
                                'afirmacion': afirmacion_texto,
                                'comentarios': comentarios,
                                'votos': votos_dict,
                                'mensaje': mensaje,
                                'error': True
                            })
                else:
                    mensaje = 'Ya has enviado este comentario hoy.'
                    print(f"DEBUG - Comentario duplicado detectado para {nombre}")
                
                # Si es AJAX, devolver JSON
                if is_ajax:
                    return JsonResponse({'success': True, 'mensaje': mensaje})
                # Si es fallback, redirigir
                elif is_fallback:
                    return redirect('.')
                    
                return redirect('.')
            else:
                mensaje = 'Por favor, completa todos los campos.'
                print(f"DEBUG - Campos incompletos: nombre='{nombre}', texto='{texto}'")
                if is_ajax:
                    return JsonResponse({'success': False, 'mensaje': mensaje})
                elif is_fallback:
                    return render(request, 'afirmaciones/index.html', {
                        'afirmacion': afirmacion_texto,
                        'comentarios': comentarios,
                        'votos': votos_dict,
                        'mensaje': mensaje,
                        'error': True
                    })
        if 'voto' in request.POST:
            nombre = request.POST.get('nombre_voto', '').strip()
            valor = request.POST.get('voto')
            
            print(f"DEBUG - Recibido voto: nombre='{nombre}', valor='{valor}'")
            
            if nombre and valor in ['positivo', 'neutral', 'negativo']:
                # Verificar si el usuario ya votó hoy
                hoy = timezone.now().date()
                voto_existente = Voto.objects.filter(
                    nombre_usuario=nombre,
                    afirmacion_texto=afirmacion_texto,
                    fecha=hoy
                ).exists()
                
                if not voto_existente:
                    try:
                        # Simular tiempo de procesamiento
                        time.sleep(0.3)
                        nuevo_voto = Voto.objects.create(
                            nombre_usuario=nombre,
                            afirmacion_texto=afirmacion_texto,
                            valor=valor
                        )
                        print(f"DEBUG - Voto creado exitosamente: ID={nuevo_voto.id}")
                        mensaje = '¡Gracias por tu voto!'
                        
                        # Si es fallback, continuar al siguiente paso
                        if is_fallback:
                            print("DEBUG - Voto por fallback, continuando...")
                            
                    except Exception as e:
                        print(f"ERROR - Al crear voto: {e}")
                        mensaje = 'Error al guardar el voto. Inténtalo de nuevo.'
                        if is_ajax:
                            return JsonResponse({'success': False, 'mensaje': mensaje})
                        elif is_fallback:
                            return render(request, 'afirmaciones/index.html', {
                                'afirmacion': afirmacion_texto,
                                'comentarios': comentarios,
                                'votos': votos_dict,
                                'mensaje': mensaje,
                                'error': True
                            })
                else:
                    mensaje = 'Ya has votado hoy.'
                    print(f"DEBUG - Voto duplicado detectado para {nombre}")
                
                # Si es AJAX, devolver JSON
                if is_ajax:
                    return JsonResponse({'success': True, 'mensaje': mensaje})
                elif is_fallback:
                    return redirect('.')
                return redirect('.')
            else:
                mensaje = 'Datos de voto inválidos.'
                print(f"DEBUG - Voto inválido: nombre='{nombre}', valor='{valor}'")
                if is_ajax:
                    return JsonResponse({'success': False, 'mensaje': mensaje})
                elif is_fallback:
                    return render(request, 'afirmaciones/index.html', {
                        'afirmacion': afirmacion_texto,
                        'comentarios': comentarios,
                        'votos': votos_dict,
                        'mensaje': mensaje,
                        'error': True
                    })

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

@staff_member_required
def debug_comentarios(request):
    """Vista de debug para ver comentarios recientes"""
    comentarios = Comentario.objects.all().order_by('-fecha_creacion')[:20]
    votos = Voto.objects.all().order_by('-fecha')[:20]
    
    debug_info = {
        'total_comentarios': Comentario.objects.count(),
        'total_votos': Voto.objects.count(),
        'comentarios_recientes': comentarios,
        'votos_recientes': votos,
    }
    
    return JsonResponse({
        'total_comentarios': debug_info['total_comentarios'],
        'total_votos': debug_info['total_votos'],
        'comentarios': [
            {
                'id': c.id,
                'nombre': c.nombre_usuario,
                'texto': c.texto,
                'fecha': c.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                'afirmacion': c.afirmacion_texto[:50] + '...'
            }
            for c in debug_info['comentarios_recientes']
        ],
        'votos': [
            {
                'id': v.id,
                'nombre': v.nombre_usuario,
                'valor': v.valor,
                'fecha': v.fecha.strftime('%Y-%m-%d'),
                'afirmacion': v.afirmacion_texto[:50] + '...'
            }
            for v in debug_info['votos_recientes']
        ]
    }, indent=2)

def test_comentarios(request):
    """Vista simple para probar comentarios"""
    afirmacion_texto = get_daily_affirmation()
    
    # Obtener comentarios para esta afirmación
    comentarios = Comentario.objects.filter(afirmacion_texto=afirmacion_texto).order_by('-fecha_creacion') if afirmacion_texto else []
    mensaje = None

    if request.method == 'POST' and afirmacion_texto:
        if 'comentario' in request.POST:
            nombre = request.POST.get('nombre_comentario', '').strip()
            texto = request.POST.get('comentario', '').strip()
            
            print(f"TEST - Recibido comentario: nombre='{nombre}', texto='{texto[:50]}...'")
            
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
                    try:
                        nuevo_comentario = Comentario.objects.create(
                            nombre_usuario=nombre,
                            afirmacion_texto=afirmacion_texto,
                            texto=texto
                        )
                        print(f"TEST - Comentario creado exitosamente: ID={nuevo_comentario.id}")
                        mensaje = '¡Comentario guardado exitosamente!'
                    except Exception as e:
                        print(f"TEST ERROR - Al crear comentario: {e}")
                        mensaje = f'Error al guardar el comentario: {e}'
                        # Si es AJAX, devolver error
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({'success': False, 'mensaje': mensaje})
                else:
                    mensaje = 'Ya has enviado este comentario hoy.'
                    print(f"TEST - Comentario duplicado detectado para {nombre}")
                
                # Si es AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'mensaje': mensaje})
                return redirect('test_comentarios')
            else:
                mensaje = 'Por favor, completa todos los campos.'
                print(f"TEST - Campos incompletos: nombre='{nombre}', texto='{texto}'")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'mensaje': mensaje})

    return render(request, 'afirmaciones/test.html', {
        'afirmacion': afirmacion_texto,
        'comentarios': comentarios,
        'mensaje': mensaje,
    })
