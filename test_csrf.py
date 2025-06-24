#!/usr/bin/env python3
"""
Script para probar el sistema CSRF con manejo de cookies como un navegador real
"""
import requests
from bs4 import BeautifulSoup
import time

def test_csrf_flow():
    print("🧪 Probando flujo completo de CSRF...")
    print("=" * 50)
    
    # Crear sesión para mantener cookies
    session = requests.Session()
    
    # Configurar headers como navegador
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    base_url = "http://127.0.0.1:8002"
    
    try:
        # Paso 1: Obtener la página inicial
        print("📄 Paso 1: Obteniendo página inicial...")
        response = session.get(f"{base_url}/test/")
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error: {response.status_code}")
            return False
        
        # Paso 2: Extraer token CSRF
        print("🔑 Paso 2: Extrayendo token CSRF...")
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if csrf_token:
            token_value = csrf_token.get('value')
            print(f"   ✅ Token encontrado: {token_value[:20]}...")
        else:
            print("   ❌ No se encontró token CSRF")
            return False
        
        # Paso 3: Mostrar cookies
        print("🍪 Paso 3: Verificando cookies...")
        cookies = session.cookies.get_dict()
        print(f"   Cookies recibidas: {list(cookies.keys())}")
        
        # Paso 4: Enviar comentario
        print("💬 Paso 4: Enviando comentario...")
        
        # Preparar datos del formulario
        form_data = {
            'csrfmiddlewaretoken': token_value,
            'nombre_comentario': 'TestUser_Script',
            'comentario': 'Este es un comentario de prueba desde el script de testing CSRF'
        }
        
        # Enviar como AJAX
        ajax_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': token_value,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f"{base_url}/test/"
        }
        
        # También enviar el token en el header alternativo
        if 'csrftoken' in cookies:
            ajax_headers['X-CSRFToken'] = cookies['csrftoken']
            print(f"   🔑 Usando cookie CSRF: {cookies['csrftoken'][:20]}...")
        
        response = session.post(
            f"{base_url}/test/",
            data=form_data,
            headers=ajax_headers
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ Respuesta JSON: {result}")
                return result.get('success', False)
            except:
                print(f"   ⚠️  Respuesta no es JSON: {response.text[:100]}...")
                return False
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def test_fallback_flow():
    print("\n🔄 Probando flujo de fallback...")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Android 10; Mobile; rv:81.0) Gecko/81.0 Firefox/81.0'
    })
    
    base_url = "http://127.0.0.1:8002"
    
    try:
        # Obtener página
        response = session.get(f"{base_url}/test/")
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        
        # Enviar como formulario tradicional
        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'nombre_comentario': 'TestUser_Fallback',
            'comentario': 'Comentario de prueba usando método de fallback',
            'fallback_submit': '1'
        }
        
        response = session.post(f"{base_url}/test/", data=form_data)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print("   ✅ Redirección exitosa (formulario tradicional funcionando)")
            return True
        elif response.status_code == 200:
            print("   ✅ Respuesta exitosa")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante prueba de fallback: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de CSRF...")
    print("⏰ Esperando 2 segundos para que el servidor esté listo...")
    time.sleep(2)
    
    # Probar flujo AJAX
    ajax_success = test_csrf_flow()
    
    # Probar flujo de fallback
    fallback_success = test_fallback_flow()
    
    print("\n📊 RESULTADOS:")
    print("=" * 50)
    print(f"AJAX Flow: {'✅ ÉXITO' if ajax_success else '❌ FALLÓ'}")
    print(f"Fallback Flow: {'✅ ÉXITO' if fallback_success else '❌ FALLÓ'}")
    
    if ajax_success and fallback_success:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema CSRF está funcionando correctamente.")
    elif ajax_success or fallback_success:
        print("\n⚠️  Algunas pruebas pasaron. El sistema tiene funcionalidad parcial.")
    else:
        print("\n💥 Todas las pruebas fallaron. Revisar configuración CSRF.") 