import time
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable

# Pines y configuración (ajustar si es necesario)
DIN_PIN = 3
CS_PIN = 5
CLK_PIN = 2
NUM_MODULES = 2
BRIGHTNESS = 8
ORIENTATION = 'horizontal'  # o 'vertical'

rotations = [0, 90, 180, 270]

print("Test de rotación de display MAX7219")

display = MAX7219DualDisplayConfigurable(
    din_pin=DIN_PIN,
    cs_pin=CS_PIN,
    clk_pin=CLK_PIN,
    num_modules=NUM_MODULES,
    brightness=BRIGHTNESS,
    rotation=0,  # Se cambiará en el bucle
    orientation=ORIENTATION
)

for rot in rotations:
    print(f"\nMostrando conteo 1-5 con rotación {rot}°...")
    display.set_rotation(rot)
    for i in range(1, 6):
        display.show_two_digits(i)
        print(f"Mostrando: {i} (rotación {rot}°)")
        time.sleep(2)
    display.clear()
    time.sleep(1)

print("Test finalizado. El display debería haber mostrado los números 1-5 en cada rotación.") 