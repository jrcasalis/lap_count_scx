"""
Ejemplo de prueba para el display MAX7219
Este script prueba la funcionalidad básica del display
"""

import sys
import os

# Agregar el directorio src al path para poder importar los módulos
sys.path.append('/src')

from max7219_display import MAX7219Display
import time

def test_display():
    """Prueba el display MAX7219"""
    print("Iniciando prueba del display MAX7219...")
    
    # Inicializar display
    display = MAX7219Display()
    
    try:
        print("Mostrando letra 'R'...")
        display.display_letter('R')
        time.sleep(3)
        
        print("Mostrando letra 'N'...")
        display.display_letter('N')
        time.sleep(3)
        
        print("Limpiando display...")
        display.clear_display()
        time.sleep(1)
        
        print("Prueba completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
    finally:
        display.cleanup()

if __name__ == "__main__":
    test_display() 