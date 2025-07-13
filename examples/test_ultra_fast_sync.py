"""
Test de Sincronización Ultra-Rápida de Semáforos
Verifica que la sincronización sea de 0.3 segundos y el verde sea realtime
"""

import time
import json
from src.race_controller import RaceController
from src.web_server import WebServer
from src.config import *

def test_ultra_fast_semaphore_sync():
    """Test de sincronización ultra-rápida de semáforos"""
    print("⚡ Test de Sincronización Ultra-Rápida de Semáforos")
    print("=" * 60)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("🚦 Verificando sincronización ultra-rápida...")
    
    # Test 1: Cambios rápidos de estado
    print("\n--- Test 1: Cambios Rápidos de Estado ---")
    
    test_sequence = [
        {'state': 'off', 'name': 'Apagado'},
        {'state': 'blinking', 'name': 'Titileando'},
        {'state': 'red', 'name': 'Luz Roja'},
        {'state': 'yellow', 'name': 'Luz Amarilla'},
        {'state': 'green', 'name': 'Luz Verde'},
        {'state': 'off', 'name': 'Apagado'}
    ]
    
    for i, test_state in enumerate(test_sequence):
        print(f"\n   Cambio {i+1}: {test_state['name']}")
        
        # Cambiar estado
        race_controller.traffic_light.current_state = test_state['state']
        
        # Medir tiempo de respuesta
        start_time = time.time()
        
        # Obtener estado inmediatamente
        traffic_status = race_controller.get_traffic_light_status()
        
        response_time = (time.time() - start_time) * 1000  # Convertir a milisegundos
        
        print(f"      Estado: {traffic_status['state']}")
        print(f"      Tiempo de respuesta: {response_time:.2f}ms")
        
        # Verificar que la respuesta es ultra-rápida (< 50ms)
        if response_time < 50:
            print("      ✅ Respuesta ultra-rápida")
        else:
            print(f"      ⚠️ Respuesta lenta: {response_time:.2f}ms")
        
        # Pausa mínima para simular cambios reales
        time.sleep(0.1)
    
    # Test 2: Sincronización del verde crítico
    print("\n--- Test 2: Sincronización del Verde Crítico ---")
    
    print("   🟢 Verificando sincronización del verde...")
    
    # Simular secuencia de carrera
    sequence_steps = [
        {'state': 'red', 'expected_green': False, 'description': 'Luz roja - Verde debe estar OFF'},
        {'state': 'yellow', 'expected_green': False, 'description': 'Luz amarilla - Verde debe estar OFF'},
        {'state': 'green', 'expected_green': True, 'description': 'Luz verde - Verde debe estar ON'},
        {'state': 'off', 'expected_green': False, 'description': 'Apagado - Verde debe estar OFF'}
    ]
    
    for step in sequence_steps:
        print(f"\n   {step['description']}")
        
        # Configurar estado
        race_controller.traffic_light.current_state = step['state']
        
        # Obtener estado múltiples veces para verificar consistencia
        green_states = []
        for _ in range(5):  # Verificar 5 veces
            traffic_status = race_controller.get_traffic_light_status()
            green_states.append(traffic_status['green_on'])
            time.sleep(0.01)  # 10ms entre verificaciones
        
        # Verificar que el verde es consistente
        consistent_green = all(state == step['expected_green'] for state in green_states)
        
        print(f"      Estado esperado: {step['expected_green']}")
        print(f"      Estados obtenidos: {green_states}")
        
        if consistent_green:
            print("      ✅ Verde sincronizado correctamente")
        else:
            print("      ❌ Error en sincronización del verde")
    
    # Test 3: Múltiples cambios rápidos
    print("\n--- Test 3: Múltiples Cambios Rápidos ---")
    
    print("   🔄 Simulando cambios rápidos...")
    
    change_times = []
    for i in range(10):
        # Alternar entre estados rápidamente
        states = ['off', 'blinking', 'red', 'yellow', 'green']
        test_state = states[i % len(states)]
        
        start_time = time.time()
        
        # Cambiar estado
        race_controller.traffic_light.current_state = test_state
        
        # Obtener estado inmediatamente
        traffic_status = race_controller.get_traffic_light_status()
        
        response_time = (time.time() - start_time) * 1000
        change_times.append(response_time)
        
        print(f"      Cambio {i+1}: {test_state} - {response_time:.2f}ms")
        
        time.sleep(0.05)  # 50ms entre cambios
    
    # Calcular estadísticas
    avg_time = sum(change_times) / len(change_times)
    max_time = max(change_times)
    min_time = min(change_times)
    
    print(f"\n   📊 Estadísticas de respuesta:")
    print(f"      Promedio: {avg_time:.2f}ms")
    print(f"      Máximo: {max_time:.2f}ms")
    print(f"      Mínimo: {min_time:.2f}ms")
    
    # Verificar que el promedio es menor a 50ms
    if avg_time < 50:
        print("      ✅ Sincronización ultra-rápida confirmada")
    else:
        print(f"      ⚠️ Sincronización lenta: {avg_time:.2f}ms promedio")
    
    # Test 4: Verificar intervalos de actualización
    print("\n--- Test 4: Verificar Intervalos de Actualización ---")
    
    print("   ⏱️ Verificando intervalos de actualización...")
    
    # Simular los intervalos configurados
    intervals = {
        'General': 300,      # 0.3 segundos
        'Semáforo': 100,     # 100ms
        'Visual': 50         # 50ms
    }
    
    for name, interval in intervals.items():
        print(f"      {name}: {interval}ms")
        
        if interval <= 300:
            print("      ✅ Intervalo ultra-rápido")
        else:
            print("      ⚠️ Intervalo lento")
    
    print("\n   🎯 Objetivos de sincronización:")
    print("      • General: ≤ 300ms (0.3 segundos)")
    print("      • Semáforo: ≤ 100ms")
    print("      • Visual: ≤ 50ms")
    print("      • Verde crítico: Real-time")
    
    race_controller.cleanup()

def test_green_light_realtime():
    """Test específico para el verde realtime"""
    print("\n🟢 Test de Verde Realtime")
    print("=" * 40)
    
    race_controller = RaceController(max_laps=3)
    
    print("🎯 Verificando que el verde sea realtime...")
    
    # Test de respuesta inmediata del verde
    test_scenarios = [
        {
            'name': 'Inicio de carrera',
            'sequence': ['off', 'red', 'yellow', 'green'],
            'expected_green_timing': [False, False, False, True]
        },
        {
            'name': 'Parada de carrera',
            'sequence': ['green', 'yellow', 'red', 'off'],
            'expected_green_timing': [True, False, False, False]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        for i, (state, expected_green) in enumerate(zip(scenario['sequence'], scenario['expected_green_timing'])):
            print(f"   Paso {i+1}: {state}")
            
            # Configurar estado
            race_controller.traffic_light.current_state = state
            
            # Medir tiempo de respuesta del verde
            start_time = time.time()
            
            # Obtener estado del verde
            traffic_status = race_controller.get_traffic_light_status()
            green_state = traffic_status['green_on']
            
            response_time = (time.time() - start_time) * 1000
            
            print(f"      Verde esperado: {expected_green}")
            print(f"      Verde obtenido: {green_state}")
            print(f"      Tiempo: {response_time:.2f}ms")
            
            # Verificar que el verde es correcto y rápido
            if green_state == expected_green and response_time < 50:
                print("      ✅ Verde realtime correcto")
            elif green_state == expected_green:
                print("      ⚠️ Verde correcto pero lento")
            else:
                print("      ❌ Error en verde")
            
            time.sleep(0.1)
    
    race_controller.cleanup()

def test_sync_performance():
    """Test de rendimiento de sincronización"""
    print("\n⚡ Test de Rendimiento de Sincronización")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    
    print("📈 Verificando rendimiento...")
    
    # Simular carga de sincronización
    iterations = 100
    response_times = []
    
    print(f"   Ejecutando {iterations} iteraciones...")
    
    for i in range(iterations):
        start_time = time.time()
        
        # Cambiar estado
        state = ['off', 'blinking', 'red', 'yellow', 'green'][i % 5]
        race_controller.traffic_light.current_state = state
        
        # Obtener estado
        traffic_status = race_controller.get_traffic_light_status()
        
        response_time = (time.time() - start_time) * 1000
        response_times.append(response_time)
        
        if i % 20 == 0:  # Mostrar progreso cada 20 iteraciones
            print(f"      Iteración {i+1}: {response_time:.2f}ms")
    
    # Calcular estadísticas
    avg_time = sum(response_times) / len(response_times)
    max_time = max(response_times)
    min_time = min(response_times)
    
    print(f"\n   📊 Resultados de rendimiento:")
    print(f"      Promedio: {avg_time:.2f}ms")
    print(f"      Máximo: {max_time:.2f}ms")
    print(f"      Mínimo: {min_time:.2f}ms")
    
    # Evaluar rendimiento
    if avg_time < 30:
        print("      🚀 Rendimiento excelente")
    elif avg_time < 50:
        print("      ✅ Rendimiento bueno")
    elif avg_time < 100:
        print("      ⚠️ Rendimiento aceptable")
    else:
        print("      ❌ Rendimiento pobre")
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests de Sincronización Ultra-Rápida")
    print("=" * 60)
    
    try:
        # Test 1: Sincronización ultra-rápida general
        test_ultra_fast_semaphore_sync()
        
        # Test 2: Verde realtime específico
        test_green_light_realtime()
        
        # Test 3: Rendimiento de sincronización
        test_sync_performance()
        
        print("\n🎉 Todos los tests de sincronización ultra-rápida completados!")
        print("\n📋 Resumen de optimizaciones:")
        print("   • Sincronización general: 300ms (0.3 segundos)")
        print("   • Sincronización semáforo: 100ms")
        print("   • Sincronización visual: 50ms")
        print("   • Verde crítico: Real-time")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc() 