"""
Ejemplo: Test de scroll con casco real y velocidad configurable
Prueba la nueva funcionalidad de scroll con patrón de casco real
"""

import time
from race_controller import RaceController
from config import *

def test_helmet_scroll_fixed():
    """Prueba el scroll con casco real y velocidad configurable"""
    print("=== Test de Scroll con Casco Real ===")
    
    # Crear controlador
    controller = RaceController(max_laps=10)
    
    # Nombres de prueba
    test_names = [
        "Juan",
        "Maria",
        "Carlos",
        "Ana",
        "Pedro"
    ]
    
    # Velocidades de prueba
    test_speeds = [0.1, 0.2, 0.3, 0.5]
    
    print("Probando diferentes velocidades de scroll:")
    for speed in test_speeds:
        print(f"\n--- Velocidad: {speed}s ---")
        controller.set_scroll_speed(speed)
        
        for name in test_names:
            print(f"Probando nombre: {name}")
            
            # Cambiar nombre (esto automáticamente mostrará el scroll)
            success = controller.set_racer_name(name)
            
            if success:
                print(f"✅ Nombre guardado: {name}")
                print(f"📺 Scroll mostrado con velocidad: {speed}s")
                
                # Esperar un poco antes del siguiente nombre
                time.sleep(1)
            else:
                print(f"❌ Error al guardar nombre: {name}")
    
    # Probar velocidad actual
    current_speed = controller.get_scroll_speed()
    print(f"\nVelocidad actual configurada: {current_speed}s")
    
    print("\n=== Test completado ===")
    controller.cleanup()

if __name__ == "__main__":
    test_helmet_scroll_fixed() 