"""
Controlador de Carrera - Maneja la lógica del contador de vueltas
Integra el display MAX7219 configurable y animaciones
"""

import time
from machine import Pin
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
from config import *

class RaceController:
    def __init__(self, max_laps=RACE_MAX_LAPS):
        """Inicializa el controlador de carrera"""
        self.max_laps = max_laps
        self.current_laps = 0
        self.is_completed = False
        self.last_sensor_time = 0
        
        # Inicializar LED
        self.led = Pin(LED_PIN_RED, Pin.OUT)
        self.led.off()
        
        # Inicializar display configurable
        self.display = MAX7219DualDisplayConfigurable(
            din_pin=MAX7219_DIN_PIN,
            cs_pin=MAX7219_CS_PIN,
            clk_pin=MAX7219_CLK_PIN,
            num_modules=MAX7219_NUM_MODULES,
            brightness=MAX7219_BRIGHTNESS,
            rotation=MAX7219_ROTATION,
            orientation=MAX7219_ORIENTATION
        )
        
        # Mostrar estado inicial
        self.update_display()
        
        if DEBUG_ENABLED:
            print(f"[RACE] Controlador inicializado - Máximo: {max_laps} vueltas")
    
    def increment_lap(self):
        """Incrementa el contador de vueltas"""
        if self.is_completed:
            if DEBUG_ENABLED:
                print("[RACE] Carrera ya completada")
            return False
        
        # Verificar debounce del sensor
        current_time = time.time()
        if current_time - self.last_sensor_time < SENSOR_DEBOUNCE_TIME:
            if DEBUG_ENABLED:
                print("[RACE] Debounce - ignorando señal")
            return False
        
        self.last_sensor_time = current_time
        self.current_laps += 1
        
        if DEBUG_ENABLED:
            print(f"[RACE] Vuelta incrementada: {self.current_laps}/{self.max_laps}")
        
        # Verificar si la carrera está completada
        if self.current_laps >= self.max_laps:
            self.complete_race()
        else:
            self.update_display()
        
        return True
    
    def reset_race(self):
        """Reinicia la carrera"""
        self.current_laps = 0
        self.is_completed = False
        self.last_sensor_time = 0
        
        if DEBUG_ENABLED:
            print("[RACE] Carrera reiniciada")
        
        self.update_display()
        return True
    
    def complete_race(self):
        """Marca la carrera como completada y muestra animación"""
        self.is_completed = True
        
        if DEBUG_ENABLED:
            print(f"[RACE] ¡Carrera completada! {self.current_laps} vueltas")
        
        # Mostrar animación de bandera si está habilitada
        if RACE_SHOW_FLAG_ANIMATION:
            self.show_flag_animation()
        else:
            self.update_display()
        
        # Reiniciar automáticamente si está habilitado
        if RACE_AUTO_RESET:
            time.sleep(FLAG_ANIMATION_DURATION)
            self.reset_race()
    
    def update_display(self):
        """Actualiza el display con el contador actual"""
        if self.is_completed:
            # Mostrar "FI" (Final) cuando está completada
            self.display.show_two_digits(99)  # Usar 99 como código para "FI"
        else:
            # Mostrar número de vueltas
            self.display.show_two_digits(self.current_laps)
    
    def show_flag_animation(self, animation_type=DEFAULT_COMPLETION_ANIMATION):
        """Muestra animación de bandera configurable"""
        if DEBUG_ENABLED:
            print(f"[RACE] Iniciando animación: {animation_type}")
        
        if animation_type == "checkered_flag":
            self._show_checkered_flag_animation()
        elif animation_type == "spinning_flag":
            self._show_spinning_flag_animation()
        elif animation_type == "pulse_flag":
            self._show_pulse_flag_animation()
        elif animation_type == "wave_flag":
            self._show_wave_flag_animation()
        elif animation_type == "none":
            # No mostrar animación
            pass
        else:
            # Animación por defecto
            self._show_checkered_flag_animation()
    
    def _show_checkered_flag_animation(self):
        """Muestra animación de bandera a cuadros clásica con cuadros 2x2 que alterna patrones"""
        # Dos patrones complementarios de bandera a cuadros 2x2
        # Cuando uno se apaga, el otro se enciende para mantener el display activo
        checkered_patterns = [
            # Patrón 1: cuadros 2x2 (0xCC = 11001100, 0x33 = 00110011)
            [0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33],
            # Patrón 2: cuadros complementarios (0x33 = 00110011, 0xCC = 11001100)
            [0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC],
        ]
        
        start_time = time.time()
        pattern_index = 0
        
        while time.time() - start_time < FLAG_ANIMATION_DURATION:
            # Mostrar patrón actual
            pattern = checkered_patterns[pattern_index % len(checkered_patterns)]
            for row in range(8):
                self.display.write_register_all(row + 1, pattern[row])
            
            # Cambiar al siguiente patrón
            pattern_index += 1
            
            # Esperar intervalo configurable
            time.sleep(CHECKERED_FLAG_BLINK_INTERVAL)
        
        # Limpiar display al finalizar
        self.display.clear()
    
    def _show_spinning_flag_animation(self):
        """Muestra animación de bandera giratoria"""
        # Patrones que simulan rotación
        spinning_patterns = [
            # Rotación 0°
            [0x81, 0x42, 0x24, 0x18, 0x18, 0x24, 0x42, 0x81],
            # Rotación 45°
            [0x00, 0x81, 0x42, 0x24, 0x24, 0x42, 0x81, 0x00],
            # Rotación 90°
            [0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF],
            # Rotación 135°
            [0x00, 0x00, 0x81, 0x42, 0x42, 0x81, 0x00, 0x00],
        ]
        
        start_time = time.time()
        pattern_index = 0
        
        while time.time() - start_time < FLAG_ANIMATION_DURATION:
            pattern = spinning_patterns[pattern_index % len(spinning_patterns)]
            
            for row in range(8):
                self.display.write_register_all(row + 1, pattern[row])
            
            pattern_index += 1
            time.sleep(FLAG_ANIMATION_SPEED)
        
        self.display.clear()
    
    def _show_pulse_flag_animation(self):
        """Muestra animación de bandera pulsante"""
        # Patrones que pulsan desde el centro
        pulse_patterns = [
            [0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x3C, 0x3C, 0x3C, 0x3C, 0x00, 0x00],
            [0x00, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x00],
            [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
            [0x00, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x00],
            [0x00, 0x00, 0x3C, 0x3C, 0x3C, 0x3C, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00],
        ]
        
        start_time = time.time()
        pattern_index = 0
        
        while time.time() - start_time < FLAG_ANIMATION_DURATION:
            pattern = pulse_patterns[pattern_index % len(pulse_patterns)]
            
            for row in range(8):
                self.display.write_register_all(row + 1, pattern[row])
            
            pattern_index += 1
            time.sleep(FLAG_ANIMATION_SPEED)
        
        self.display.clear()
    
    def _show_wave_flag_animation(self):
        """Muestra animación de bandera ondulante"""
        # Patrones que simulan ondas
        wave_patterns = [
            [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80],
            [0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x01],
            [0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x01, 0x02],
            [0x08, 0x10, 0x20, 0x40, 0x80, 0x01, 0x02, 0x04],
            [0x10, 0x20, 0x40, 0x80, 0x01, 0x02, 0x04, 0x08],
            [0x20, 0x40, 0x80, 0x01, 0x02, 0x04, 0x08, 0x10],
            [0x40, 0x80, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20],
            [0x80, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40],
        ]
        
        start_time = time.time()
        pattern_index = 0
        
        while time.time() - start_time < FLAG_ANIMATION_DURATION:
            pattern = wave_patterns[pattern_index % len(wave_patterns)]
            
            for row in range(8):
                self.display.write_register_all(row + 1, pattern[row])
            
            pattern_index += 1
            time.sleep(FLAG_ANIMATION_SPEED)
        
        self.display.clear()
    
    def get_race_status(self):
        """Retorna el estado actual de la carrera"""
        progress_percentage = (self.current_laps / self.max_laps) * 100 if self.max_laps > 0 else 0
        
        return {
            'current_laps': self.current_laps,
            'max_laps': self.max_laps,
            'remaining_laps': max(0, self.max_laps - self.current_laps),
            'is_completed': self.is_completed,
            'progress_percentage': progress_percentage,
            'led_status': {
                'is_on': self.led.value() == 1
            }
        }
    
    def toggle_led(self):
        """Alterna el estado del LED"""
        current_state = self.led.value()
        self.led.value(not current_state)
        
        if DEBUG_ENABLED:
            print(f"[RACE] LED alternado: {'ON' if not current_state else 'OFF'}")
        
        return not current_state
    
    def turn_on_led(self):
        """Enciende el LED"""
        self.led.on()
        
        if DEBUG_ENABLED:
            print("[RACE] LED encendido")
        
        return True
    
    def turn_off_led(self):
        """Apaga el LED"""
        self.led.off()
        
        if DEBUG_ENABLED:
            print("[RACE] LED apagado")
        
        return False
    
    def set_brightness(self, brightness):
        """Cambia el brillo del display"""
        self.display.set_brightness(brightness)
        
        if DEBUG_ENABLED:
            print(f"[RACE] Brillo cambiado a: {brightness}")
    
    def set_rotation(self, rotation):
        """Cambia la rotación del display"""
        self.display.set_rotation(rotation)
        
        if DEBUG_ENABLED:
            print(f"[RACE] Rotación cambiada a: {rotation}°")
    
    def set_orientation(self, orientation):
        """Cambia la orientación del display"""
        self.display.set_orientation(orientation)
        
        if DEBUG_ENABLED:
            print(f"[RACE] Orientación cambiada a: {orientation}")
    
    def set_completion_animation(self, animation_type):
        """Cambia la animación de finalización"""
        if animation_type in ANIMATION_TYPES:
            global DEFAULT_COMPLETION_ANIMATION
            DEFAULT_COMPLETION_ANIMATION = animation_type
            
            if DEBUG_ENABLED:
                print(f"[RACE] Animación de finalización cambiada a: {animation_type}")
            return True
        else:
            if DEBUG_ENABLED:
                print(f"[RACE] Animación no válida: {animation_type}")
            return False
    
    def get_available_animations(self):
        """Retorna las animaciones disponibles"""
        return ANIMATION_TYPES
    
    def test_animation(self, animation_type):
        """Prueba una animación específica"""
        if animation_type in ANIMATION_TYPES:
            if DEBUG_ENABLED:
                print(f"[RACE] Probando animación: {animation_type}")
            self.show_flag_animation(animation_type)
            return True
        else:
            if DEBUG_ENABLED:
                print(f"[RACE] Animación no válida: {animation_type}")
            return False
    
    def cleanup(self):
        """Limpia recursos al finalizar"""
        self.led.off()
        self.display.clear()
        
        if DEBUG_ENABLED:
            print("[RACE] Limpieza completada") 