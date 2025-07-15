"""
Controlador de Carrera - Maneja la lógica del contador de vueltas
Integra el display MAX7219 configurable y animaciones
"""

import time
from machine import Pin
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
from traffic_light_controller import TrafficLightController
from config import *
from patterns.animations import get_animation_patterns

class RaceController:
    def __init__(self, max_laps=RACE_MAX_LAPS):
        """Inicializa el controlador de carrera"""
        self.max_laps = max_laps
        self.current_laps = 0
        self.is_completed = False
        self.is_race_started = False  # Nuevo estado: carrera iniciada
        self.last_sensor_time = 0
        
        # Inicializar nombre del piloto
        self.racer_name = RACER_NAME
        
        # Inicializar LED
        self.led = Pin(LED_PIN_RED, Pin.OUT)
        self.led.off()
        
        # Inicializar semáforo con referencia al controlador de carrera
        self.traffic_light = TrafficLightController(self)
        
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
            print(f"[RACE] Piloto: {self.racer_name}")
            print(f"[RACE] Estado inicial: Carrera no iniciada")
    
    def increment_lap(self):
        """Incrementa el contador de vueltas solo si la carrera está iniciada"""
        if self.is_completed:
            if DEBUG_ENABLED:
                print("[RACE] Carrera ya completada")
            return False
        
        # Verificar si la carrera está iniciada
        if not self.is_race_started:
            if DEBUG_ENABLED:
                print("[RACE] Carrera no iniciada - ignorando detección del sensor")
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
    
    def increment_lap_immediate(self):
        """Incrementa el contador de vueltas inmediatamente sin debounce para respuesta rápida"""
        if self.is_completed:
            return False
        
        # Verificar si la carrera está iniciada
        if not self.is_race_started:
            return False
        
        # Incrementar inmediatamente sin debounce para respuesta rápida
        self.current_laps += 1
        
        # Actualizar display inmediatamente
        self.update_display()
        
        # Verificar si la carrera está completada
        if self.current_laps >= self.max_laps:
            self.complete_race()
        
        return True
    
    def start_race(self):
        """Inicia la carrera - permite que el sensor cuente vueltas"""
        # Si hay previa activa, terminarla automáticamente sin mensajes
        if self.traffic_light and self.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            try:
                self.traffic_light.race_previous_stop()
                # Esperar un momento para que se complete la terminación
                time.sleep(0.1)
            except Exception as e:
                pass
        
        # Verificar que la previa se terminó correctamente
        if self.traffic_light and self.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            try:
                self.traffic_light.race_previous_stop()
                time.sleep(0.1)
            except Exception as e:
                pass
        
        self.is_race_started = True
        return True
    
    def stop_race(self):
        """Detiene la carrera - el sensor no cuenta vueltas"""
        self.is_race_started = False
        
        if DEBUG_ENABLED:
            print("[RACE] Carrera detenida - Sensor inactivo")
        
        return True
    
    def is_race_running(self):
        """Retorna True si la carrera está iniciada y no completada"""
        return self.is_race_started and not self.is_completed
    
    def reset_race(self):
        """Reinicia la carrera"""
        self.current_laps = 0
        self.is_completed = False
        self.is_race_started = False  # Resetear estado de carrera iniciada
        self.last_sensor_time = 0
        
        if DEBUG_ENABLED:
            print("[RACE] Carrera reiniciada")
        
        self.update_display()
        return True
    
    def complete_race(self):
        """Marca la carrera como completada, muestra animación y termina automáticamente"""
        self.is_completed = True
        
        if DEBUG_ENABLED:
            print(f"[RACE] ¡Carrera completada! {self.current_laps} vueltas")
        
        # Mostrar animación de bandera si está habilitada
        if RACE_SHOW_FLAG_ANIMATION:
            self.show_flag_animation()
        else:
            self.update_display()
        
        # Esperar a que termine la animación de bandera
        time.sleep(FLAG_ANIMATION_DURATION)
        
        # Terminar la carrera automáticamente
        self._finish_race_automatically()
    
    def _finish_race_automatically(self):
        """Termina la carrera automáticamente: apaga semáforos, resetea vueltas"""
        if DEBUG_ENABLED:
            print("[RACE] Finalizando carrera automáticamente...")
        
        # 1. Apagar semáforos
        if self.traffic_light:
            self.traffic_light.race_stop()
            if DEBUG_ENABLED:
                print("[RACE] Semáforos apagados")
        
        # 2. Detener la carrera
        self.stop_race()
        
        # 3. Resetear vueltas
        self.reset_race()
        
        if DEBUG_ENABLED:
            print("[RACE] Carrera finalizada automáticamente")
    
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
        # Usar patrones centralizados
        checkered_patterns = get_animation_patterns('checkered')
        
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
        # Usar patrones centralizados
        pulse_patterns = get_animation_patterns('pulse')
        
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
        # Usar patrones centralizados
        wave_patterns = get_animation_patterns('wave')
        
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
            'is_race_started': self.is_race_started,
            'is_race_running': self.is_race_running(),
            'progress_percentage': progress_percentage,
            'racer_name': self.racer_name,
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
    
    def set_scroll_speed(self, speed):
        """Cambia la velocidad del scroll del nombre del piloto"""
        global RACER_NAME_SCROLL_SPEED
        RACER_NAME_SCROLL_SPEED = max(0.1, min(1.0, speed))  # Limitar entre 0.1 y 1.0 segundos
        
        if DEBUG_ENABLED:
            print(f"[RACE] Velocidad de scroll cambiada a: {RACER_NAME_SCROLL_SPEED}s")
    
    def get_scroll_speed(self):
        """Retorna la velocidad actual del scroll"""
        return RACER_NAME_SCROLL_SPEED
    
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
    
    def get_racer_name(self):
        """Retorna el nombre actual del piloto"""
        return self.racer_name
    
    def set_racer_name(self, name):
        """Cambia el nombre del piloto y lo muestra en el display"""
        if name and len(name) <= RACER_NAME_MAX_LENGTH:
            self.racer_name = name
            
            # Mostrar el nombre inmediatamente sin scroll que bloquea
            self.display_racer_name()
            return True
        else:
            return False
    
    def display_racer_name(self):
        """Muestra el nombre del piloto en el display de forma rápida"""
        # Usar la función rápida sin scroll bloqueante
        self.display.show_racer_name_fast(self.racer_name)
    
    def display_racer_name_with_scroll(self):
        """Muestra el nombre del piloto con scroll: [Casco] NOMBRE PILOTO"""
        if DEBUG_ENABLED:
            print(f"[RACE] Mostrando nombre con scroll: {self.racer_name.upper()}")
        
        # Mostrar scroll del texto con casco real y velocidad configurable
        self.display.scroll_text_with_helmet(self.racer_name, scroll_speed=RACER_NAME_SCROLL_SPEED, repeat=False)
        
        # Después del scroll, volver al estado normal del display
        self.update_display()
    
    # =============================================================================
    # MÉTODOS DEL SEMÁFORO
    # =============================================================================
    
    def race_previous(self):
        """Inicia el titileo de todas las luces del semáforo"""
        return self.traffic_light.race_previous()
    
    def race_previous_stop(self):
        """Detiene el titileo de todas las luces del semáforo"""
        return self.traffic_light.race_previous_stop()
    
    def race_start(self):
        """Inicia la secuencia de largada: Roja -> Amarilla -> Verde"""
        return self.traffic_light.race_start()
    
    def race_stop(self):
        """Apaga las luces verdes del semáforo"""
        return self.traffic_light.race_stop()
    
    def get_traffic_light_status(self):
        """Retorna el estado actual del semáforo"""
        return self.traffic_light.get_status()
    
    def cleanup(self):
        """Limpia recursos al finalizar"""
        self.led.off()
        self.display.clear()
        self.traffic_light.cleanup()
        
        if DEBUG_ENABLED:
            print("[RACE] Limpieza completada") 