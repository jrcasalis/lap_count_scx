from max7219_dual_display import MAX7219DualDisplay
import time

def main():
    display = MAX7219DualDisplay(din_pin=3, cs_pin=5, clk_pin=2, num_modules=2)
    
    print("Diagnóstico de módulos MAX7219...")
    
    # Limpiar todo
    display.clear()
    time.sleep(1)
    
    # Prueba 1: Encender solo el módulo 0 (izquierda)
    print("Prueba módulo 0 (izquierda)...")
    for row in range(1, 9):
        display.write_register_module(0, row, 0xFF)  # Todas las LEDs encendidas
    time.sleep(3)
    
    # Limpiar
    display.clear()
    time.sleep(1)
    
    # Prueba 2: Encender solo el módulo 1 (derecha)
    print("Prueba módulo 1 (derecha)...")
    for row in range(1, 9):
        display.write_register_module(1, row, 0xFF)  # Todas las LEDs encendidas
    time.sleep(3)
    
    # Limpiar
    display.clear()
    time.sleep(1)
    
    # Prueba 3: Patrón alternado
    print("Patrón alternado...")
    for i in range(10):
        # Módulo 0: patrón de rayas
        for row in range(1, 9):
            if row % 2 == 0:
                display.write_register_module(0, row, 0xAA)
            else:
                display.write_register_module(0, row, 0x55)
        
        # Módulo 1: patrón inverso
        for row in range(1, 9):
            if row % 2 == 0:
                display.write_register_module(1, row, 0x55)
            else:
                display.write_register_module(1, row, 0xAA)
        
        time.sleep(0.5)
    
    # Limpiar
    display.clear()
    print("Diagnóstico completado!")

if __name__ == "__main__":
    main() 