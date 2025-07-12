from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
import time

def main():
    print("Prueba del display configurable...")
    
    # Configuración básica
    display = MAX7219DualDisplayConfigurable(
        din_pin=3, 
        cs_pin=5, 
        clk_pin=2, 
        num_modules=2,
        brightness=8,  # Brillo medio
        rotation=0,    # Sin rotación
        orientation='horizontal'  # Orientación horizontal
    )
    
    # Prueba 1: Configuración por defecto
    print("1. Configuración por defecto (horizontal, sin rotación)")
    for i in range(5):
        display.show_two_digits(i)
        time.sleep(1)
    
    # Prueba 2: Diferentes niveles de brillo
    print("2. Prueba de brillo")
    for brightness in [1, 4, 8, 12, 15]:
        print(f"Brillo: {brightness}")
        display.set_brightness(brightness)
        display.show_two_digits(42)
        time.sleep(1)
    
    # Prueba 3: Diferentes rotaciones
    print("3. Prueba de rotaciones")
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
    for i in range(5):
        display.show_two_digits(i)
        time.sleep(1)
    
    # Prueba 5: Patrones de prueba
    print("5. Patrones de prueba")
    display.set_orientation('horizontal')
    display.set_rotation(0)
    display.set_brightness(8)
    
    print("Patrón: Todo encendido")
    display.test_pattern('all_on')
    time.sleep(2)
    
    print("Patrón: Tablero de ajedrez")
    display.test_pattern('checkerboard')
    time.sleep(2)
    
    print("Patrón: Todo apagado")
    display.test_pattern('all_off')
    time.sleep(1)
    
    # Prueba 6: Combinación de configuraciones
    print("6. Combinación: Vertical + Rotación 90°")
    display.set_orientation('vertical')
    display.set_rotation(90)
    display.set_brightness(12)
    
    for i in range(3):
        display.show_two_digits(i)
        time.sleep(1)
    
    # Limpiar
    display.clear()
    print("Prueba completada!")

if __name__ == "__main__":
    main() 