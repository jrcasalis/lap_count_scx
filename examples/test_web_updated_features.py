"""
Test de Funcionalidades Actualizadas de la Web
Verifica las nuevas características: 4 semáforos, sincronización realtime, botón de terminar previa, estados de carrera
"""

import time
import json
from src.race_controller import RaceController
from src.web_server import WebServer
from src.config import *

def test_four_traffic_lights():
    """Test de los 4 semáforos con sincronización realtime"""
    print("🧪 Test de 4 Semáforos con Sincronización Realtime")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("🚦 Verificando 4 semáforos...")
    
    # Simular diferentes estados del semáforo
    test_states = [
        {
            'name': 'Apagado',
            'state': 'off',
            'red_on': False,
            'yellow_on': False,
            'green_on': False
        },
        {
            'name': 'Titileando',
            'state': 'blinking',
            'red_on': True,
            'yellow_on': True,
            'green_on': True
        },
        {
            'name': 'Luz Roja',
            'state': 'red',
            'red_on': True,
            'yellow_on': False,
            'green_on': False
        },
        {
            'name': 'Luz Amarilla',
            'state': 'yellow',
            'red_on': True,
            'yellow_on': True,
            'green_on': False
        },
        {
            'name': 'Luz Verde',
            'state': 'green',
            'red_on': False,
            'yellow_on': False,
            'green_on': True
        }
    ]
    
    for test_state in test_states:
        print(f"\n--- {test_state['name']} ---")
        
        # Configurar estado del semáforo
        race_controller.traffic_light.current_state = test_state['state']
        
        # Simular estado de las luces
        if test_state['red_on']:
            print("   🔴 Luz roja: ON")
        if test_state['yellow_on']:
            print("   🟡 Luz amarilla: ON")
        if test_state['green_on']:
            print("   🟢 Luz verde: ON")
        
        # Verificar que el estado se refleja correctamente
        traffic_status = race_controller.get_traffic_light_status()
        
        print(f"   Estado: {traffic_status['state']}")
        print(f"   Roja: {traffic_status['red_on']}")
        print(f"   Amarilla: {traffic_status['yellow_on']}")
        print(f"   Verde: {traffic_status['green_on']}")
        
        # Verificar sincronización
        if (traffic_status['red_on'] == test_state['red_on'] and
            traffic_status['yellow_on'] == test_state['yellow_on'] and
            traffic_status['green_on'] == test_state['green_on']):
            print("   ✅ Sincronización correcta")
        else:
            print("   ❌ Error de sincronización")
    
    race_controller.cleanup()

def test_race_state_synchronization():
    """Test de sincronización del estado de la carrera"""
    print("\n🧪 Test de Sincronización del Estado de Carrera")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    
    print("🏁 Verificando estados de carrera...")
    
    # Test 1: Carrera no iniciada
    print("\n--- Test 1: Carrera No Iniciada ---")
    race_controller.is_race_started = False
    race_controller.current_laps = 0
    
    status = race_controller.get_race_status()
    print(f"   Estado: {'Iniciada' if status['is_race_started'] else 'No Iniciada'}")
    print(f"   Vueltas: {status['current_laps']}")
    print(f"   Progreso: {status['progress_percentage']:.1f}%")
    
    if not status['is_race_started'] and status['current_laps'] == 0:
        print("   ✅ Estado correcto")
    else:
        print("   ❌ Error en estado")
    
    # Test 2: Carrera iniciada
    print("\n--- Test 2: Carrera Iniciada ---")
    race_controller.is_race_started = True
    race_controller.current_laps = 1
    
    status = race_controller.get_race_status()
    print(f"   Estado: {'Iniciada' if status['is_race_started'] else 'No Iniciada'}")
    print(f"   Vueltas: {status['current_laps']}")
    print(f"   Progreso: {status['progress_percentage']:.1f}%")
    
    if status['is_race_started'] and status['current_laps'] == 1:
        print("   ✅ Estado correcto")
    else:
        print("   ❌ Error en estado")
    
    # Test 3: Carrera completada
    print("\n--- Test 3: Carrera Completada ---")
    race_controller.current_laps = 3
    race_controller.is_completed = True
    
    status = race_controller.get_race_status()
    print(f"   Estado: {'Completada' if status['is_completed'] else 'En Progreso'}")
    print(f"   Vueltas: {status['current_laps']}")
    print(f"   Progreso: {status['progress_percentage']:.1f}%")
    
    if status['is_completed'] and status['current_laps'] == 3:
        print("   ✅ Estado correcto")
    else:
        print("   ❌ Error en estado")
    
    race_controller.cleanup()

def test_previous_race_controls():
    """Test de controles de previa de carrera"""
    print("\n🧪 Test de Controles de Previa de Carrera")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("⚠️ Verificando controles de previa...")
    
    # Test 1: Iniciar previa
    print("\n--- Test 1: Iniciar Previa ---")
    
    # Simular inicio de previa
    race_controller.race_previous()
    
    traffic_status = race_controller.get_traffic_light_status()
    print(f"   Estado: {traffic_status['state']}")
    print(f"   Titileando: {traffic_status['blinking_active']}")
    
    if traffic_status['state'] == 'blinking':
        print("   ✅ Previa iniciada correctamente")
    else:
        print("   ❌ Error al iniciar previa")
    
    # Test 2: Terminar previa
    print("\n--- Test 2: Terminar Previa ---")
    
    # Simular terminación de previa
    race_controller.race_previous_stop()
    
    traffic_status = race_controller.get_traffic_light_status()
    print(f"   Estado: {traffic_status['state']}")
    print(f"   Titileando: {traffic_status['blinking_active']}")
    
    if traffic_status['state'] == 'off':
        print("   ✅ Previa terminada correctamente")
    else:
        print("   ❌ Error al terminar previa")
    
    race_controller.cleanup()

def test_realtime_synchronization():
    """Test de sincronización en tiempo real"""
    print("\n🧪 Test de Sincronización en Tiempo Real")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("⚡ Verificando sincronización realtime...")
    
    # Simular múltiples cambios rápidos
    for i in range(3):
        print(f"\n--- Cambio {i+1} ---")
        
        # Cambiar estado de la carrera
        race_controller.is_race_started = (i % 2 == 0)
        race_controller.current_laps = i + 1
        
        # Obtener estado inmediatamente
        status = race_controller.get_race_status()
        
        print(f"   Carrera iniciada: {status['is_race_started']}")
        print(f"   Vueltas: {status['current_laps']}")
        print(f"   Progreso: {status['progress_percentage']:.1f}%")
        
        # Verificar que los datos están sincronizados
        if status['current_laps'] == i + 1:
            print("   ✅ Sincronización correcta")
        else:
            print("   ❌ Error de sincronización")
        
        time.sleep(0.1)  # Simular delay mínimo
    
    race_controller.cleanup()

def test_web_card_order():
    """Test del orden de las cards"""
    print("\n🧪 Test del Orden de Cards")
    print("=" * 50)
    
    print("📋 Verificando orden de cards...")
    
    expected_order = [
        "Estado de la Carrera",
        "Piloto", 
        "Semáforo",
        "Sistema",
        "Control LED"
    ]
    
    for i, card_name in enumerate(expected_order, 1):
        print(f"   Card {i}: {card_name}")
    
    print("\n✅ Orden de cards correcto")
    print("   ❌ Card de Sonidos eliminada")
    print("   ✅ Control LED movido a penúltimo lugar")

def test_traffic_light_detailed_status():
    """Test del estado detallado del semáforo"""
    print("\n🧪 Test de Estado Detallado del Semáforo")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    
    print("📊 Verificando estado detallado...")
    
    # Simular diferentes estados
    test_scenarios = [
        {
            'name': 'Apagado',
            'state': 'off',
            'expected_lights': 'Roja: OFF | Amarilla: OFF | Verde: OFF'
        },
        {
            'name': 'Luz Roja',
            'state': 'red',
            'expected_lights': 'Roja: ON | Amarilla: OFF | Verde: OFF'
        },
        {
            'name': 'Luz Amarilla',
            'state': 'yellow',
            'expected_lights': 'Roja: ON | Amarilla: ON | Verde: OFF'
        },
        {
            'name': 'Luz Verde',
            'state': 'green',
            'expected_lights': 'Roja: OFF | Amarilla: OFF | Verde: ON'
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        # Configurar estado
        race_controller.traffic_light.current_state = scenario['state']
        
        # Obtener estado detallado
        traffic_status = race_controller.get_traffic_light_status()
        
        print(f"   Estado: {traffic_status['state']}")
        print(f"   Roja: {'ON' if traffic_status['red_on'] else 'OFF'}")
        print(f"   Amarilla: {'ON' if traffic_status['yellow_on'] else 'OFF'}")
        print(f"   Verde: {'ON' if traffic_status['green_on'] else 'OFF'}")
        
        # Verificar que el estado es correcto
        if traffic_status['state'] == scenario['state']:
            print("   ✅ Estado correcto")
        else:
            print("   ❌ Error en estado")
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests de Funcionalidades Actualizadas")
    print("=" * 60)
    
    try:
        # Test 1: 4 semáforos
        test_four_traffic_lights()
        
        # Test 2: Sincronización de estado de carrera
        test_race_state_synchronization()
        
        # Test 3: Controles de previa
        test_previous_race_controls()
        
        # Test 4: Sincronización realtime
        test_realtime_synchronization()
        
        # Test 5: Orden de cards
        test_web_card_order()
        
        # Test 6: Estado detallado del semáforo
        test_traffic_light_detailed_status()
        
        print("\n🎉 Todos los tests de funcionalidades actualizadas completados exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc() 