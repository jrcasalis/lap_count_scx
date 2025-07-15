"""
Controlador del Semáforo - Maneja las luces del semáforo para la largada de carreras
Optimizado para módulo de 5V conectado a 3.3V
"""

import time
import _thread
from machine import Pin, PWM
from config import *

class TrafficLightController:
    def __init__(self):
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
        self.blinking_active = False
        
        # Variables para polling (sin hilos)
        self.last_blink_time = 0
        self.blink_state = False  # True = luces encendidas, False = luces apagadas
        
        # Apagar todas las luces al inicio
        self._turn_off_all_lights()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Controlador de semáforo inicializado (modo polling)")
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
    
    def update_blinking(self):
        """Actualiza el estado del titileo (debe ser llamado desde el bucle principal)"""
        if not self.blinking_active:
            return
        
        current_time = time.time()
        if current_time - self.last_blink_time >= TRAFFIC_LIGHT_BLINK_INTERVAL:
            self.last_blink_time = current_time
            self.blink_state = not self.blink_state
            
            if self.blink_state:
                # Encender todas las luces
                self._turn_on_light(self.red_light)
                self._turn_on_light(self.yellow_light)
                self._turn_on_light(self.green_light)
                if DEBUG_ENABLED:
                    print("[TRAFFIC] Titileo: luces ENCENDIDAS")
            else:
                # Apagar todas las luces
                self._turn_off_light(self.red_light)
                self._turn_off_light(self.yellow_light)
                self._turn_off_light(self.green_light)
                if DEBUG_ENABLED:
                    print("[TRAFFIC] Titileo: luces APAGADAS")
    
    def race_previous(self):
        """Inicia el titileo de todas las luces del semáforo a máxima potencia (previa de carrera)"""
        if DEBUG_ENABLED:
            print(f"[TRAFFIC] Iniciando previa - Estado actual: {self.current_state}")
        
        if self.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Titileo ya activo")
            return False
        
        # Detener cualquier titileo previo
        if DEBUG_ENABLED:
            print("[TRAFFIC] Deteniendo titileo previo...")
        self.race_previous_stop()
        
        # Iniciar nuevo titileo (modo polling)
        if DEBUG_ENABLED:
            print("[TRAFFIC] Configurando nuevo titileo (modo polling)...")
        self.blinking_active = True
        self.current_state = TRAFFIC_LIGHT_STATE_BLINKING
        self.last_blink_time = time.time()
        self.blink_state = False
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Titileo iniciado - todas las luces (modo polling)")
        return True
    
    def race_previous_stop(self):
        """Detiene el titileo de todas las luces del semáforo (fin de la previa)"""
        if DEBUG_ENABLED:
            print(f"[TRAFFIC] Deteniendo previa - Estado actual: {self.current_state}")
        
        if self.current_state != TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[TRAFFIC] No hay titileo activo para detener")
            return False
        
        # Detener titileo (modo polling)
        if DEBUG_ENABLED:
            print("[TRAFFIC] Deteniendo titileo (modo polling)...")
        self.blinking_active = False
        self.current_state = TRAFFIC_LIGHT_STATE_OFF
        
        # Apagar todas las luces
        if DEBUG_ENABLED:
            print("[TRAFFIC] Apagando todas las luces...")
        self._turn_off_all_lights()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Titileo detenido (modo polling)")
        return True
    
    def race_start(self):
        """Inicia la secuencia de largada: Roja -> Amarilla -> Verde"""
        if DEBUG_ENABLED:
            print(f"[TRAFFIC] Iniciando secuencia de largada - Estado actual: {self.current_state}")
        
        if self.current_state in [TRAFFIC_LIGHT_STATE_RED, TRAFFIC_LIGHT_STATE_YELLOW, TRAFFIC_LIGHT_STATE_GREEN]:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Secuencia de largada ya en progreso")
            return False
        
        # Verificar que no hay hilos activos
        if self.blinking_active:
            if DEBUG_ENABLED:
                print("[TRAFFIC] WARNING: Hilo de titileo aún activo, forzando detención...")
            self.blinking_active = False
            time.sleep(0.5)  # Esperar más tiempo
        
        # Detener cualquier titileo previo de forma segura
        if DEBUG_ENABLED:
            print("[TRAFFIC] Deteniendo previa antes de largada...")
        try:
            self.race_previous_stop()
            # Esperar un momento para que se complete la terminación
            time.sleep(0.2)
            if DEBUG_ENABLED:
                print("[TRAFFIC] Previa detenida, espera completada")
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Error terminando previa antes de largada: {e}")
        
        # Verificar que la previa se terminó correctamente
        if self.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Previa aún activa, intentando terminar nuevamente")
            try:
                self.race_previous_stop()
                time.sleep(0.2)
                if DEBUG_ENABLED:
                    print("[TRAFFIC] Segundo intento de terminar previa completado")
            except Exception as e:
                if DEBUG_ENABLED:
                    print(f"[TRAFFIC] Error en segundo intento de terminar previa: {e}")
        
        # Verificación final antes de iniciar
        if self.blinking_active:
            if DEBUG_ENABLED:
                print("[TRAFFIC] ERROR: No se pudo detener el hilo de titileo")
            return False
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Iniciando secuencia de largada")
        
        # Iniciar hilo para la secuencia de largada
        try:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Iniciando hilo de secuencia de largada...")
            _thread.start_new_thread(self._race_start_sequence, ())
            if DEBUG_ENABLED:
                print("[TRAFFIC] Hilo de secuencia de largada iniciado")
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
            
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Luz roja encendida, esperando {TRAFFIC_LIGHT_RED_DURATION}s...")
            time.sleep(TRAFFIC_LIGHT_RED_DURATION)
            
            # Fase 2: Luz amarilla (mantener roja)
            if DEBUG_ENABLED:
                print("[TRAFFIC] Fase 2: Luz amarilla")
            
            self.current_state = TRAFFIC_LIGHT_STATE_YELLOW
            self._turn_on_light(self.yellow_light)  # Mantener roja y agregar amarilla
            
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Luz amarilla encendida, esperando {TRAFFIC_LIGHT_YELLOW_DURATION}s...")
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
        if DEBUG_ENABLED:
            print(f"[TRAFFIC] Deteniendo carrera - Estado actual: {self.current_state}")
        
        if self.current_state != TRAFFIC_LIGHT_STATE_GREEN:
            if DEBUG_ENABLED:
                print("[TRAFFIC] No hay luz verde activa para apagar")
            return False
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Apagando luces verdes...")
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
        if DEBUG_ENABLED:
            print("[TRAFFIC] Iniciando limpieza de recursos...")
        
        # Detener todos los procesos activos
        self.race_previous_stop()
        self.race_stop()
        
        # Asegurar que no hay hilos activos
        if self.blinking_active:
            if DEBUG_ENABLED:
                print("[TRAFFIC] Forzando terminación de hilos activos...")
            self.blinking_active = False
            time.sleep(0.5)
        
        # Desactivar PWM
        if DEBUG_ENABLED:
            print("[TRAFFIC] Desactivando PWM...")
        self.red_light.deinit()
        self.yellow_light.deinit()
        self.green_light.deinit()
        
        if DEBUG_ENABLED:
            print("[TRAFFIC] Limpieza completada")

    def get_thread_status(self):
        """Retorna información sobre el estado del titileo"""
        return {
            'blinking_active': self.blinking_active,
            'current_state': self.current_state,
            'blink_state': self.blink_state,
            'last_blink_time': self.last_blink_time
        } 