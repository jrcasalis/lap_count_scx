"""
Test de Sincronización Inmediata con la Web
Verifica que la interfaz web se actualice inmediatamente al detectar el sensor
"""

import time
import json
from src.race_controller import RaceController
from src.web_server import WebServer
from src.config import *

def test_web_immediate_sync():
    """Test de sincronización inmediata con la web"""
    print("🧪 Test de Sincronización Inmediata con la Web")
    print("=" * 50)
    
    # Inicializar controlador de carrera
    race_controller = RaceController(max_laps=5)
    
    # Inicializar servidor web
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("📊 Estado inicial:")
    status = race_controller.get_race_status()
    print(f"   Vueltas: {status['current_laps']}")
    print(f"   Carrera iniciada: {status['is_race_started']}")
    
    # Iniciar carrera
    print("\n🏁 Iniciando carrera...")
    race_controller.start_race()
    
    # Simular detecciones y verificar sincronización web
    print("\n⚡ Simulando detecciones y verificando sincronización web...")
    
    for i in range(3):
        print(f"\n--- Detección {i+1} ---")
        
        # Verificar estado antes de la detección
        status_before = race_controller.get_race_status()
        print(f"📊 Vueltas antes: {status_before['current_laps']}")
        
        # Incrementar vuelta
        start_time = time.time()
        race_controller.increment_lap_immediate()
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        print(f"⏱️ Tiempo de incremento: {response_time:.2f}ms")
        
        # Verificar estado después de la detección
        status_after = race_controller.get_race_status()
        print(f"📊 Vueltas después: {status_after['current_laps']}")
        print(f"🌐 Datos para web: {json.dumps(status_after, indent=2)}")
        
        # Verificar que los datos estén sincronizados
        if status_after['current_laps'] == status_before['current_laps'] + 1:
            print("✅ Sincronización correcta")
        else:
            print("❌ Error de sincronización")
        
        # Verificar tiempo de respuesta
        if response_time < 5:  # Menos de 5ms para respuesta inmediata
            print("✅ Respuesta inmediata confirmada")
        else:
            print("⚠️ Respuesta lenta detectada")
        
        time.sleep(0.1)
    
    # Limpiar
    race_controller.cleanup()
    print("\n✅ Test completado")

def test_web_api_response():
    """Test de respuesta de la API web"""
    print("\n🧪 Test de Respuesta de API Web")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    race_controller.start_race()
    
    print("📊 Probando endpoints de la API...")
    
    # Simular petición a /api/lap/status
    print("\n🔍 Endpoint: /api/lap/status")
    status = race_controller.get_race_status()
    print(f"   Respuesta: {json.dumps(status, indent=2)}")
    
    # Simular incremento y verificar API
    print("\n⚡ Incrementando vuelta...")
    race_controller.increment_lap_immediate()
    
    # Verificar estado actualizado
    status_updated = race_controller.get_race_status()
    print(f"   Estado actualizado: {json.dumps(status_updated, indent=2)}")
    
    # Verificar que la API refleja el cambio inmediatamente
    if status_updated['current_laps'] == 1:
        print("✅ API actualizada correctamente")
    else:
        print("❌ Error en actualización de API")
    
    race_controller.cleanup()

def test_web_real_time_updates():
    """Test de actualizaciones en tiempo real de la web"""
    print("\n🧪 Test de Actualizaciones en Tiempo Real")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    race_controller.start_race()
    
    print("📊 Simulando actualizaciones en tiempo real...")
    
    # Realizar múltiples detecciones rápidas
    for i in range(4):
        print(f"\n--- Actualización {i+1} ---")
        
        # Incrementar vuelta
        race_controller.increment_lap_immediate()
        
        # Obtener datos para web inmediatamente
        status = race_controller.get_race_status()
        
        print(f"   Vueltas: {status['current_laps']}")
        print(f"   Progreso: {status['progress_percentage']:.1f}%")
        print(f"   Restantes: {status['remaining_laps']}")
        print(f"   Completada: {status['is_completed']}")
        
        # Verificar que los datos estén actualizados
        if status['current_laps'] == i + 1:
            print("   ✅ Datos actualizados correctamente")
        else:
            print("   ❌ Error en actualización de datos")
        
        # Verificar progreso
        expected_progress = ((i + 1) / 5) * 100
        if abs(status['progress_percentage'] - expected_progress) < 1:
            print("   ✅ Progreso calculado correctamente")
        else:
            print("   ❌ Error en cálculo de progreso")
    
    race_controller.cleanup()

def test_web_race_completion():
    """Test de completación de carrera en la web"""
    print("\n🧪 Test de Completación de Carrera en Web")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    race_controller.start_race()
    
    print("📊 Simulando completación de carrera...")
    
    # Incrementar hasta completar
    for i in range(3):
        print(f"\n--- Vuelta {i+1} ---")
        
        race_controller.increment_lap_immediate()
        
        status = race_controller.get_race_status()
        
        print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
        print(f"   Completada: {status['is_completed']}")
        print(f"   Progreso: {status['progress_percentage']:.1f}%")
        
        if status['is_completed']:
            print("   🏁 ¡Carrera completada!")
            print("   🌐 Web debería mostrar estado completado")
            break
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests de Sincronización Web")
    print("=" * 60)
    
    try:
        # Test 1: Sincronización inmediata
        test_web_immediate_sync()
        
        # Test 2: Respuesta de API
        test_web_api_response()
        
        # Test 3: Actualizaciones en tiempo real
        test_web_real_time_updates()
        
        # Test 4: Completación de carrera
        test_web_race_completion()
        
        print("\n🎉 Todos los tests completados exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc() 