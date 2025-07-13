#!/usr/bin/env python3
"""
Script de prueba para el servidor de sonidos
"""

import urllib.request
import urllib.error
import time

def test_server_sounds():
    """Prueba el servidor de sonidos"""
    
    # Cambiar por la IP real del servidor
    base_url = "http://192.168.0.20:8080"
    
    sound_files = ["beep.mp3", "go.mp3", "beep.wav", "go.wav"]
    
    print(f"🔊 === PRUEBA DEL SERVIDOR ===")
    print(f"📡 Servidor: {base_url}")
    print()
    
    for sound_file in sound_files:
        url = f"{base_url}/sounds/{sound_file}"
        print(f"🔍 Probando: {sound_file}")
        print(f"   URL: {url}")
        
        try:
            # Crear request para HEAD
            req = urllib.request.Request(url, method='HEAD')
            response = urllib.request.urlopen(req, timeout=5)
            
            print(f"   ✅ Status: {response.status}")
            print(f"   📊 Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"   📏 Content-Length: {response.headers.get('Content-Length', 'N/A')}")
            
            # Intentar descargar una pequeña parte
            try:
                req_get = urllib.request.Request(url)
                response_get = urllib.request.urlopen(req_get, timeout=5)
                chunk = response_get.read(1024)
                print(f"   📥 Primeros bytes: {len(chunk)} bytes")
                print(f"   🎵 Archivo accesible y descargable")
            except Exception as e:
                print(f"   ❌ Error al descargar: {e}")
                
        except urllib.error.URLError as e:
            if "Connection refused" in str(e):
                print(f"   ❌ Error de conexión - ¿Está el servidor ejecutándose?")
            elif "timed out" in str(e):
                print(f"   ❌ Timeout - Servidor no responde")
            else:
                print(f"   ❌ Error de URL: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    test_server_sounds()
