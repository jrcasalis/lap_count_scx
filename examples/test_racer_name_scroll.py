"""
Ejemplo: Test de scroll del nombre del piloto
Prueba la funcionalidad de mostrar el nombre del piloto con scroll
"""

import time
from race_controller import RaceController
from config import *

def test_racer_name_scroll():
    """Prueba el scroll del nombre del piloto"""
    print("=== Test de Scroll del Nombre del Piloto ===")
    
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
    
    for name in test_names:
        print(f"\n--- Probando nombre: {name} ---")
        
        # Cambiar nombre (esto automáticamente mostrará el scroll)
        success = controller.set_racer_name(name)
        
        if success:
            print(f"✅ Nombre guardado: {name}")
            print("📺 Scroll mostrado en display")
            
            # Esperar un poco antes del siguiente nombre
            time.sleep(2)
        else:
            print(f"❌ Error al guardar nombre: {name}")
    
    # Probar con nombre muy largo
    long_name = "SuperPiloto"
    print(f"\n--- Probando nombre largo: {long_name} ---")
    success = controller.set_racer_name(long_name)
    if success:
        print(f"✅ Nombre largo guardado: {long_name}")
    else:
        print(f"❌ Nombre largo rechazado (correcto)")
    
    # Probar con nombre vacío
    empty_name = ""
    print(f"\n--- Probando nombre vacío ---")
    success = controller.set_racer_name(empty_name)
    if not success:
        print("✅ Nombre vacío rechazado (correcto)")
    else:
        print("❌ Error: nombre vacío aceptado")
    
    print("\n=== Test completado ===")
    controller.cleanup()

if __name__ == "__main__":
    test_racer_name_scroll() 