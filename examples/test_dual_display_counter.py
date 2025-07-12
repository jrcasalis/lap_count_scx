from max7219_dual_display import MAX7219DualDisplay
import time

# Configuración de pines SPI0 estándar
# Cableado: CLK=GPIO2, DIN=GPIO3, CS=GPIO5
DIN_PIN = 3
CS_PIN = 5
CLK_PIN = 2
NUM_MODULES = 2

def main():
    display = MAX7219DualDisplay(din_pin=DIN_PIN, cs_pin=CS_PIN, clk_pin=CLK_PIN, num_modules=NUM_MODULES)
    display.clear()
    print("Contador de 2 dígitos en display 8x16...")
    n = 0
    while True:
        display.show_two_digits(n)
        print(f"Mostrando: {n:02d}")
        n = (n + 1) % 100
        time.sleep(1)

if __name__ == "__main__":
    main() 