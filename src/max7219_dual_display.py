import time
from machine import Pin, SPI

class MAX7219DualDisplay:
    def __init__(self, din_pin=3, cs_pin=5, clk_pin=2, num_modules=2):
        self.num_modules = num_modules
        self.cs = Pin(cs_pin, Pin.OUT)
        # SPI0 estándar: CLK=GPIO2, DIN=GPIO3, CS=GPIO5
        self.spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(clk_pin), mosi=Pin(din_pin))
        self.init_display()

    def write_register_all(self, address, data):
        self.cs.value(0)
        # En cascada: enviar datos en orden inverso (módulo más lejano primero)
        for _ in range(self.num_modules):
            self.spi.write(bytearray([address, data]))
        self.cs.value(1)

    def write_register_module(self, module_index, address, data):
        self.cs.value(0)
        # En cascada: enviar datos en orden inverso (módulo más lejano primero)
        # Módulo 0 = más alejado de DIN, módulo 1 = más cercano a DIN
        for i in range(self.num_modules - 1, -1, -1):  # Enviar en orden inverso
            if i == module_index:
                self.spi.write(bytearray([address, data]))
            else:
                # Enviar comando NO-OP (0x00, 0x00) para mantener el estado
                self.spi.write(bytearray([0x00, 0x00]))
        self.cs.value(1)
        # Pequeña pausa para estabilizar la comunicación
        for _ in range(10):  # Delay mínimo
            pass

    def init_display(self):
        for address, data in [
            (0x09, 0x00),  # Decoding: off
            (0x0A, 0x08),  # Brightness: mid
            (0x0B, 0x07),  # Scan limit: 8 LEDs
            (0x0C, 0x01),  # Shutdown: normal operation
            (0x0F, 0x00),  # Display test: off
        ]:
            self.write_register_all(address, data)
        self.clear()

    def clear(self):
        for i in range(1, 9):
            self.write_register_all(i, 0x00)

    # Tabla de patrones para los dígitos 0-9 (8x8)
    DIGITS = {
        '0': [0b00111100,0b01100110,0b11000011,0b11000011,0b11000011,0b11000011,0b01100110,0b00111100],
        '1': [0b00011000,0b00111000,0b00011000,0b00011000,0b00011000,0b00011000,0b00011000,0b01111110],
        '2': [0b00111100,0b01100110,0b00000110,0b00001100,0b00011000,0b00110000,0b01100000,0b01111110],
        '3': [0b00111100,0b01100110,0b00000110,0b00011100,0b00000110,0b00000110,0b01100110,0b00111100],
        '4': [0b00001100,0b00011100,0b00111100,0b01101100,0b01111110,0b00001100,0b00001100,0b00001100],
        '5': [0b01111110,0b01100000,0b01100000,0b01111100,0b00000110,0b00000110,0b01100110,0b00111100],
        '6': [0b00111100,0b01100110,0b01100000,0b01111100,0b01100110,0b01100110,0b01100110,0b00111100],
        '7': [0b01111110,0b00000110,0b00001100,0b00011000,0b00110000,0b00110000,0b00110000,0b00110000],
        '8': [0b00111100,0b01100110,0b01100110,0b00111100,0b01100110,0b01100110,0b01100110,0b00111100],
        '9': [0b00111100,0b01100110,0b01100110,0b00111110,0b00000110,0b00000110,0b01100110,0b00111100],
    }

    def show_two_digits(self, value):
        """Muestra un número de dos dígitos (00-99) en el display de 8x16"""
        s = str(value)
        if len(s) == 1:
            s = "0" + s
        left = self.DIGITS.get(s[0], [0]*8)
        right = self.DIGITS.get(s[1], [0]*8)
        for row in range(8):
            self.write_register_module(0, row+1, left[row])
            self.write_register_module(1, row+1, right[row]) 