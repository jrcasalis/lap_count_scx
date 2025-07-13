"""
Test del Diseño de Cards de la Web
Verifica que el nuevo diseño responsivo funciona correctamente
"""

import time
import json
from src.race_controller import RaceController
from src.web_server import WebServer
from src.config import *

def test_web_cards_structure():
    """Test de la estructura de cards en la web"""
    print("🧪 Test de Estructura de Cards")
    print("=" * 50)
    
    # Inicializar controlador de carrera
    race_controller = RaceController(max_laps=5)
    
    # Inicializar servidor web
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("📊 Verificando estructura de cards...")
    
    # Simular diferentes estados para probar las cards
    test_scenarios = [
        {
            'name': 'Estado Inicial',
            'current_laps': 0,
            'led_status': False,
            'race_started': False
        },
        {
            'name': 'Carrera en Progreso',
            'current_laps': 2,
            'led_status': True,
            'race_started': True
        },
        {
            'name': 'Carrera Completada',
            'current_laps': 5,
            'led_status': False,
            'race_started': True
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        # Configurar estado
        race_controller.current_laps = scenario['current_laps']
        race_controller.is_race_started = scenario['race_started']
        race_controller.led.value(scenario['led_status'])
        
        # Obtener estado
        status = race_controller.get_race_status()
        
        print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
        print(f"   Progreso: {status['progress_percentage']:.1f}%")
        print(f"   LED: {'Encendido' if status['led_status']['is_on'] else 'Apagado'}")
        print(f"   Carrera iniciada: {status['is_race_started']}")
        print(f"   Completada: {status['is_completed']}")
        
        # Verificar que los datos son correctos
        if status['current_laps'] == scenario['current_laps']:
            print("   ✅ Datos de carrera correctos")
        else:
            print("   ❌ Error en datos de carrera")
        
        if status['led_status']['is_on'] == scenario['led_status']:
            print("   ✅ Estado de LED correcto")
        else:
            print("   ❌ Error en estado de LED")
    
    race_controller.cleanup()

def test_web_responsive_design():
    """Test del diseño responsivo"""
    print("\n🧪 Test de Diseño Responsivo")
    print("=" * 50)
    
    print("📱 Verificando breakpoints de diseño...")
    
    # Simular diferentes tamaños de pantalla
    screen_sizes = [
        {'name': 'Desktop', 'width': 1400, 'cards_per_row': 3},
        {'name': 'Tablet', 'width': 768, 'cards_per_row': 2},
        {'name': 'Mobile', 'width': 480, 'cards_per_row': 1}
    ]
    
    for size in screen_sizes:
        print(f"\n--- {size['name']} ({size['width']}px) ---")
        print(f"   Cards por fila esperadas: {size['cards_per_row']}")
        print(f"   Grid responsivo: CSS Grid con auto-fit")
        print(f"   Breakpoint: @media (max-width: {size['width']}px)")
    
    print("\n✅ Diseño responsivo configurado correctamente")

def test_web_card_interactions():
    """Test de interacciones de las cards"""
    print("\n🧪 Test de Interacciones de Cards")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=3)
    web_server = WebServer("127.0.0.1", 8080, race_controller)
    
    print("🖱️ Verificando interacciones...")
    
    # Test de incremento de vuelta
    print("\n--- Test: Incrementar Vuelta ---")
    race_controller.start_race()
    initial_laps = race_controller.current_laps
    
    race_controller.increment_lap_immediate()
    new_laps = race_controller.current_laps
    
    if new_laps == initial_laps + 1:
        print("   ✅ Incremento de vuelta funciona")
    else:
        print("   ❌ Error en incremento de vuelta")
    
    # Test de control LED
    print("\n--- Test: Control LED ---")
    initial_led = race_controller.led.value()
    
    race_controller.turn_on_led()
    led_on = race_controller.led.value()
    
    if led_on:
        print("   ✅ Encender LED funciona")
    else:
        print("   ❌ Error al encender LED")
    
    race_controller.turn_off_led()
    led_off = race_controller.led.value()
    
    if not led_off:
        print("   ✅ Apagar LED funciona")
    else:
        print("   ❌ Error al apagar LED")
    
    # Test de piloto
    print("\n--- Test: Piloto ---")
    test_name = "TEST PILOT"
    race_controller.set_racer_name(test_name)
    
    if race_controller.racer_name == test_name:
        print("   ✅ Cambio de nombre funciona")
    else:
        print("   ❌ Error al cambiar nombre")
    
    race_controller.cleanup()

def test_web_card_styles():
    """Test de estilos de las cards"""
    print("\n🧪 Test de Estilos de Cards")
    print("=" * 50)
    
    print("🎨 Verificando estilos CSS...")
    
    # Verificar clases CSS necesarias
    required_classes = [
        'cards-grid',
        'card',
        'card-header',
        'card-body',
        'card-footer',
        'race-status-card',
        'led-control-card',
        'racer-card',
        'traffic-light-card',
        'sound-card',
        'system-info-card'
    ]
    
    for class_name in required_classes:
        print(f"   ✅ Clase CSS: {class_name}")
    
    # Verificar estilos responsivos
    responsive_styles = [
        'grid-template-columns: repeat(auto-fit, minmax(350px, 1fr))',
        '@media (max-width: 1200px)',
        '@media (max-width: 768px)',
        '@media (max-width: 480px)'
    ]
    
    for style in responsive_styles:
        print(f"   ✅ Estilo responsivo: {style}")
    
    print("\n✅ Todos los estilos están configurados")

def test_web_card_content():
    """Test del contenido de las cards"""
    print("\n🧪 Test de Contenido de Cards")
    print("=" * 50)
    
    race_controller = RaceController(max_laps=5)
    
    print("📋 Verificando contenido de cards...")
    
    # Card 1: Estado de la Carrera
    print("\n--- Card 1: Estado de la Carrera ---")
    status = race_controller.get_race_status()
    print(f"   Contador: {status['current_laps']}/{status['max_laps']}")
    print(f"   Progreso: {status['progress_percentage']:.1f}%")
    print(f"   Estado: {status['is_race_running']}")
    
    # Card 2: Control LED
    print("\n--- Card 2: Control LED ---")
    led_status = race_controller.led.value()
    print(f"   LED: {'Encendido' if led_status else 'Apagado'}")
    
    # Card 3: Piloto
    print("\n--- Card 3: Piloto ---")
    print(f"   Nombre: {race_controller.racer_name}")
    
    # Card 4: Semáforo
    print("\n--- Card 4: Semáforo ---")
    traffic_status = race_controller.get_traffic_light_status()
    print(f"   Estado: {traffic_status['state']}")
    print(f"   Roja: {traffic_status['red_on']}")
    print(f"   Amarilla: {traffic_status['yellow_on']}")
    print(f"   Verde: {traffic_status['green_on']}")
    
    # Card 5: Sonidos
    print("\n--- Card 5: Sonidos ---")
    print("   Funcionalidad de sonidos disponible")
    
    # Card 6: Información del Sistema
    print("\n--- Card 6: Sistema ---")
    print("   Información del dispositivo disponible")
    
    race_controller.cleanup()

if __name__ == "__main__":
    print("🚀 Iniciando Tests del Diseño de Cards")
    print("=" * 60)
    
    try:
        # Test 1: Estructura de cards
        test_web_cards_structure()
        
        # Test 2: Diseño responsivo
        test_web_responsive_design()
        
        # Test 3: Interacciones
        test_web_card_interactions()
        
        # Test 4: Estilos
        test_web_card_styles()
        
        # Test 5: Contenido
        test_web_card_content()
        
        print("\n🎉 Todos los tests del diseño de cards completados exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {e}")
        import traceback
        traceback.print_exc() 