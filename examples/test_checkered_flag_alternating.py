"""
Ejemplo: Prueba de animación de bandera a cuadros con alternancia de patrones
Muestra cómo la animación ahora alterna entre dos patrones complementarios
en lugar de encender y apagar completamente el display
"""

import time
from src.race_controller import RaceController
from src.config import *

def test_checkered_flag_alternating():
    """Prueba la animación de bandera a cuadros con alternancia de patrones"""
    print("=== PRUEBA: Animación de Bandera a Cuadros con Alternancia ===")
    print("Configuración:")
    print(f"- Duración: {FLAG_ANIMATION_DURATION} segundos")
    print(f"- Intervalo: {CHECKERED_FLAG_BLINK_INTERVAL} segundos")
    print(f"- Animación: {DEFAULT_COMPLETION_ANIMATION}")
    print()
    
    # Crear controlador de carrera
    controller = RaceController(max_laps=5)
    
    print("Iniciando animación de bandera a cuadros...")
    print("Observa cómo alterna entre dos patrones complementarios")
    print("en lugar de apagar completamente el display.")
    print()
    
    # Mostrar animación de bandera a cuadros
    controller.show_flag_animation("checkered_flag")
    
    print("Animación completada.")
    print("El display ahora alterna entre:")
    print("- Patrón 1: Cuadros 2x2 en posiciones principales")
    print("- Patrón 2: Cuadros 2x2 en posiciones complementarias")
    print("Esto mantiene el display siempre activo durante la animación.")
    
    # Limpiar
    controller.cleanup()

if __name__ == "__main__":
    test_checkered_flag_alternating() 