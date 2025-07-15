import time
import _thread
from machine import Pin, SPI
from patterns.digits import DIGITS, get_two_digits_pattern
from patterns.various import HELMET
from config import DEBUG_ENABLED, MAX7219_ROTATION

class MAX7219DualDisplayConfigurable:
    def __init__(self, din_pin=3, cs_pin=5, clk_pin=2, num_modules=2, 
                 brightness=8, rotation=MAX7219_ROTATION, orientation='horizontal'):
        """
        Inicializa el display MAX7219 configurable
        
        Args:
            din_pin: Pin para datos (MOSI)
            cs_pin: Pin para chip select
            clk_pin: Pin para reloj (SCK)
            num_modules: Número de módulos en cascada
            brightness: Brillo (0-15)
            rotation: Rotación en grados (0, 90, 180, 270)
            orientation: 'horizontal' o 'vertical'
        """
        # Todos los prints de log y debug han sido comentados para limpiar la consola
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Inicializando display MAX7219 configurable...")
        #     print(f"[MAX7219] Pines: DIN={din_pin}, CS={cs_pin}, CLK={clk_pin}")
        #     print(f"[MAX7219] Configuración: módulos={num_modules}, brillo={brightness}, rotación={rotation}, orientación={orientation}")
        
        self.num_modules = num_modules
        self.brightness = max(0, min(15, brightness))  # Limitar a 0-15
        self.rotation = rotation % 360  # Normalizar a 0-359
        self.orientation = orientation.lower()
        
        # Variables para titileo (modo polling)
        self.blink_active = False
        self.blink_pattern = None
        self.blink_interval = 0.5
        self.last_blink_time = 0
        self.blink_state = False  # True = patrón visible, False = display limpio
        
        self.cs = Pin(cs_pin, Pin.OUT)
        self.spi = SPI(0, baudrate=10000000, polarity=0, phase=0, 
                      sck=Pin(clk_pin), mosi=Pin(din_pin))
        
        self.init_display()
        
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Display MAX7219 inicializado correctamente")

    def write_register_all(self, address, data):
        """Escribe el mismo registro a todos los módulos"""
        self.cs.value(0)
        for _ in range(self.num_modules):
            self.spi.write(bytearray([address, data]))
        self.cs.value(1)
        # Pequeña pausa para estabilizar
        for _ in range(10):
            pass

    def write_register_module(self, module_index, address, data):
        """Escribe un registro específico a un módulo"""
        self.cs.value(0)
        # En cascada: enviar datos en orden inverso
        for i in range(self.num_modules - 1, -1, -1):
            if i == module_index:
                self.spi.write(bytearray([address, data]))
            else:
                # Enviar comando NO-OP para mantener el estado
                self.spi.write(bytearray([0x00, 0x00]))
        self.cs.value(1)
        # Pequeña pausa para estabilizar
        for _ in range(10):
            pass

    def init_display(self):
        """Inicializa todos los módulos"""
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Inicializando módulos del display...")
        
        for address, data in [
            (0x09, 0x00),  # Decoding: off
            (0x0A, self.brightness),  # Brightness: configurable
            (0x0B, 0x07),  # Scan limit: 8 LEDs
            (0x0C, 0x01),  # Shutdown: normal operation
            (0x0F, 0x00),  # Display test: off
        ]:
            # if DEBUG_ENABLED:
            #     print(f"[MAX7219] Configurando registro 0x{address:02X} = 0x{data:02X}")
            self.write_register_all(address, data)
        
        self.clear()
        
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Módulos inicializados y display limpiado")

    def set_brightness(self, brightness):
        """Cambia el brillo de todos los módulos"""
        self.brightness = max(0, min(15, brightness))
        self.write_register_all(0x0A, self.brightness)

    def clear(self):
        """Limpia todos los módulos"""
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Limpiando display...")
        
        for i in range(1, 9):
            self.write_register_all(i, 0x00)
        
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Display limpiado")

    def rotate_pattern(self, pattern, rotation):
        """Rota un patrón según la rotación especificada"""
        if rotation == 0:
            return pattern
        elif rotation == 90:
            # Rotar 90°: transpuesta + invertir filas
            rotated = []
            for col in range(8):
                new_row = 0
                for row in range(8):
                    if pattern[row] & (1 << (7-col)):
                        new_row |= (1 << row)
                rotated.append(new_row)
            return rotated
        elif rotation == 180:
            # Rotar 180°: invertir filas y columnas
            rotated = []
            for row in pattern:
                # Invertir bits manualmente
                inverted = 0
                for i in range(8):
                    if row & (1 << i):
                        inverted |= (1 << (7-i))
                rotated.append(inverted)
            # Invertir orden de filas manualmente
            result = []
            for i in range(len(rotated)-1, -1, -1):
                result.append(rotated[i])
            return result
        elif rotation == 270:
            # Rotar 270°: transpuesta + invertir columnas
            rotated = []
            for col in range(8):
                new_row = 0
                for row in range(8):
                    if pattern[7-row] & (1 << col):
                        new_row |= (1 << (7-row))
                rotated.append(new_row)
            return rotated
        return pattern

    # Los patrones ahora se importan desde patterns/
    # DIGITS y HELMET están disponibles desde los imports

    def show_helmet_and_digit(self, digit):
        """Muestra el casco en el primer módulo y el dígito en el segundo"""
        # Obtener patrón del dígito
        s = str(digit)
        if len(s) == 1:
            s = "0" + s
        right_pattern = DIGITS.get(s[-1], [0]*8)  # Solo el último dígito
        helmet_pattern = HELMET
        # Aplicar rotación
        helmet_pattern = self.rotate_pattern(helmet_pattern, self.rotation)
        right_pattern = self.rotate_pattern(right_pattern, self.rotation)
        # Mostrar casco en el primer módulo, dígito en el segundo
        for row in range(8):
            self.write_register_module(0, row+1, helmet_pattern[row])
            self.write_register_module(1, row+1, right_pattern[row])

    def show_two_digits(self, value):
        """Muestra un número de dos dígitos (00-99) con rotación y orientación configuradas"""
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Mostrando dos dígitos: {value}")
        
        s = str(value)
        if len(s) == 1:
            s = "0" + s
        
        left_pattern = DIGITS.get(s[0], [0]*8)
        right_pattern = DIGITS.get(s[1], [0]*8)
        
        # Aplicar rotación
        left_pattern = self.rotate_pattern(left_pattern, self.rotation)
        right_pattern = self.rotate_pattern(right_pattern, self.rotation)
        
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Patrones: izquierda='{s[0]}', derecha='{s[1]}', orientación={self.orientation}")
        
        # Aplicar orientación
        if self.orientation == 'vertical':
            # Para orientación vertical, mostrar dígitos uno encima del otro
            # Combinar patrones verticalmente
            combined_pattern = []
            for i in range(8):
                combined_pattern.append(left_pattern[i])
            for i in range(8):
                combined_pattern.append(right_pattern[i])
            
            # Distribuir en los módulos según la orientación
            if self.num_modules >= 2:
                for row in range(8):
                    self.write_register_module(0, row+1, combined_pattern[row])
                    self.write_register_module(1, row+1, combined_pattern[row+8])
        else:
            # Orientación horizontal (por defecto)
            for row in range(8):
                self.write_register_module(0, row+1, left_pattern[row])
                self.write_register_module(1, row+1, right_pattern[row])
        
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Dígitos {value} mostrados correctamente")

    def show_text(self, text, start_position=0):
        """Muestra texto en el display (solo números por ahora)"""
        if len(text) < 2:
            text = "0" + text
        
        # Mostrar solo los primeros 2 caracteres
        text = text[:2]
        self.show_two_digits(int(text))

    def set_rotation(self, rotation):
        """Cambia la rotación del display"""
        self.rotation = rotation % 360

    def set_orientation(self, orientation):
        """Cambia la orientación del display"""
        self.orientation = orientation.lower()
        if self.orientation not in ['horizontal', 'vertical']:
            self.orientation = 'horizontal'

    def scroll_text(self, text, scroll_speed=0.3, repeat=True):
        """
        Hace scroll de texto en el display
        
        Args:
            text: Texto a mostrar (máximo 8 caracteres para display 8x16)
            scroll_speed: Velocidad del scroll en segundos
            repeat: Si debe repetir el scroll
        """
        from patterns.letters import get_letter_pattern
        
        # Convertir texto a mayúsculas y limitar longitud
        text = text.upper()[:8]
        
        # Crear secuencia de patrones para el texto
        text_patterns = []
        for letter in text:
            pattern = get_letter_pattern(letter)
            text_patterns.append(pattern)
        
        # Agregar espacios al inicio y final para mejor efecto
        empty_pattern = [0] * 8
        display_patterns = [empty_pattern] + text_patterns + [empty_pattern]
        
        # Calcular cuántos pasos necesitamos para mostrar todo el texto
        total_steps = len(display_patterns) * 8  # 8 columnas por letra
        
        step = 0
        while True:
            # Calcular qué patrones mostrar en cada paso
            start_col = step % 8
            pattern_index = step // 8
            
            if pattern_index >= len(display_patterns):
                if not repeat:
                    break
                step = 0
                continue
            
            # Obtener patrones actuales (máximo 2 letras visibles a la vez)
            current_patterns = display_patterns[pattern_index:pattern_index + 2]
            
            # Mostrar patrones en el display
            if len(current_patterns) >= 1:
                left_pattern = current_patterns[0]
                left_pattern = self.rotate_pattern(left_pattern, self.rotation)
                
                for row in range(8):
                    self.write_register_module(0, row+1, left_pattern[row])
            
            if len(current_patterns) >= 2:
                right_pattern = current_patterns[1]
                right_pattern = self.rotate_pattern(right_pattern, self.rotation)
                
                for row in range(8):
                    self.write_register_module(1, row+1, right_pattern[row])
            else:
                # Limpiar segundo módulo si no hay segunda letra
                for row in range(8):
                    self.write_register_module(1, row+1, 0)
            
            step += 1
            time.sleep(scroll_speed)
    
    def scroll_text_with_helmet(self, text, scroll_speed=0.2, repeat=False):
        """
        Hace scroll de texto con patrón de casco al inicio - Versión mejorada
        
        Args:
            text: Texto a mostrar (sin límite de caracteres)
            scroll_speed: Velocidad del scroll en segundos
            repeat: Si debe repetir el scroll
        """
        from patterns.letters import get_letter_pattern
        
        # Convertir texto a mayúsculas
        text = text.upper()
        
        # Crear secuencia de patrones: [espacio, casco, espacio, texto completo, espacio]
        empty_pattern = [0] * 8
        helmet_pattern = HELMET  # Usar el patrón real del casco
        
        # Crear patrones para todo el texto (sin límite)
        text_patterns = []
        for letter in text:
            pattern = get_letter_pattern(letter)
            text_patterns.append(pattern)
        
        # Secuencia completa: espacio + casco + espacio + texto completo + espacio
        display_patterns = [empty_pattern, helmet_pattern, empty_pattern] + text_patterns + [empty_pattern]
        
        # Calcular pasos totales para mostrar todo el contenido
        total_steps = len(display_patterns) * 8  # 8 columnas por patrón
        
        step = 0
        while True:
            # Calcular qué patrones mostrar en cada paso
            pattern_index = step // 8
            
            if pattern_index >= len(display_patterns):
                if not repeat:
                    break
                step = 0
                continue
            
            # Obtener patrones actuales (máximo 2 patrones visibles a la vez)
            current_patterns = display_patterns[pattern_index:pattern_index + 2]
            
            # Mostrar patrones en el display
            if len(current_patterns) >= 1:
                left_pattern = current_patterns[0]
                left_pattern = self.rotate_pattern(left_pattern, self.rotation)
                
                for row in range(8):
                    self.write_register_module(0, row+1, left_pattern[row])
            
            if len(current_patterns) >= 2:
                right_pattern = current_patterns[1]
                right_pattern = self.rotate_pattern(right_pattern, self.rotation)
                
                for row in range(8):
                    self.write_register_module(1, row+1, right_pattern[row])
            else:
                # Limpiar segundo módulo si no hay segundo patrón
                for row in range(8):
                    self.write_register_module(1, row+1, 0)
            
            step += 1
            time.sleep(scroll_speed)
    
    def scroll_text_smooth(self, text, scroll_speed=0.15, repeat=False):
        """
        Scroll suave de texto que simula movimiento real
        
        Args:
            text: Texto a mostrar (sin límite de caracteres)
            scroll_speed: Velocidad del scroll en segundos
            repeat: Si debe repetir el scroll
        """
        from patterns.letters import get_letter_pattern
        
        # Convertir texto a mayúsculas
        text = text.upper()
        
        # Crear patrones para todo el texto
        text_patterns = []
        for letter in text:
            pattern = get_letter_pattern(letter)
            text_patterns.append(pattern)
        
        # Agregar espacios al inicio y final para mejor efecto
        empty_pattern = [0] * 8
        display_patterns = [empty_pattern] + text_patterns + [empty_pattern]
        
        # Calcular pasos totales
        total_steps = len(display_patterns) * 8
        
        step = 0
        while True:
            # Calcular qué patrones mostrar en cada paso
            pattern_index = step // 8
            
            if pattern_index >= len(display_patterns):
                if not repeat:
                    break
                step = 0
                continue
            
            # Obtener patrones actuales (máximo 2 patrones visibles a la vez)
            current_patterns = display_patterns[pattern_index:pattern_index + 2]
            
            # Mostrar patrones en el display
            if len(current_patterns) >= 1:
                left_pattern = current_patterns[0]
                left_pattern = self.rotate_pattern(left_pattern, self.rotation)
                
                for row in range(8):
                    self.write_register_module(0, row+1, left_pattern[row])
            
            if len(current_patterns) >= 2:
                right_pattern = current_patterns[1]
                right_pattern = self.rotate_pattern(right_pattern, self.rotation)
                
                for row in range(8):
                    self.write_register_module(1, row+1, right_pattern[row])
            else:
                # Limpiar segundo módulo si no hay segundo patrón
                for row in range(8):
                    self.write_register_module(1, row+1, 0)
            
            step += 1
            time.sleep(scroll_speed)
    
    def test_pattern(self, pattern_type='all_on'):
        """Muestra patrones de prueba"""
        if pattern_type == 'all_on':
            for row in range(1, 9):
                self.write_register_all(row, 0xFF)
        elif pattern_type == 'all_off':
            self.clear()
        elif pattern_type == 'checkerboard':
            for row in range(1, 9):
                if row % 2 == 0:
                    self.write_register_all(row, 0xAA)
                else:
                    self.write_register_all(row, 0x55) 

    def show_racer_name_fast(self, name):
        """
        Muestra el nombre del piloto de forma rápida sin scroll bloqueante
        
        Args:
            name: Nombre del piloto a mostrar
        """
        from patterns.letters import get_letter_pattern
        
        # Convertir texto a mayúsculas y limitar a 2 caracteres
        text = name.upper()[:2]
        
        # Si solo hay un carácter, agregar espacio
        if len(text) == 1:
            text = text + " "
        
        # Mostrar los dos caracteres directamente
        left_pattern = get_letter_pattern(text[0])
        right_pattern = get_letter_pattern(text[1])
        
        # Aplicar rotación
        left_pattern = self.rotate_pattern(left_pattern, self.rotation)
        right_pattern = self.rotate_pattern(right_pattern, self.rotation)
        
        # Mostrar en el display inmediatamente
        for row in range(8):
            self.write_register_module(0, row+1, left_pattern[row])
            self.write_register_module(1, row+1, right_pattern[row]) 

    def start_pattern_blink(self, pattern, interval=0.5):
        """
        Inicia el titileo continuo de un patrón (modo polling)
        
        Args:
            pattern: Lista de 8 bytes que representan el patrón 8x8
            interval: Intervalo de titileo en segundos (por defecto 0.5s)
        """
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Iniciando titileo de patrón (modo polling) - intervalo: {interval}s")
        #     print(f"[MAX7219] Patrón recibido: {pattern}")
        #     print(f"[MAX7219] Longitud del patrón: {len(pattern) if pattern else 'None'}")
        
        if self.blink_active:
            # if DEBUG_ENABLED:
            #     print("[MAX7219] Titileo activo detectado, deteniendo antes de iniciar nuevo...")
            self.stop_pattern_blink()
        
        self.blink_pattern = pattern
        self.blink_interval = interval
        self.blink_active = True
        self.last_blink_time = time.time()
        self.blink_state = False
        
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Titileo iniciado correctamente (modo polling) - blink_active={self.blink_active}")
        return True

    def stop_pattern_blink(self):
        """Detiene el titileo de patrones (modo polling)"""
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Deteniendo titileo de patrón (modo polling)...")
        
        if not self.blink_active:
            # if DEBUG_ENABLED:
            #     print("[MAX7219] No hay titileo activo para detener")
            return
        
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Marcando titileo como inactivo...")
        self.blink_active = False
        
        # NO limpiar el display automáticamente - dejar que el contenido actual permanezca
        # if DEBUG_ENABLED:
        #     print("[MAX7219] Titileo detenido correctamente (modo polling) - display no limpiado")

    def update_pattern_blink(self):
        """Actualiza el estado del titileo de patrones (debe ser llamado desde el bucle principal)"""
        if not self.blink_active or not self.blink_pattern:
            # if DEBUG_ENABLED:
            #     print(f"[MAX7219] update_pattern_blink: blink_active={self.blink_active}, blink_pattern={self.blink_pattern is not None}")
            return
        
        current_time = time.time()
        if current_time - self.last_blink_time >= self.blink_interval:
            self.last_blink_time = current_time
            self.blink_state = not self.blink_state
            
            if self.blink_state:
                # Mostrar patrón
                # if DEBUG_ENABLED:
                #     print(f"[MAX7219] Titileo: mostrando patrón - {len(self.blink_pattern)} filas")
                for row in range(8):
                    self.write_register_all(row + 1, self.blink_pattern[row])
                # if DEBUG_ENABLED:
                #     print("[MAX7219] Titileo: patrón VISIBLE")
            else:
                # Limpiar display
                # if DEBUG_ENABLED:
                #     print("[MAX7219] Titileo: limpiando display...")
                self.clear()
                # if DEBUG_ENABLED:
                #     print("[MAX7219] Titileo: patrón OCULTO")

    def is_blinking(self):
        """Retorna True si el display está titilando"""
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Consultando estado de titileo: {self.blink_active}")
        return self.blink_active

    def set_blink_interval(self, interval):
        """Cambia el intervalo de titileo"""
        # if DEBUG_ENABLED:
        #     print(f"[MAX7219] Cambiando intervalo de titileo de {self.blink_interval}s a {interval}s")
        self.blink_interval = max(0.1, interval)  # Mínimo 0.1 segundos 