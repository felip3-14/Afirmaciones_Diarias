from django.middleware.csrf import CsrfViewMiddleware
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

class CustomCSRFMiddleware(CsrfViewMiddleware):
    """
    Middleware personalizado para manejo de CSRF con mejor debugging
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Log información útil para debugging
        if request.method == 'POST':
            logger.info(f"POST request to {request.path}")
            logger.info(f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')}")
            logger.info(f"Referer: {request.META.get('HTTP_REFERER', 'N/A')}")
            logger.info(f"CSRF Token in POST: {'csrfmiddlewaretoken' in request.POST}")
            logger.info(f"CSRF Token in META: {'CSRF_COOKIE' in request.META}")
            logger.info(f"CSRF Cookie value: {request.COOKIES.get('csrftoken', 'NO COOKIE')}")
            logger.info(f"X-CSRFToken header: {request.META.get('HTTP_X_CSRFTOKEN', 'NO HEADER')}")
            
            # Debug detallado de cookies
            logger.info(f"All cookies: {list(request.COOKIES.keys())}")
            
        return super().process_view(request, view_func, view_args, view_kwargs)
    
    def _reject(self, request, reason):
        """
        Manejo personalizado de rechazo CSRF
        """
        logger.warning(f"CSRF rejection: {reason}")
        logger.warning(f"Path: {request.path}")
        logger.warning(f"Method: {request.method}")
        logger.warning(f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')}")
        logger.warning(f"Available cookies: {list(request.COOKIES.keys())}")
        logger.warning(f"CSRF cookie value: {request.COOKIES.get('csrftoken', 'NOT FOUND')}")
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'csrf_failed',
                'mensaje': 'Error de seguridad. Por favor, recarga la página e inténtalo de nuevo.',
                'debug_info': {
                    'reason': str(reason),
                    'path': request.path,
                    'user_agent': request.META.get('HTTP_USER_AGENT', 'N/A')[:100],
                    'cookies_available': list(request.COOKIES.keys()),
                    'csrf_cookie': request.COOKIES.get('csrftoken', 'NOT_FOUND')[:20] + '...' if request.COOKIES.get('csrftoken') else 'NOT_FOUND'
                }
            }, status=403)
        
        # Para peticiones normales, usar el comportamiento por defecto
        return super()._reject(request, reason) 