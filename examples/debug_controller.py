"""
Script de diagnóstico para detectar el problema con el WebServer
"""

from race_controller import RaceController
from led_controller import LEDController
from web_server import WebServer

def debug_controller():
    """Función de diagnóstico"""
    print("=== DIAGNÓSTICO DE CONTROLADORES ===")
    
    # Crear un RaceController
    print("1. Creando RaceController...")
    race_controller = RaceController(max_laps=10)
    print(f"   Tipo: {type(race_controller)}")
    print(f"   Tiene get_race_status: {hasattr(race_controller, 'get_race_status')}")
    print(f"   Tiene led_controller: {hasattr(race_controller, 'led_controller')}")
    
    # Crear un LEDController
    print("\n2. Creando LEDController...")
    led_controller = LEDController(0)  # Pin 0
    print(f"   Tipo: {type(led_controller)}")
    print(f"   Tiene get_race_status: {hasattr(led_controller, 'get_race_status')}")
    print(f"   Tiene led_controller: {hasattr(led_controller, 'led_controller')}")
    
    # Verificar qué pasa si pasamos LEDController al WebServer
    print("\n3. Probando WebServer con LEDController...")
    try:
        web_server_wrong = WebServer("127.0.0.1", 8080, led_controller)
        print("   ERROR: Se creó WebServer con LEDController (esto no debería pasar)")
    except Exception as e:
        print(f"   OK: Error esperado: {e}")
    
    # Verificar qué pasa si pasamos RaceController al WebServer
    print("\n4. Probando WebServer con RaceController...")
    try:
        web_server_correct = WebServer("127.0.0.1", 8080, race_controller)
        print("   OK: WebServer creado correctamente con RaceController")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n=== FIN DEL DIAGNÓSTICO ===")

if __name__ == "__main__":
    debug_controller() 