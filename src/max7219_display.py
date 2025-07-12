"""
Controlador para display MAX7219
Maneja la comunicación SPI con el display de 8x8 LEDs
"""

from machine import Pin, SPI
import time

class MAX7219Display:
    def __init__(self, din_pin=2, cs_pin=3, clk_pin=4):
        """
        Inicializa el display MAX7219
        
        Args:
            din_pin (int): Pin de datos (GP2)
            cs_pin (int): Pin de chip select (GP3)
            clk_pin (int): Pin de reloj (GP4)
        """
        self.din_pin = din_pin
        self.cs_pin = cs_pin
        self.clk_pin = clk_pin
        
        # Configuración SPI robusta para Pico 2W
        try:
            # Intentar SPI(1) primero
            self.spi = SPI(1, baudrate=1000000, polarity=0, phase=0, 
                          sck=Pin(clk_pin), mosi=Pin(din_pin))
            print("SPI(1) configurado exitosamente")
        except:
            try:
                # Intentar SPI(0) como alternativa
                self.spi = SPI(0, baudrate=1000000, polarity=0, phase=0, 
                              sck=Pin(clk_pin), mosi=Pin(din_pin))
                print("SPI(0) configurado exitosamente")
            except Exception as e:
                print(f"Error configurando SPI: {e}")
                # Configuración manual de pines como último recurso
                self.spi = None
                self.din = Pin(din_pin, Pin.OUT)
                self.clk = Pin(clk_pin, Pin.OUT)
                print("Usando configuración manual de pines")
        
        self.cs = Pin(cs_pin, Pin.OUT)
        
        # Inicializar display
        self.init_display()
        
    def init_display(self):
        """Inicializa el display MAX7219"""
        # Apagar modo de prueba
        self.write_register(0x0F, 0x00)
        # Establecer intensidad (0-15)
        self.write_register(0x0A, 0x08)
        # Establecer modo de escaneo (todas las filas)
        self.write_register(0x0B, 0x07)
        # Establecer modo de operación normal
        self.write_register(0x0C, 0x01)
        # Limpiar display
        self.clear_display()
        
    def write_register_manual(self, address, data):
        """Escribe un registro usando pines manuales"""
        self.cs.value(0)  # Activar CS
        
        # Enviar dirección (8 bits)
        for i in range(8):
            self.clk.value(0)
            self.din.value((address >> (7-i)) & 1)
            self.clk.value(1)
        
        # Enviar datos (8 bits)
        for i in range(8):
            self.clk.value(0)
            self.din.value((data >> (7-i)) & 1)
            self.clk.value(1)
        
        self.cs.value(1)  # Desactivar CS
        
    def write_register(self, address, data):
        """Escribe un byte a un registro específico"""
        self.cs.value(0)  # Activar CS
        
        if self.spi:
            # Usar SPI si está disponible
            self.spi.write(bytes([address, data]))
        else:
            # Usar configuración manual
            self.write_register_manual(address, data)
        
        self.cs.value(1)  # Desactivar CS
        
    def clear_display(self):
        """Limpia todo el display"""
        for i in range(1, 9):
            self.write_register(i, 0x00)
            
    def display_letter(self, letter):
        """Muestra una letra en el display"""
        # Definir patrones para las letras R y N
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
            # Si la letra no está definida, limpiar display
            self.clear_display()
            
    def cleanup(self):
        """Limpia los recursos del display"""
        self.clear_display()
        print("MAX7219 display cleanup completado") 