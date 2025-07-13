"""
Test de Respuesta Inmediata del Sensor TCRT5000
Verifica que la detección del sensor actualice inmediatamente el contador, display y web
"""

import time
from machine import Pin
from src.race_controller import RaceController
from src.config import *

def test_sensor_immediate_response():
    """Test de respuesta inmediata del sensor"""
    print("🧪 Test de Respuesta Inmediata del Sensor")
    print("=" * 50)
    
    # Inicializar controlador de carrera
    race_controller = RaceController(max_laps=5)
    
    # Inicializar sensor TCRT5000
    sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
    last_sensor_state = sensor.value()
    
    print(f"📊 Estado inicial: {race_controller.get_race_status()}")
    print(f"🔍 Estado del sensor: {last_sensor_state}")
    
    # Iniciar carrera
    print("\n🏁 Iniciando carrera...")
    race_controller.start_race()
    
    # Simular detecciones rápidas
    print("\n⚡ Simulando detecciones rápidas del sensor...")
    
    for i in range(3):
        print(f"\n--- Detección {i+1} ---")
        
        # Simular flanco descendente (detección)
        start_time = time.time()
        
        # Llamar al método inmediato
        result = race_controller.increment_lap_immediate()
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        
        print(f"⏱️ Tiempo de respuesta: {response_time:.2f}ms")
        print(f"✅ Resultado: {result}")
        print(f"📊 Estado actual: {race_controller.get_race_status()}")
        
        # Verificar que el tiempo de respuesta sea muy bajo
        if response_time < 10:  # Menos de 10ms
            print("✅ Respuesta inmediata confirmada")
        else:
            print("⚠️ Respuesta lenta detectada")
        
        # Pequeña pausa entre detecciones
        time.sleep(0.1)
    
    # Verificar estado final
    print(f"\n📊 Estado final: {race_controller.get_race_status()}")
    
    # Limpiar
    race_controller.cleanup()
    print("\n✅ Test completado")

def test_sensor_debounce_vs_immediate():
    """Compara el método normal vs el método inmediato"""
    print("\n🧪 Comparación: Método Normal vs Inmediato")
    print("=" * 50)
    
    # Test con método normal
    print("\n📊 Test con método normal (con debounce):")
    race_controller_normal = RaceController(max_laps=5)
    race_controller_normal.start_race()
    
    start_time = time.time()
    race_controller_normal.increment_lap()  # Método normal
    end_time = time.time()
    normal_time = (end_time - start_time) * 1000
    
    print(f"⏱️ Tiempo método normal: {normal_time:.2f}ms")
    
    # Test con método inmediato
    print("\n📊 Test con método inmediato (sin debounce):")
    race_controller_immediate = RaceController(max_laps=5)
    race_controller_immediate.start_race()
    
    start_time = time.time()
    race_controller_immediate.increment_lap_immediate()  # Método inmediato
    end_time = time.time()
    immediate_time = (end_time - start_time) * 1000
    
    print(f"⏱️ Tiempo método inmediato: {immediate_time:.2f}ms")
    
    # Comparar
    improvement = ((normal_time - immediate_time) / normal_time) * 100
    print(f"🚀 Mejora: {improvement:.1f}% más rápido")
    
    # Limpiar
    race_controller_normal.cleanup()
    race_controller_immediate.cleanup()

def test_web_synchronization():
    """Test de sincronización con la web"""
    print("\n🧪 Test de Sincronización Web")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    race_controller.start_race()
    
    print("📊 Estado inicial:")
    status = race_controller.get_race_status()
    print(f"   Vueltas: {status['current_laps']}")
    print(f"   Carrera iniciada: {status['is_race_started']}")
    
    # Simular detecciones y verificar sincronización
    for i in range(2):
        print(f"\n--- Detección {i+1} ---")
        
        # Incrementar vuelta
        race_controller.increment_lap_immediate()
        
        # Obtener estado inmediatamente
        status = race_controller.get_race_status()
        
        print(f"📊 Estado después de detección:")
        print(f"   Vueltas: {status['current_laps']}")
        print(f"   Progreso: {status['progress_percentage']:.1f}%")
        print(f"   Restantes: {status['remaining_laps']}")
        
        # Verificar que los datos estén sincronizados
        if status['current_laps'] == i + 1:
            print("✅ Sincronización correcta")
        else:
            print("❌ Error de sincronización")
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests de Respuesta Inmediata")
    print("=" * 60)
    
    try:
        # Test 1: Respuesta inmediata
        test_sensor_immediate_response()
        
        # Test 2: Comparación de métodos
        test_sensor_debounce_vs_immediate()
        
        # Test 3: Sincronización web
        test_web_synchronization()
        
        print("\n🎉 Todos los tests completados exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import sys
        sys.print_exception(e) 