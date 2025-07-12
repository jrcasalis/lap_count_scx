"""
Ejemplo: Test de nombres largos con scroll mejorado
Prueba la funcionalidad de scroll con nombres largos como "MANGUILA"
"""

import time
from race_controller import RaceController
from config import *

def test_long_names_scroll():
    """Prueba el scroll con nombres largos"""
    print("=== Test de Nombres Largos con Scroll Mejorado ===")
    
    # Crear controlador
    controller = RaceController(max_laps=10)
    
    # Nombres largos de prueba
    long_names = [
        "MANGUILA",
        "SUPERPILOTO",
        "CAMPEON",
        "VELOCIDAD",
        "CARRERA"
    ]
    
    print("Probando nombres largos:")
    for name in long_names:
        print(f"\n--- Probando nombre: {name} ---")
        print(f"Longitud: {len(name)} caracteres")
        
        # Cambiar nombre (esto automáticamente mostrará el scroll)
        success = controller.set_racer_name(name)
        
        if success:
            print(f"✅ Nombre guardado: {name}")
            print("📺 Scroll mostrado en display (debería mostrar todo el nombre)")
            
            # Esperar un poco antes del siguiente nombre
            time.sleep(2)
        else:
            print(f"❌ Error al guardar nombre: {name}")
    
    # Probar con nombre muy largo
    very_long_name = "SUPERVELOCIDADMAXIMA"
    print(f"\n--- Probando nombre muy largo: {very_long_name} ---")
    print(f"Longitud: {len(very_long_name)} caracteres")
    
    success = controller.set_racer_name(very_long_name)
    if success:
        print(f"✅ Nombre muy largo guardado: {very_long_name}")
        print("📺 Scroll mostrado en display (debería mostrar todo el nombre)")
    else:
        print(f"❌ Error al guardar nombre muy largo: {very_long_name}")
    
    # Probar velocidad actual
    current_speed = controller.get_scroll_speed()
    print(f"\nVelocidad actual configurada: {current_speed}s")
    
    print("\n=== Test completado ===")
    print("Verifica que:")
    print("1. Se muestre todo el nombre completo")
    print("2. El scroll sea fluido y suave")
    print("3. El casco aparezca como patrón real")
    print("4. La velocidad sea apropiada")
    
    controller.cleanup()

if __name__ == "__main__":
    test_long_names_scroll() 