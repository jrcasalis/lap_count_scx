from max7219_dual_display import MAX7219DualDisplay
import time

def main():
    display = MAX7219DualDisplay(din_pin=3, cs_pin=5, clk_pin=2, num_modules=2)
    
    print("Prueba de cambio de patrones...")
    
    # Limpiar todo
    display.clear()
    time.sleep(1)
    
    # Prueba 1: Ambos módulos con el mismo patrón (debería funcionar)
    print("Ambos módulos con patrón completo...")
    for row in range(1, 9):
        display.write_register_all(row, 0xFF)
    time.sleep(2)
    
    # Limpiar
    display.clear()
    time.sleep(1)
    
    # Prueba 2: Cambio de patrones individuales
    print("Cambio de patrones individuales...")
    
    # Ciclo 1: Módulo 0 lleno, módulo 1 vacío
    print("Ciclo 1: Módulo 0 lleno, módulo 1 vacío")
    for row in range(1, 9):
        display.write_register_module(0, row, 0xFF)
        display.write_register_module(1, row, 0x00)
    time.sleep(2)
    
    # Ciclo 2: Módulo 0 vacío, módulo 1 lleno
    print("Ciclo 2: Módulo 0 vacío, módulo 1 lleno")
    for row in range(1, 9):
        display.write_register_module(0, row, 0x00)
        display.write_register_module(1, row, 0xFF)
    time.sleep(2)
    
    # Ciclo 3: Patrones alternados
    print("Ciclo 3: Patrones alternados")
    for row in range(1, 9):
        if row % 2 == 0:
            display.write_register_module(0, row, 0xAA)
            display.write_register_module(1, row, 0x55)
        else:
            display.write_register_module(0, row, 0x55)
            display.write_register_module(1, row, 0xAA)
    time.sleep(2)
    
    # Limpiar
    display.clear()
    print("Prueba completada!")

if __name__ == "__main__":
    main() 