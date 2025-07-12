from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
import time

def test_horizontal_rotations():
    """Prueba todas las rotaciones en orientación horizontal"""
    print("=== PRUEBA: Orientación Horizontal ===")
    
    display = MAX7219DualDisplayConfigurable(
        din_pin=3, cs_pin=5, clk_pin=2,
        brightness=10, rotation=0, orientation='horizontal'
    )
    
    rotations = [0, 90, 180, 270]
    for rotation in rotations:
        print(f"Rotación: {rotation}°")
        display.set_rotation(rotation)
        display.show_two_digits(12)
        time.sleep(3)
    
    display.clear()

def test_vertical_rotations():
    """Prueba todas las rotaciones en orientación vertical"""
    print("=== PRUEBA: Orientación Vertical ===")
    
    display = MAX7219DualDisplayConfigurable(
        din_pin=3, cs_pin=5, clk_pin=2,
        brightness=10, rotation=0, orientation='vertical'
    )
    
    rotations = [0, 90, 180, 270]
    for rotation in rotations:
        print(f"Rotación: {rotation}°")
        display.set_rotation(rotation)
        display.show_two_digits(34)
        time.sleep(3)
    
    display.clear()

def test_brightness_levels():
    """Prueba diferentes niveles de brillo"""
    print("=== PRUEBA: Niveles de Brillo ===")
    
    display = MAX7219DualDisplayConfigurable(
        din_pin=3, cs_pin=5, clk_pin=2,
        brightness=8, rotation=0, orientation='horizontal'
    )
    
    brightness_levels = [1, 3, 5, 8, 10, 12, 15]
    for brightness in brightness_levels:
        print(f"Brillo: {brightness}")
        display.set_brightness(brightness)
        display.show_two_digits(56)
        time.sleep(2)
    
    display.clear()

def main():
    print("Pruebas de configuración del display MAX7219")
    print("=" * 50)
    
    # Prueba 1: Rotaciones horizontales
    test_horizontal_rotations()
    time.sleep(2)
    
    # Prueba 2: Rotaciones verticales
    test_vertical_rotations()
    time.sleep(2)
    
    # Prueba 3: Niveles de brillo
    test_brightness_levels()
    
    print("Todas las pruebas completadas!")

if __name__ == "__main__":
    main() 