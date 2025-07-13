"""
Test de Funcionalidades de Fin de Carrera y Sincronización
Verifica el fin de carrera automático, sincronización realtime y manejo de previa
"""

import time
import json
from src.race_controller import RaceController
from src.web_server import WebServer
from src.config import *

def test_race_completion_automatic():
    """Test de fin de carrera automático"""
    print("🏁 Test de Fin de Carrera Automático")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("🎯 Verificando fin de carrera automático...")
    
    # Simular carrera hasta completar
    print("\n--- Simulando carrera ---")
    
    # Incrementar vueltas hasta completar
    for i in range(3):
        print(f"   Vuelta {i+1}/3")
        race_controller.increment_lap_immediate()
        
        # Verificar estado
        status = race_controller.get_race_status()
        print(f"      Vueltas: {status['current_laps']}")
        print(f"      Completada: {status['is_completed']}")
        print(f"      Carrera iniciada: {status['is_race_started']}")
        
        time.sleep(0.1)
    
    # Verificar que la carrera se completó automáticamente
    print("\n--- Verificando fin automático ---")
    
    # Esperar a que termine la animación y el fin automático
    time.sleep(2)
    
    final_status = race_controller.get_race_status()
    print(f"   Estado final:")
    print(f"      Vueltas: {final_status['current_laps']}")
    print(f"      Completada: {final_status['is_completed']}")
    print(f"      Carrera iniciada: {final_status['is_race_started']}")
    
    # Verificar que se reseteó automáticamente
    if final_status['current_laps'] == 0 and not final_status['is_completed']:
        print("   ✅ Fin de carrera automático correcto")
    else:
        print("   ❌ Error en fin de carrera automático")
    
    race_controller.cleanup()

def test_previa_automatic_finish():
    """Test de fin automático de previa al iniciar carrera"""
    print("\n⚠️ Test de Fin Automático de Previa")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("🔄 Verificando fin automático de previa...")
    
    # 1. Iniciar previa
    print("\n--- Paso 1: Iniciar Previa ---")
    race_controller.race_previous()
    
    traffic_status = race_controller.get_traffic_light_status()
    print(f"   Estado del semáforo: {traffic_status['state']}")
    print(f"   Titileando: {traffic_status['blinking_active']}")
    
    if traffic_status['state'] == 'blinking':
        print("   ✅ Previa iniciada correctamente")
    else:
        print("   ❌ Error al iniciar previa")
    
    # 2. Iniciar carrera (debe terminar previa automáticamente)
    print("\n--- Paso 2: Iniciar Carrera ---")
    race_controller.start_race()
    
    traffic_status = race_controller.get_traffic_light_status()
    race_status = race_controller.get_race_status()
    
    print(f"   Estado del semáforo: {traffic_status['state']}")
    print(f"   Titileando: {traffic_status['blinking_active']}")
    print(f"   Carrera iniciada: {race_status['is_race_started']}")
    
    # Verificar que la previa se terminó automáticamente
    if traffic_status['state'] != 'blinking' and race_status['is_race_started']:
        print("   ✅ Previa terminada automáticamente")
    else:
        print("   ❌ Error en fin automático de previa")
    
    race_controller.cleanup()

def test_realtime_sync_improved():
    """Test de sincronización realtime mejorada"""
    print("\n⚡ Test de Sincronización Realtime Mejorada")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("🔄 Verificando sincronización realtime...")
    
    # Simular múltiples incrementos rápidos
    print("\n--- Simulando incrementos rápidos ---")
    
    sync_times = []
    for i in range(5):
        start_time = time.time()
        
        # Incrementar vuelta
        race_controller.increment_lap_immediate()
        
        # Obtener estado inmediatamente
        status = race_controller.get_race_status()
        
        sync_time = (time.time() - start_time) * 1000  # Convertir a ms
        sync_times.append(sync_time)
        
        print(f"   Incremento {i+1}: {status['current_laps']} vueltas - {sync_time:.2f}ms")
        
        time.sleep(0.05)  # 50ms entre incrementos
    
    # Calcular estadísticas de sincronización
    avg_sync = sum(sync_times) / len(sync_times)
    max_sync = max(sync_times)
    min_sync = min(sync_times)
    
    print(f"\n   📊 Estadísticas de sincronización:")
    print(f"      Promedio: {avg_sync:.2f}ms")
    print(f"      Máximo: {max_sync:.2f}ms")
    print(f"      Mínimo: {min_sync:.2f}ms")
    
    # Verificar que la sincronización es rápida
    if avg_sync < 50:
        print("   ✅ Sincronización ultra-rápida confirmada")
    else:
        print(f"   ⚠️ Sincronización lenta: {avg_sync:.2f}ms promedio")
    
    race_controller.cleanup()

def test_traffic_light_race_state():
    """Test del estado de carrera en el semáforo"""
    print("\n🚦 Test de Estado de Carrera en Semáforo")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("📊 Verificando estado de carrera en semáforo...")
    
    # Test 1: Carrera no iniciada
    print("\n--- Test 1: Carrera No Iniciada ---")
    race_controller.is_race_started = False
    
    traffic_status = race_controller.get_traffic_light_status()
    race_status = race_controller.get_race_status()
    
    print(f"   Estado del semáforo: {traffic_status['state']}")
    print(f"   Carrera iniciada: {race_status['is_race_started']}")
    
    if not race_status['is_race_started']:
        print("   ✅ Estado correcto")
    else:
        print("   ❌ Error en estado")
    
    # Test 2: Carrera iniciada
    print("\n--- Test 2: Carrera Iniciada ---")
    race_controller.start_race()
    
    traffic_status = race_controller.get_traffic_light_status()
    race_status = race_controller.get_race_status()
    
    print(f"   Estado del semáforo: {traffic_status['state']}")
    print(f"   Carrera iniciada: {race_status['is_race_started']}")
    
    if race_status['is_race_started']:
        print("   ✅ Estado correcto")
    else:
        print("   ❌ Error en estado")
    
    # Test 3: Carrera completada
    print("\n--- Test 3: Carrera Completada ---")
    race_controller.current_laps = 3
    race_controller.complete_race()
    
    # Esperar a que termine el fin automático
    time.sleep(2)
    
    traffic_status = race_controller.get_traffic_light_status()
    race_status = race_controller.get_race_status()
    
    print(f"   Estado del semáforo: {traffic_status['state']}")
    print(f"   Carrera iniciada: {race_status['is_race_started']}")
    print(f"   Vueltas: {race_status['current_laps']}")
    
    if not race_status['is_race_started'] and race_status['current_laps'] == 0:
        print("   ✅ Estado correcto después de completar")
    else:
        print("   ❌ Error en estado después de completar")
    
    race_controller.cleanup()

def test_web_sync_improvements():
    """Test de mejoras de sincronización web"""
    print("\n🌐 Test de Mejoras de Sincronización Web")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("📱 Verificando sincronización web...")
    
    # Simular actualizaciones web rápidas
    print("\n--- Simulando actualizaciones web ---")
    
    web_sync_times = []
    for i in range(3):
        start_time = time.time()
        
        # Simular incremento de vuelta
        race_controller.increment_lap_immediate()
        
        # Simular obtención de estado web
        race_status = race_controller.get_race_status()
        traffic_status = race_controller.get_traffic_light_status()
        
        sync_time = (time.time() - start_time) * 1000
        web_sync_times.append(sync_time)
        
        print(f"   Actualización {i+1}: {race_status['current_laps']} vueltas - {sync_time:.2f}ms")
        
        time.sleep(0.1)
    
    # Calcular estadísticas
    avg_web_sync = sum(web_sync_times) / len(web_sync_times)
    
    print(f"\n   📊 Sincronización web:")
    print(f"      Promedio: {avg_web_sync:.2f}ms")
    
    if avg_web_sync < 100:
        print("   ✅ Sincronización web rápida")
    else:
        print(f"   ⚠️ Sincronización web lenta: {avg_web_sync:.2f}ms")
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests de Funcionalidades de Fin de Carrera")
    print("=" * 60)
    
    try:
        # Test 1: Fin de carrera automático
        test_race_completion_automatic()
        
        # Test 2: Fin automático de previa
        test_previa_automatic_finish()
        
        # Test 3: Sincronización realtime mejorada
        test_realtime_sync_improved()
        
        # Test 4: Estado de carrera en semáforo
        test_traffic_light_race_state()
        
        # Test 5: Mejoras de sincronización web
        test_web_sync_improvements()
        
        print("\n🎉 Todos los tests de funcionalidades de fin de carrera completados!")
        print("\n📋 Resumen de mejoras implementadas:")
        print("   • Fin de carrera automático con banderas")
        print("   • Terminación automática de previa al iniciar carrera")
        print("   • Sincronización realtime mejorada (0.3 segundos)")
        print("   • Estado de carrera sincronizado en semáforo")
        print("   • Reset automático de vueltas al completar")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc() 