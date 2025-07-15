"""
Ejemplo para probar el sistema completo con semáforo integrado
"""

import time
from machine import Pin
from src.race_controller import RaceController
from src.web_server import WebServer
import network
import gc

def test_complete_system():
    """Prueba el sistema completo con semáforo"""
    print("=== SISTEMA COMPLETO CON SEMÁFORO ===")
    print("Iniciando controlador de carrera...")
    
    try:
        # Crear controlador de carrera
        race_controller = RaceController()
        
        # Crear servidor web
        web_server = WebServer("0.0.0.0", 8080, race_controller)
        
        print("✓ Sistema iniciado correctamente")
        print("✓ Servidor web en puerto 8080")
        print("✓ Semáforo integrado")
        print()
        
        # Probar funciones del semáforo
        print("--- PRUEBA DEL SEMÁFORO ---")
        
        print("1. Iniciando previa (titileo)...")
        success = race_controller.race_previous()
        print(f"   Resultado: {'✓' if success else '✗'}")
        time.sleep(3)
        
        print("2. Parando previa...")
        success = race_controller.race_previous_stop()
        print(f"   Resultado: {'✓' if success else '✗'}")
        time.sleep(2)
        
        print("3. Largando carrera...")
        success = race_controller.race_start()
        print(f"   Resultado: {'✓' if success else '✗'}")
        time.sleep(8)  # Esperar a que termine la secuencia
        
        print("4. Parando carrera...")
        success = race_controller.race_stop()
        print(f"   Resultado: {'✓' if success else '✗'}")
        
        print("\n--- ESTADO DEL SEMÁFORO ---")
        status = race_controller.get_traffic_light_status()
        print(f"Estado: {status['state']}")
        print(f"Rojo: {'ON' if status['red_on'] else 'OFF'}")
        print(f"Amarillo: {'ON' if status['yellow_on'] else 'OFF'}")
        print(f"Verde: {'ON' if status['green_on'] else 'OFF'}")
        print(f"Titileando: {'SÍ' if status['blinking_active'] else 'NO'}")
        
        print("\n=== SISTEMA LISTO ===")
        print("Accede a la interfaz web desde tu navegador:")
        print("http://[IP_DEL_PICO]:8080")
        print()
        print("Funciones disponibles en la web:")
        print("- Contador de vueltas")
        print("- Control del piloto")
        print("- 🚦 Control del semáforo:")
        print("  • Iniciar Previa (titileo)")
        print("  • Parar Previa")
        print("  • Largar Carrera (secuencia)")
        print("  • Parar Carrera")
        
    except Exception as e:
        print(f"Error iniciando sistema: {e}")

if __name__ == "__main__":
    test_complete_system() 