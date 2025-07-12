"""
Test simple para el display MAX7219
Este script debe ejecutarse directamente en la Raspberry Pi Pico
"""

from machine import Pin, SPI
import time

class MAX7219Display:
    def __init__(self, din_pin=2, cs_pin=3, clk_pin=4):
        """Inicializa el display MAX7219"""
        # Configurar SPI con pines específicos para Pico 2W
        self.spi = SPI(1, baudrate=1000000, polarity=0, phase=0, 
                      sck=Pin(clk_pin), mosi=Pin(din_pin))
        self.cs = Pin(cs_pin, Pin.OUT)
        self.init_display()
        
    def init_display(self):
        """Inicializa el display MAX7219"""
        self.write_register(0x0F, 0x00)  # Apagar modo de prueba
        self.write_register(0x0A, 0x08)  # Intensidad media
        self.write_register(0x0B, 0x07)  # Modo de escaneo
        self.write_register(0x0C, 0x01)  # Modo normal
        self.clear_display()
        
    def write_register(self, address, data):
        """Escribe un byte a un registro específico"""
        self.cs.value(0)
        self.spi.write(bytes([address, data]))
        self.cs.value(1)
        
    def clear_display(self):
        """Limpia todo el display"""
        for i in range(1, 9):
            self.write_register(i, 0x00)
            
    def display_letter(self, letter):
        """Muestra una letra en el display"""
        patterns = {
            'R': [
                0b11111111,  # Fila 1
                0b10000001,  # Fila 2
                0b10000001,  # Fila 3
                0b11111111,  # Fila 4
                0b10001000,  # Fila 5
                0b10000100,  # Fila 6
                0b10000010,  # Fila 7
                0b10000001   # Fila 8
            ],
            'N': [
                0b10000001,  # Fila 1
                0b11000001,  # Fila 2
                0b10100001,  # Fila 3
                0b10010001,  # Fila 4
                0b10001001,  # Fila 5
                0b10000101,  # Fila 6
                0b10000011,  # Fila 7
                0b10000001   # Fila 8
            ]
        }
        
        if letter in patterns:
            pattern = patterns[letter]
            for i, row in enumerate(pattern, 1):
                self.write_register(i, row)
        else:
            self.clear_display()
            
    def cleanup(self):
        """Limpia los recursos del display"""
        self.clear_display()
        print("MAX7219 display cleanup completado")

def test_display():
    """Prueba el display MAX7219"""
    print("Iniciando prueba del display MAX7219...")
    
    try:
        # Inicializar display
        display = MAX7219Display()
        print("Display inicializado correctamente")
        
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
        import sys
        sys.print_exception(e)
    finally:
        try:
            display.cleanup()
        except:
            pass

if __name__ == "__main__":
    test_display() 