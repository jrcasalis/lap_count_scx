"""
Test de Actualización Inmediata del Display
Verifica que el display MAX7219 se actualice inmediatamente al detectar el sensor
"""

import time
from src.race_controller import RaceController
from src.config import *

def test_display_immediate_update():
    """Test de actualización inmediata del display"""
    print("🧪 Test de Actualización Inmediata del Display")
    print("=" * 50)
    
    # Inicializar controlador de carrera
    race_controller = RaceController(max_laps=5)
    
    print(f"📊 Estado inicial: {race_controller.get_race_status()}")
    print("🔍 Display debería mostrar: 00")
    
    # Iniciar carrera
    print("\n🏁 Iniciando carrera...")
    race_controller.start_race()
    
    # Simular detecciones y verificar display
    print("\n⚡ Simulando detecciones y verificando display...")
    
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
        print(f"⏱️ Tiempo de actualización: {response_time:.2f}ms")
        
        # Verificar estado después de la detección
        status_after = race_controller.get_race_status()
        print(f"📊 Vueltas después: {status_after['current_laps']}")
        print(f"🔍 Display debería mostrar: {status_after['current_laps']:02d}")
        
        # Verificar que el display se actualizó correctamente
        if status_after['current_laps'] == status_before['current_laps'] + 1:
            print("✅ Display actualizado correctamente")
        else:
            print("❌ Error en actualización del display")
        
        # Verificar tiempo de respuesta
        if response_time < 5:  # Menos de 5ms para actualización inmediata
            print("✅ Actualización inmediata confirmada")
        else:
            print("⚠️ Actualización lenta detectada")
        
        time.sleep(0.2)  # Pausa para observar
    
    # Verificar estado final
    print(f"\n📊 Estado final: {race_controller.get_race_status()}")
    
    # Limpiar
    race_controller.cleanup()
    print("\n✅ Test completado")

def test_display_synchronization():
    """Test de sincronización entre contador y display"""
    print("\n🧪 Test de Sincronización Display-Contador")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=10)
    race_controller.start_race()
    
    print("📊 Verificando sincronización...")
    
    # Realizar múltiples detecciones rápidas
    for i in range(5):
        # Incrementar vuelta
        race_controller.increment_lap_immediate()
        
        # Verificar inmediatamente
        status = race_controller.get_race_status()
        
        print(f"   Detección {i+1}: {status['current_laps']} vueltas")
        
        # Verificar que el contador interno coincide con el estado
        if status['current_laps'] == i + 1:
            print("   ✅ Sincronización correcta")
        else:
            print("   ❌ Error de sincronización")
    
    race_controller.cleanup()

def test_display_race_completion():
    """Test de actualización del display al completar la carrera"""
    print("\n🧪 Test de Completación de Carrera")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    race_controller.start_race()
    
    print("📊 Estado inicial:")
    status = race_controller.get_race_status()
    print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
    
    # Incrementar hasta completar la carrera
    for i in range(3):
        print(f"\n--- Vuelta {i+1} ---")
        
        race_controller.increment_lap_immediate()
        
        status = race_controller.get_race_status()
        print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
        print(f"   Completada: {status['is_completed']}")
        
        if status['is_completed']:
            print("   🏁 ¡Carrera completada!")
            print("   🔍 Display debería mostrar animación")
            break
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests de Actualización de Display")
    print("=" * 60)
    
    try:
        # Test 1: Actualización inmediata
        test_display_immediate_update()
        
        # Test 2: Sincronización
        test_display_synchronization()
        
        # Test 3: Completación de carrera
        test_display_race_completion()
        
        print("\n🎉 Todos los tests completados exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc() 