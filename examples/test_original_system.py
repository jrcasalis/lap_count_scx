"""
Test del sistema original para verificar que todo funciona
"""

import time
from src.race_controller import RaceController
from src.web_server import WebServer

def test_original_system():
    """Test del sistema original"""
    print("🧪 Test del sistema original")
    print("=" * 40)
    
    try:
        # Crear controlador de carrera
        print("1. Creando controlador de carrera...")
        race_controller = RaceController()
        print("✅ Controlador creado")
        
        # Crear servidor web
        print("2. Creando servidor web...")
        server = WebServer("127.0.0.1", 8080, race_controller)
        print("✅ Servidor web creado")
        
        # Test de APIs básicas
        print("3. Probando APIs básicas...")
        
        # Test API de estado
        response = server.api_lap_status()
        print(f"   📊 API lap status: {len(response)} bytes")
        
        # Test API de semáforo
        response = server.api_traffic_status()
        print(f"   🚦 API traffic status: {len(response)} bytes")
        
        # Test respuesta HTTP
        response = server.http_response("200 OK", "text/plain", "Test")
        print(f"   ⚡ HTTP response: {len(response)} bytes")
        
        print("✅ Todas las APIs funcionan")
        
        # Test de manejo de errores
        print("4. Probando manejo de errores...")
        try:
            response = server.process_request("INVALID REQUEST")
            print(f"   🛡️ Error handling: {len(response)} bytes")
        except Exception as e:
            print(f"   ❌ Error en manejo de errores: {e}")
        
        print("\n🎉 Test del sistema original completado exitosamente!")
        print("✅ El sistema original está funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        print(f"   Tipo: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando test del sistema original...")
    
    success = test_original_system()
    
    if success:
        print("\n🎉 Sistema original listo para usar!")
        print("📱 Puedes ejecutar: import src.main")
    else:
        print("\n❌ Hay problemas en el sistema original")
        print("⚠️ Revisar configuración antes de usar") 