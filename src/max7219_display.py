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
        # Definir patrones para las letras y números
        patterns = {
            'R': [
                0b11111111,  # Fila 1: ████████
                0b10000001,  # Fila 2: █     █
                0b10000001,  # Fila 3: █     █
                0b11111111,  # Fila 4: ████████
                0b10001000,  # Fila 5: █   █
                0b10000100,  # Fila 6: █    █
                0b10000010,  # Fila 7: █     █
                0b10000001   # Fila 8: █      █
            ],
            'O': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b11000011,  # Fila 3: ██    ██
                0b11000011,  # Fila 4: ██    ██
                0b11000011,  # Fila 5: ██    ██
                0b11000011,  # Fila 6: ██    ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            'J': [
                0b00000011,  # Fila 1:       ██
                0b00000011,  # Fila 2:       ██
                0b00000011,  # Fila 3:       ██
                0b00000011,  # Fila 4:       ██
                0b11000011,  # Fila 5: ██    ██
                0b11000011,  # Fila 6: ██    ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            'N': [
                0b10000001,  # Fila 1: █      █
                0b11000001,  # Fila 2: ██     █
                0b10100001,  # Fila 3: █ █    █
                0b10010001,  # Fila 4: █  █   █
                0b10001001,  # Fila 5: █   █  █
                0b10000101,  # Fila 6: █    █ █
                0b10000011,  # Fila 7: █     ██
                0b10000001   # Fila 8: █      █
            ],
            'F': [
                0b11111111,  # Fila 1: ████████
                0b11000000,  # Fila 2: ██
                0b11000000,  # Fila 3: ██
                0b11111100,  # Fila 4: ██████
                0b11000000,  # Fila 5: ██
                0b11000000,  # Fila 6: ██
                0b11000000,  # Fila 7: ██
                0b11000000   # Fila 8: ██
            ],
            'I': [
                0b01111110,  # Fila 1:  ██████
                0b00011000,  # Fila 2:    ██
                0b00011000,  # Fila 3:    ██
                0b00011000,  # Fila 4:    ██
                0b00011000,  # Fila 5:    ██
                0b00011000,  # Fila 6:    ██
                0b00011000,  # Fila 7:    ██
                0b01111110   # Fila 8:  ██████
            ],
            '/': [
                0b00000011,  # Fila 1:       ██
                0b00000110,  # Fila 2:      ██
                0b00001100,  # Fila 3:     ██
                0b00011000,  # Fila 4:    ██
                0b00110000,  # Fila 5:   ██
                0b01100000,  # Fila 6:  ██
                0b11000000,  # Fila 7: ██
                0b10000000   # Fila 8: █
            ],
            # Números del 0 al 9
            '0': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b11000011,  # Fila 3: ██    ██
                0b11000011,  # Fila 4: ██    ██
                0b11000011,  # Fila 5: ██    ██
                0b11000011,  # Fila 6: ██    ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            '1': [
                0b00011000,  # Fila 1:    ██
                0b00111000,  # Fila 2:   ███
                0b00011000,  # Fila 3:    ██
                0b00011000,  # Fila 4:    ██
                0b00011000,  # Fila 5:    ██
                0b00011000,  # Fila 6:    ██
                0b00011000,  # Fila 7:    ██
                0b01111110   # Fila 8:  ██████
            ],
            '2': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b00000110,  # Fila 3:      ██
                0b00001100,  # Fila 4:     ██
                0b00011000,  # Fila 5:    ██
                0b00110000,  # Fila 6:   ██
                0b01100000,  # Fila 7:  ██
                0b01111110   # Fila 8:  ██████
            ],
            '3': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b00000110,  # Fila 3:      ██
                0b00111100,  # Fila 4:   ████
                0b00000110,  # Fila 5:      ██
                0b00000110,  # Fila 6:      ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            '4': [
                0b00001100,  # Fila 1:     ██
                0b00011100,  # Fila 2:    ███
                0b00111100,  # Fila 3:   ████
                0b01101100,  # Fila 4:  ██ ██
                0b01111110,  # Fila 5:  ██████
                0b00001100,  # Fila 6:     ██
                0b00001100,  # Fila 7:     ██
                0b00001100   # Fila 8:     ██
            ],
            '5': [
                0b01111110,  # Fila 1:  ██████
                0b01100000,  # Fila 2:  ██
                0b01100000,  # Fila 3:  ██
                0b01111100,  # Fila 4:  ██████
                0b00000110,  # Fila 5:      ██
                0b00000110,  # Fila 6:      ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            '6': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b01100000,  # Fila 3:  ██
                0b01111100,  # Fila 4:  ██████
                0b01100110,  # Fila 5:  ██  ██
                0b01100110,  # Fila 6:  ██  ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            '7': [
                0b01111110,  # Fila 1:  ██████
                0b00000110,  # Fila 2:      ██
                0b00001100,  # Fila 3:     ██
                0b00011000,  # Fila 4:    ██
                0b00110000,  # Fila 5:   ██
                0b01100000,  # Fila 6:  ██
                0b01100000,  # Fila 7:  ██
                0b01100000   # Fila 8:  ██
            ],
            '8': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b01100110,  # Fila 3:  ██  ██
                0b00111100,  # Fila 4:   ████
                0b01100110,  # Fila 5:  ██  ██
                0b01100110,  # Fila 6:  ██  ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ],
            '9': [
                0b00111100,  # Fila 1:   ████
                0b01100110,  # Fila 2:  ██  ██
                0b01100110,  # Fila 3:  ██  ██
                0b00111110,  # Fila 4:   ██████
                0b00000110,  # Fila 5:      ██
                0b00000110,  # Fila 6:      ██
                0b01100110,  # Fila 7:  ██  ██
                0b00111100   # Fila 8:   ████
            ]
        }
        
        if letter in patterns:
            pattern = patterns[letter]
            for i, row in enumerate(pattern, 1):
                self.write_register(i, row)
        else:
            # Si la letra no está definida, limpiar display
            self.clear_display()
    
    def scroll_text(self, text, delay=0.3):
        """Desplaza texto por el display"""
        # Definir patrones para todas las letras y números
        patterns = {
            'R': [
                0b11111111, 0b10000001, 0b10000001, 0b11111111,
                0b10001000, 0b10000100, 0b10000010, 0b10000001
            ],
            'O': [
                0b00111100, 0b01100110, 0b11000011, 0b11000011,
                0b11000011, 0b11000011, 0b01100110, 0b00111100
            ],
            'J': [
                0b00000011, 0b00000011, 0b00000011, 0b00000011,
                0b11000011, 0b11000011, 0b01100110, 0b00111100
            ],
            'N': [
                0b10000001, 0b11000001, 0b10100001, 0b10010001,
                0b10001001, 0b10000101, 0b10000011, 0b10000001
            ],
            'F': [
                0b11111111, 0b11000000, 0b11000000, 0b11111100,
                0b11000000, 0b11000000, 0b11000000, 0b11000000
            ],
            'I': [
                0b01111110, 0b00011000, 0b00011000, 0b00011000,
                0b00011000, 0b00011000, 0b00011000, 0b01111110
            ],
            # Números del 0 al 9
            '0': [
                0b00111100, 0b01100110, 0b11000011, 0b11000011,
                0b11000011, 0b11000011, 0b01100110, 0b00111100
            ],
            '1': [
                0b00011000, 0b00111000, 0b00011000, 0b00011000,
                0b00011000, 0b00011000, 0b00011000, 0b01111110
            ],
            '2': [
                0b00111100, 0b01100110, 0b00000110, 0b00001100,
                0b00011000, 0b00110000, 0b01100000, 0b01111110
            ],
            '3': [
                0b00111100, 0b01100110, 0b00000110, 0b00111100,
                0b00000110, 0b00000110, 0b01100110, 0b00111100
            ],
            '4': [
                0b00001100, 0b00011100, 0b00111100, 0b01101100,
                0b01111110, 0b00001100, 0b00001100, 0b00001100
            ],
            '5': [
                0b01111110, 0b01100000, 0b01100000, 0b01111100,
                0b00000110, 0b00000110, 0b01100110, 0b00111100
            ],
            '6': [
                0b00111100, 0b01100110, 0b01100000, 0b01111100,
                0b01100110, 0b01100110, 0b01100110, 0b00111100
            ],
            '7': [
                0b01111110, 0b00000110, 0b00001100, 0b00011000,
                0b00110000, 0b01100000, 0b01100000, 0b01100000
            ],
            '8': [
                0b00111100, 0b01100110, 0b01100110, 0b00111100,
                0b01100110, 0b01100110, 0b01100110, 0b00111100
            ],
            '9': [
                0b00111100, 0b01100110, 0b01100110, 0b00111110,
                0b00000110, 0b00000110, 0b01100110, 0b00111100
            ]
        }
        
        # Convertir texto a patrones
        text_patterns = []
        for letter in text.upper():
            if letter in patterns:
                text_patterns.append(patterns[letter])
        
        if not text_patterns:
            return
        
        # Crear matriz completa del texto
        full_text = []
        for letter_pattern in text_patterns:
            full_text.extend(letter_pattern)
        
        # Agregar espacios al final para que el texto salga completamente
        full_text.extend([0] * 8)  # 8 filas de espacios
        
        # Desplazar el texto
        for start_pos in range(len(full_text) - 7):  # -7 para mostrar solo 8 filas
            # Obtener 8 filas para mostrar
            display_rows = full_text[start_pos:start_pos + 8]
            
            # Mostrar en el display
            for i, row in enumerate(display_rows, 1):
                self.write_register(i, row)
            
            time.sleep(delay)
        
        # Limpiar display al final
        self.clear_display()
            
    def cleanup(self):
        """Limpia los recursos del display"""
        self.clear_display()
        print("MAX7219 display cleanup completado") 

    def set_brightness(self, value):
        """Cambia el brillo del display (0-15)"""
        self.write_register(0x0A, value)

    def show_checkered_flag(self, blink_time=10, blink_interval=0.5, brightness=8, keep_on=True):
        """
        Muestra una bandera a cuadros 2x2 titilando durante blink_time segundos, luego la deja fija si keep_on.
        Args:
            blink_time (float): Duración total del parpadeo en segundos
            blink_interval (float): Intervalo de parpadeo en segundos
            brightness (int): Nivel de brillo durante la bandera
            keep_on (bool): Si True, deja la bandera fija al final
        """
        # Patrón de bandera a cuadros 2x2
        pattern1 = [
            0b11001100,
            0b11001100,
            0b00110011,
            0b00110011,
            0b11001100,
            0b11001100,
            0b00110011,
            0b00110011
        ]
        pattern2 = [
            0b00110011,
            0b00110011,
            0b11001100,
            0b11001100,
            0b00110011,
            0b00110011,
            0b11001100,
            0b11001100
        ]
        self.set_brightness(brightness)
        import time
        t_end = time.time() + blink_time
        toggle = True
        while time.time() < t_end:
            pat = pattern1 if toggle else pattern2
            for i, row in enumerate(pat, 1):
                self.write_register(i, row)
            toggle = not toggle
            time.sleep(blink_interval)
        # Dejar bandera fija si se pide
        if keep_on:
            for i, row in enumerate(pattern1, 1):
                self.write_register(i, row) 