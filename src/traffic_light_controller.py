"""
Controlador del Semáforo - Maneja las luces del semáforo para la largada de carreras
Optimizado para módulo de 5V conectado a 3.3V
"""

import time
import _thread
from machine import Pin, PWM
from config import *

class TrafficLightController:
    def __init__(self, race_controller=None):
        """Inicializa el controlador del semáforo"""
        # Inicializar pines del semáforo con PWM para mejor control
        self.red_light = PWM(Pin(TRAFFIC_LIGHT_RED_PIN), freq=1000)
        self.yellow_light = PWM(Pin(TRAFFIC_LIGHT_YELLOW_PIN), freq=1000)
        self.green_light = PWM(Pin(TRAFFIC_LIGHT_GREEN_PIN), freq=1000)
        
        # Configurar duty cycle para compensar voltaje más bajo
        self.duty_on = 65535  # Máximo brillo (100%) - rango completo de 16 bits
        self.duty_off = 0    # Apagado
        
        # Estado del semáforo
        self.current_state = TRAFFIC_LIGHT_STATE_OFF
        self.blinking_thread = None
        self.blinking_active = False
        
        # Referencia al controlador de carrera
        self.race_controller = race_controller
        
        # Apagar todas las luces al inicio
        self._turn_off_all_lights()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Controlador de semáforo inicializado")
            print(f"[TRAFFIC] Pines: Rojo={TRAFFIC_LIGHT_RED_PIN}, Amarillo={TRAFFIC_LIGHT_YELLOW_PIN}, Verde={TRAFFIC_LIGHT_GREEN_PIN}")
            print(f"[TRAFFIC] Duty cycle: ON={self.duty_on}, OFF={self.duty_off}")
    
    def _turn_off_all_lights(self):
        """Apaga todas las luces del semáforo"""
        self.red_light.duty_u16(self.duty_off)
        self.yellow_light.duty_u16(self.duty_off)
        self.green_light.duty_u16(self.duty_off)
    
    def _turn_on_light(self, light, duty_cycle=None):
        """Enciende una luz específica"""
        if duty_cycle is None:
            duty_cycle = self.duty_on
        light.duty_u16(duty_cycle)
    
    def _turn_off_light(self, light):
        """Apaga una luz específica"""
        light.duty_u16(self.duty_off)
    
    def _blinking_thread_function(self):
        """Función del hilo para el titileo de las luces"""
        while self.blinking_active:
            # Encender todas las luces
            self._turn_on_light(self.red_light)
            self._turn_on_light(self.yellow_light)
            self._turn_on_light(self.green_light)
            time.sleep(TRAFFIC_LIGHT_BLINK_INTERVAL)
            
            # Apagar todas las luces
            self._turn_off_light(self.red_light)
            self._turn_off_light(self.yellow_light)
            self._turn_off_light(self.green_light)
            time.sleep(TRAFFIC_LIGHT_BLINK_INTERVAL)
    
    def race_previous(self):
        """Inicia el titileo de todas las luces del semáforo"""
        if self.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Titileo ya activo")
            return False
        
        # Detener cualquier titileo previo
        self.race_previous_stop()
        
        # Iniciar nuevo titileo
        self.blinking_active = True
        self.current_state = TRAFFIC_LIGHT_STATE_BLINKING
        
        try:
            # Iniciar hilo de titileo
            self.blinking_thread = _thread.start_new_thread(self._blinking_thread_function, ())
            
            if DEBUG_ENABLED:
                print("[TRAFFIC] Titileo iniciado - todas las luces")
            return True
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Error iniciando titileo: {e}")
            self.blinking_active = False
            self.current_state = TRAFFIC_LIGHT_STATE_OFF
            return False
    
    def race_previous_stop(self):
        """Detiene el titileo de todas las luces del semáforo"""
        if self.current_state != TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[TRAFFIC] No hay titileo activo para detener")
            return False
        
        # Detener titileo
        self.blinking_active = False
        self.current_state = TRAFFIC_LIGHT_STATE_OFF
        
        # Apagar todas las luces
        self._turn_off_all_lights()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Titileo detenido")
        return True
    
    def race_start(self):
        """Inicia la secuencia de largada: Roja -> Amarilla -> Verde"""
        if self.current_state in [TRAFFIC_LIGHT_STATE_RED, TRAFFIC_LIGHT_STATE_YELLOW, TRAFFIC_LIGHT_STATE_GREEN]:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Secuencia de largada ya en progreso")
            return False
        
        # Detener cualquier titileo previo de forma segura
        try:
            self.race_previous_stop()
            # Esperar un momento para que se complete la terminación
            time.sleep(0.1)
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Error terminando previa antes de largada: {e}")
        
        # Verificar que la previa se terminó correctamente
        if self.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Previa aún activa, intentando terminar nuevamente")
            try:
                self.race_previous_stop()
                time.sleep(0.1)
            except Exception as e:
                if DEBUG_ENABLED:
                    print(f"[TRAFFIC] Error en segundo intento de terminar previa: {e}")
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Iniciando secuencia de largada")
        
        # Iniciar hilo para la secuencia de largada
        try:
            _thread.start_new_thread(self._race_start_sequence, ())
            return True
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Error iniciando secuencia de largada: {e}")
            return False
    
    def _race_start_sequence(self):
        """Secuencia interna de largada: Roja -> Amarilla -> Verde"""
        try:
            # Fase 1: Luz roja
            if DEBUG_ENABLED:
                print("[TRAFFIC] Fase 1: Luz roja")
            
            self.current_state = TRAFFIC_LIGHT_STATE_RED
            self._turn_off_all_lights()
            self._turn_on_light(self.red_light)
            
            time.sleep(TRAFFIC_LIGHT_RED_DURATION)
            
            # Fase 2: Luz amarilla (mantener roja)
            if DEBUG_ENABLED:
                print("[TRAFFIC] Fase 2: Luz amarilla")
            
            self.current_state = TRAFFIC_LIGHT_STATE_YELLOW
            self._turn_on_light(self.yellow_light)  # Mantener roja y agregar amarilla
            
            time.sleep(TRAFFIC_LIGHT_YELLOW_DURATION)
            
            # Fase 3: Luz verde (apagar roja y amarilla)
            if DEBUG_ENABLED:
                print("[TRAFFIC] Fase 3: Luz verde - ¡LARGADA!")
            
            self.current_state = TRAFFIC_LIGHT_STATE_GREEN
            self._turn_off_all_lights()
            self._turn_on_light(self.green_light)
            
            # Iniciar la carrera automáticamente cuando se enciende la luz verde
            if self.race_controller:
                self.race_controller.start_race()
                if DEBUG_ENABLED:
                    print("[TRAFFIC] Carrera iniciada automáticamente")
            
            if DEBUG_ENABLED:
                print("[TRAFFIC] Secuencia de largada completada")
                
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Error en secuencia de largada: {e}")
            self.current_state = TRAFFIC_LIGHT_STATE_OFF
            self._turn_off_all_lights()
    
    def race_stop(self):
        """Apaga las luces verdes del semáforo"""
        if self.current_state != TRAFFIC_LIGHT_STATE_GREEN:
            if DEBUG_ENABLED:
                print("[TRAFFIC] No hay luz verde activa para apagar")
            return False
        
        self.current_state = TRAFFIC_LIGHT_STATE_OFF
        self._turn_off_all_lights()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Luces verdes apagadas")
        return True
    
    def get_status(self):
        """Retorna el estado actual del semáforo"""
        return {
            'state': self.current_state,
            'red_on': self.red_light.duty_u16() > 0,
            'yellow_on': self.yellow_light.duty_u16() > 0,
            'green_on': self.green_light.duty_u16() > 0,
            'blinking_active': self.blinking_active
        }
    
    def cleanup(self):
        """Limpia recursos al finalizar"""
        self.race_previous_stop()
        self.race_stop()
        
        # Desactivar PWM
        self.red_light.deinit()
        self.yellow_light.deinit()
        self.green_light.deinit()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Limpieza completada") 