from max7219_dual_display import MAX7219DualDisplay
import time

def main():
    # Configuración SPI0 estándar
    display = MAX7219DualDisplay(din_pin=3, cs_pin=5, clk_pin=2, num_modules=2)
    
    print("Iniciando prueba del display...")
    
    # Limpiar display
    display.clear()
    time.sleep(1)
    
    # Prueba 1: Mostrar "00"
    print("Mostrando 00...")
    display.show_two_digits(0)
    time.sleep(2)
    
    # Prueba 2: Mostrar "12"
    print("Mostrando 12...")
    display.show_two_digits(12)
    time.sleep(2)
    
    # Prueba 3: Mostrar "99"
    print("Mostrando 99...")
    display.show_two_digits(99)
    time.sleep(2)
    
    # Prueba 4: Contador rápido
    print("Contador rápido...")
    for i in range(10):
        display.show_two_digits(i)
        time.sleep(0.5)
    
    print("Prueba completada!")

if __name__ == "__main__":
    main() 