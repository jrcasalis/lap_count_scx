from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
import time

def main():
    print("Prueba simple del display configurable...")
    
    # Configuración básica
    display = MAX7219DualDisplayConfigurable(
        din_pin=3, cs_pin=5, clk_pin=2,
        brightness=8, rotation=0, orientation='horizontal'
    )
    
    # Prueba 1: Números básicos
    print("1. Números básicos")
    for i in range(5):
        display.show_two_digits(i)
        time.sleep(1)
    
    # Prueba 2: Diferentes brillos
    print("2. Diferentes brillos")
    for brightness in [1, 5, 10, 15]:
        print(f"Brillo: {brightness}")
        display.set_brightness(brightness)
        display.show_two_digits(42)
        time.sleep(1)
    
    # Prueba 3: Rotaciones simples
    print("3. Rotaciones")
    rotations = [0, 90, 180, 270]
    for rotation in rotations:
        print(f"Rotación: {rotation}°")
        display.set_rotation(rotation)
        display.show_two_digits(12)
        time.sleep(2)
    
    # Prueba 4: Orientación vertical
    print("4. Orientación vertical")
    display.set_orientation('vertical')
    display.set_rotation(0)
    display.set_brightness(8)
    display.show_two_digits(34)
    time.sleep(3)
    
    # Limpiar
    display.clear()
    print("Prueba completada!")

if __name__ == "__main__":
    main() 