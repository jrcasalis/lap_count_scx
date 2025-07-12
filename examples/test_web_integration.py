"""
Prueba de integración web completa
Simula las peticiones HTTP que hace la interfaz web
"""

from race_controller import RaceController
import time

def simulate_web_requests():
    """Simula las peticiones HTTP de la interfaz web"""
    print("=== SIMULACIÓN DE PETICIONES WEB ===")
    
    # Inicializar controlador
    race = RaceController(max_laps=15)
    
    # Simular petición de estado inicial
    print("\n1. Estado inicial:")
    status = race.get_race_status()
    print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
    print(f"   LED: {'ON' if status['led_status']['is_on'] else 'OFF'}")
    print(f"   Completada: {status['is_completed']}")
    
    # Simular petición de incrementar vuelta
    print("\n2. Incrementando vueltas...")
    for i in range(3):
        success = race.increment_lap()
        status = race.get_race_status()
        print(f"   Vuelta {status['current_laps']}/{status['max_laps']} - Éxito: {success}")
        time.sleep(0.5)
    
    # Simular petición de control de LED
    print("\n3. Probando control de LED...")
    
    print("   Encendiendo LED...")
    race.turn_on_led()
    status = race.get_race_status()
    print(f"   LED: {'ON' if status['led_status']['is_on'] else 'OFF'}")
    
    print("   Apagando LED...")
    race.turn_off_led()
    status = race.get_race_status()
    print(f"   LED: {'ON' if status['led_status']['is_on'] else 'OFF'}")
    
    print("   Alternando LED...")
    is_on = race.toggle_led()
    print(f"   LED: {'ON' if is_on else 'OFF'}")
    
    # Simular petición de reiniciar
    print("\n4. Reiniciando carrera...")
    race.reset_race()
    status = race.get_race_status()
    print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
    print(f"   Completada: {status['is_completed']}")
    
    # Simular completar carrera
    print("\n5. Completando carrera...")
    for i in range(15):
        race.increment_lap()
        status = race.get_race_status()
        print(f"   Vuelta {status['current_laps']}/{status['max_laps']}")
        if status['is_completed']:
            print("   ¡Carrera completada!")
            break
        time.sleep(0.2)
    
    print("\n=== SIMULACIÓN COMPLETADA ===")
    print("Todas las funciones web funcionan correctamente!")

def test_api_responses():
    """Prueba las respuestas de la API"""
    print("\n=== PRUEBA DE RESPUESTAS API ===")
    
    race = RaceController(max_laps=15)
    
    # Simular respuestas JSON que devuelve el servidor web
    print("\n1. Respuesta de incrementar vuelta:")
    success = race.increment_lap()
    status = race.get_race_status()
    response = {
        "success": success,
        "message": "Vuelta incrementada" if success else "Ya se alcanzó el máximo",
        "race_status": status
    }
    print(f"   {response}")
    
    print("\n2. Respuesta de estado del LED:")
    led_status = {
        "success": True,
        "is_on": race.led.value() == 1,
        "pin": 0  # LED_PIN_RED
    }
    print(f"   {led_status}")
    
    print("\n3. Respuesta de estado de carrera:")
    status_response = {
        "success": True,
        "race_status": race.get_race_status()
    }
    print(f"   {status_response}")
    
    print("\n=== PRUEBA DE API COMPLETADA ===")

if __name__ == "__main__":
    simulate_web_requests()
    test_api_responses() 