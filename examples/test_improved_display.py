from max7219_dual_display import MAX7219DualDisplay
import time

def main():
    display = MAX7219DualDisplay(din_pin=3, cs_pin=5, clk_pin=2, num_modules=2)
    
    print("Prueba mejorada del display...")
    
    # Limpiar todo
    display.clear()
    time.sleep(1)
    
    # Prueba 1: Ambos módulos con el mismo patrón
    print("Ambos módulos con patrón completo...")
    for row in range(1, 9):
        # Enviar a ambos módulos con el mismo patrón
        display.write_register_all(row, 0xFF)
        time.sleep(0.1)  # Pausa entre filas
    
    time.sleep(2)
    
    # Limpiar
    display.clear()
    time.sleep(1)
    
    # Prueba 2: Patrones diferentes pero estables
    print("Patrones diferentes estables...")
    for i in range(5):
        # Módulo 0: patrón de puntos
        for row in range(1, 9):
            display.write_register_module(0, row, 0xAA)
        
        # Módulo 1: patrón inverso
        for row in range(1, 9):
            display.write_register_module(1, row, 0x55)
        
        time.sleep(1)
        
        # Invertir patrones
        for row in range(1, 9):
            display.write_register_module(0, row, 0x55)
        
        for row in range(1, 9):
            display.write_register_module(1, row, 0xAA)
        
        time.sleep(1)
    
    # Limpiar
    display.clear()
    print("Prueba completada!")

if __name__ == "__main__":
    main() 