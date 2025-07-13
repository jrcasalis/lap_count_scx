"""
Controlador del Semáforo Simplificado - Usa pines directos en lugar de PWM
Versión de respaldo para cuando PWM no funciona correctamente
"""

import time
import _thread
from machine import Pin
from config import *

class TrafficLightControllerSimple:
    def __init__(self):
        """Inicializa el controlador del semáforo con pines directos"""
        # Inicializar pines del semáforo como salida digital
        self.red_light = Pin(TRAFFIC_LIGHT_RED_PIN, Pin.OUT)
        self.yellow_light = Pin(TRAFFIC_LIGHT_YELLOW_PIN, Pin.OUT)
        self.green_light = Pin(TRAFFIC_LIGHT_GREEN_PIN, Pin.OUT)
        
        # Estado del semáforo
        self.current_state = TRAFFIC_LIGHT_STATE_OFF
        self.blinking_thread = None
        self.blinking_active = False
        
        # Apagar todas las luces al inicio
        self._turn_off_all_lights()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Controlador de semáforo simplificado inicializado")
            print(f"[TRAFFIC] Pines: Rojo={TRAFFIC_LIGHT_RED_PIN}, Amarillo={TRAFFIC_LIGHT_YELLOW_PIN}, Verde={TRAFFIC_LIGHT_GREEN_PIN}")
    
    def _turn_off_all_lights(self):
        """Apaga todas las luces del semáforo"""
        self.red_light.off()
        self.yellow_light.off()
        self.green_light.off()
    
    def _turn_on_light(self, light):
        """Enciende una luz específica"""
        light.on()
    
    def _turn_off_light(self, light):
        """Apaga una luz específica"""
        light.off()
    
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
        
        # Detener cualquier titileo previo
        self.race_previous_stop()
        
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
            'red_on': self.red_light.value() == 1,
            'yellow_on': self.yellow_light.value() == 1,
            'green_on': self.green_light.value() == 1,
            'blinking_active': self.blinking_active
        }
    
    def cleanup(self):
        """Limpia recursos al finalizar"""
        self.race_previous_stop()
        self.race_stop()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Limpieza completada") 