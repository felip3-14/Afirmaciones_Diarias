from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Comentario, Voto, Afirmacion
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import os
import time
import random
import logging
from datetime import date

logger = logging.getLogger(__name__)

# Cargar afirmaciones desde JSON
def load_affirmations_from_json():
    json_path = os.path.join('data', 'affirmations.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            affirmations = data.get('affirmations', [])
            return affirmations
    return []

def get_daily_affirmation():
    """
    Selecciona una afirmación para el día de forma determinista pero pseudo-aleatoria,
    evitando las utilizadas en los últimos 4 días.
    """
    hoy = timezone.now().date()

    # 1. ¿Ya se eligió una afirmación hoy? (verificando si hay votos)
    voto_de_hoy = Voto.objects.filter(fecha=hoy).first()
    if voto_de_hoy:
        return voto_de_hoy.afirmacion

    # 2. Si no, seleccionar una nueva
    # Obtener las IDs de las afirmaciones usadas en los últimos 4 días
    fechas_recientes = [hoy - timezone.timedelta(days=i) for i in range(1, 5)]
    votos_recientes = Voto.objects.filter(fecha__in=fechas_recientes)
    ids_usadas = list(votos_recientes.values_list('afirmacion_id', flat=True))
    
    # Obtener todas las afirmaciones candidatas (activas y no usadas recientemente)
    candidatas = Afirmacion.objects.filter(activa=True).exclude(id__in=ids_usadas)

    if not candidatas.exists():
        # Si no quedan candidatas (todas se usaron), usar cualquiera
        candidatas = Afirmacion.objects.filter(activa=True)
        if not candidatas.exists():
            return None # No hay afirmaciones activas en la BD

    # 3. Selección determinista usando el día del año
    dia_del_ano = hoy.timetuple().tm_yday
    indice_seleccionado = dia_del_ano % candidatas.count()
    afirmacion_del_dia = candidatas[indice_seleccionado]
    
    return afirmacion_del_dia

@ensure_csrf_cookie
def index(request):
    """
    Vista principal que maneja la lógica de la app.
    """
    afirmacion_del_dia = get_daily_affirmation()
    comentarios = []

    if afirmacion_del_dia:
        comentarios = Comentario.objects.filter(afirmacion=afirmacion_del_dia).order_by('-fecha_creacion')

    if request.method == 'POST':
        if not afirmacion_del_dia:
            return JsonResponse({'success': False, 'mensaje': 'No hay afirmación para hoy.'}, status=400)

        nombre = request.POST.get('nombre_comentario', '').strip()
        texto = request.POST.get('comentario', '').strip()
        
        if not nombre or not texto:
            return JsonResponse({'success': False, 'mensaje': 'Nombre y comentario son requeridos.'}, status=400)

        try:
            # Crear el voto para "bloquear" la afirmación del día
            Voto.objects.get_or_create(
                afirmacion=afirmacion_del_dia,
                nombre_usuario=nombre,
                fecha=timezone.now().date(),
                defaults={'valor': 'positivo'} # Se asume un voto al comentar
            )

            # Crear el comentario
            Comentario.objects.create(
                afirmacion=afirmacion_del_dia,
                nombre_usuario=nombre,
                texto=texto
            )
            logger.info(f"Comentario guardado de '{nombre}' para la afirmación ID {afirmacion_del_dia.id}")
            return JsonResponse({'success': True, 'mensaje': '¡Gracias por tu comentario!'})

        except Exception as e:
            logger.error(f"Error al guardar comentario: {e}")
            return JsonResponse({'success': False, 'mensaje': 'Error interno al guardar.'}, status=500)

    context = {
        'afirmacion': afirmacion_del_dia.texto if afirmacion_del_dia else "Vuelve mañana para una nueva afirmación.",
        'comentarios': comentarios,
    }
    return render(request, 'afirmaciones/index.html', context)

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

@ensure_csrf_cookie
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

def csrf_failure(request, reason=""):
    """Vista personalizada para errores CSRF con debugging"""
    print(f"🚨 CSRF FAILURE: {reason}")
    print(f"🚨 Request path: {request.path}")
    print(f"🚨 Request method: {request.method}")
    print(f"🚨 User agent: {request.META.get('HTTP_USER_AGENT', 'N/A')}")
    print(f"🚨 Cookies: {list(request.COOKIES.keys())}")
    print(f"🚨 CSRF cookie: {request.COOKIES.get('csrftoken', 'NOT_FOUND')}")
    print(f"🚨 POST data: {list(request.POST.keys())}")
    print(f"🚨 Headers: {dict(request.headers)}")
    
    # Si es AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'csrf_failed',
            'mensaje': f'Error CSRF: {reason}. Recargando página...',
            'debug_info': {
                'reason': str(reason),
                'path': request.path,
                'cookies': list(request.COOKIES.keys()),
                'csrf_cookie_present': 'csrftoken' in request.COOKIES,
                'post_token_present': 'csrfmiddlewaretoken' in request.POST
            },
            'action': 'reload'
        }, status=403)
    
    # Para formularios normales, redirigir con mensaje
    from django.contrib import messages
    messages.error(request, f'Error de seguridad: {reason}. Por favor, inténtalo de nuevo.')
    return redirect(request.path)

@ensure_csrf_cookie
def simple_test(request):
    """Vista súper simple para probar CSRF sin complicaciones"""
    afirmacion_texto = get_daily_affirmation()
    comentarios = Comentario.objects.filter(afirmacion_texto=afirmacion_texto).order_by('-fecha_creacion') if afirmacion_texto else []
    mensaje = None

    if request.method == 'POST' and afirmacion_texto:
        print(f"🔥 SIMPLE TEST - POST recibido")
        print(f"🔥 POST data: {dict(request.POST)}")
        print(f"🔥 Cookies: {dict(request.COOKIES)}")
        
        if 'comentario' in request.POST:
            nombre = request.POST.get('nombre_comentario', '').strip()
            texto = request.POST.get('comentario', '').strip()
            
            print(f"🔥 Procesando comentario: {nombre} - {texto[:50]}...")
            
            if nombre and texto:
                try:
                    nuevo_comentario = Comentario.objects.create(
                        nombre_usuario=nombre,
                        afirmacion_texto=afirmacion_texto,
                        texto=texto
                    )
                    print(f"🔥 ¡Comentario creado exitosamente! ID: {nuevo_comentario.id}")
                    mensaje = f'¡Comentario guardado exitosamente! ID: {nuevo_comentario.id}'
                    # Recargar comentarios
                    comentarios = Comentario.objects.filter(afirmacion_texto=afirmacion_texto).order_by('-fecha_creacion')
                except Exception as e:
                    print(f"🔥 ERROR creando comentario: {e}")
                    mensaje = f'Error al guardar: {e}'
            else:
                mensaje = 'Por favor, completa todos los campos.'

    return render(request, 'afirmaciones/simple_test.html', {
        'afirmacion': afirmacion_texto,
        'comentarios': comentarios,
        'mensaje': mensaje,
    })
