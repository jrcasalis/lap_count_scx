"""
Controlador de Carrera - Refactorizado para soportar múltiples corredores
"""

from traffic_light_controller import TrafficLightController
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
from config import (
    TRAFFIC_LIGHT_STATE_BLINKING, TRAFFIC_LIGHT_STATE_GREEN, DEBUG_ENABLED,
    RACE_MAX_LAPS, RACE_NUM_RACERS, RACE_START_TIMEOUT, SENSOR_DEBOUNCE_TIME, 
    FLAG_ANIMATION_DURATION, CHECKERED_FLAG_BLINK_INTERVAL, RACER_NAME,
    SENSOR_TCRT5000_PIN
)
from patterns.various import FULL_CIRCLE
from patterns.animations import CHECKERED_FLAG_PATTERNS
import time
from machine import Pin

# Compatibilidad utime para MicroPython y desarrollo
try:
    import utime
    ticks_ms = utime.ticks_ms
    ticks_diff = utime.ticks_diff
except ImportError:
    def ticks_ms():
        return int(time.time() * 1000)
    def ticks_diff(a, b):
        return a - b

class RaceController:
    # Variables globales al controlador (de clase) - Inicializadas en None para evitar conflictos
    max_laps = None
    num_racers = None
    racer_names = None
    current_laps = None
    traffic_light = None
    display = None
    race_state = None  # STOPPED | PREVIOUS | STARTED | FINISHED
    stopped_blink_enabled = None  # Controla si el patrón titila en estado STOPPED
    instance = None  # Referencia a la instancia actual para acceso desde métodos de clase
    _last_anim_time = None  # Para animación regular
    _anim_pattern_idx = 0

    def __init__(self, max_laps=None, num_racers=None, racer_names=None):
        """
        Inicializa el controlador de carrera con parámetros básicos.
        max_laps: cantidad de vueltas para finalizar la carrera (usa RACE_MAX_LAPS si no se especifica)
        num_racers: cantidad de corredores (usa RACE_NUM_RACERS si no se especifica)
        racer_names: lista de nombres de los corredores
        """
        RaceController.instance = self  # Guardar referencia a la instancia actual
        
        # Inicializar variables de clase solo si no están ya inicializadas
        if RaceController.max_laps is None:
            RaceController.max_laps = RACE_MAX_LAPS
        if RaceController.num_racers is None:
            RaceController.num_racers = RACE_NUM_RACERS if num_racers is None else num_racers
        if RaceController.racer_names is None:
            num_racers_to_use = RACE_NUM_RACERS if num_racers is None else num_racers
            RaceController.racer_names = [f"{RACER_NAME} {i+1}" for i in range(num_racers_to_use)]
        if RaceController.current_laps is None:
            num_racers_to_use = RACE_NUM_RACERS if num_racers is None else num_racers
            RaceController.current_laps = [0 for _ in range(num_racers_to_use)]
        if RaceController.race_state is None:
            RaceController.race_state = 'STOPPED'
        if RaceController.stopped_blink_enabled is None:
            RaceController.stopped_blink_enabled = True
        
        # Permitir sobrescribir valores solo si se pasan explícitamente
        if max_laps is not None:
            RaceController.max_laps = max_laps
        if num_racers is not None:
            RaceController.num_racers = num_racers
            # Actualizar también racer_names y current_laps si cambia num_racers
            RaceController.racer_names = [f"{RACER_NAME} {i+1}" for i in range(num_racers)]
            RaceController.current_laps = [0 for _ in range(num_racers)]
        if racer_names is not None:
            RaceController.racer_names = racer_names
        
        # Inicializar atributos del sensor IR
        self.ir_sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
        self.lap_detected = False  # Flag para vuelta detectada
        self._irq_enabled = False
        self._last_lap_time = 0  # Para evitar rebotes
        self._lap_debounce_ms = int(SENSOR_DEBOUNCE_TIME * 1000)  # Convertir a ms
        self._finish_time = None  # Marca de tiempo para animación de bandera
        
        # Inicializar controladores solo si no existen
        if RaceController.traffic_light is None:
            RaceController.traffic_light = TrafficLightController()
        if RaceController.display is None:
            RaceController.display = MAX7219DualDisplayConfigurable()
        
        # Inicializar estado de carrera
        RaceController.inicializar_carrera()
        self.enable_sensor_irq()  # Habilitar IRQ al iniciar

    def enable_sensor_irq(self):
        """Habilita la interrupción del sensor IR."""
        if not self._irq_enabled:
            self.ir_sensor.irq(trigger=Pin.IRQ_FALLING, handler=self.on_car_detected)
            self._irq_enabled = True

    def disable_sensor_irq(self):
        """Deshabilita la interrupción del sensor IR."""
        if self._irq_enabled:
            self.ir_sensor.irq(handler=None)
            self._irq_enabled = False

    def on_car_detected(self, pin):
        """Handler de la interrupción del sensor IR."""
        # Solo cuenta si la carrera está en STARTED
        if RaceController.race_state != "STARTED":
            return
        now = ticks_ms()
        # Antirebote simple
        if ticks_diff(now, self._last_lap_time) > self._lap_debounce_ms:
            self.lap_detected = True
            self._last_lap_time = now

    def process_lap(self):
        """Procesa una vuelta detectada: suma, actualiza display y verifica fin de carrera."""
        # Solo cuenta para el corredor 1 (índice 0)
        if RaceController.current_laps is not None and RaceController.max_laps is not None:
            RaceController.current_laps[0] += 1
            # Actualiza el display
            RaceController._show_current_laps()
            # ¿Llegó al máximo?
            if RaceController.current_laps[0] >= RaceController.max_laps:
                RaceController.race_state = "FINISHED"
                RaceController._update_display()
                self._finish_time = ticks_ms()
                RaceController._last_anim_time = self._finish_time  # Inicializa animación
                RaceController._anim_pattern_idx = 0
                self.disable_sensor_irq()

    # Métodos relacionados con sensor IR y vueltas eliminados

    @classmethod
    def inicializar_carrera(cls):
        """Inicializa el estado de la carrera: STOPPED con display titilando y sensor desactivado"""
        # Resetear estado
        cls.race_state = "STOPPED"
        if cls.num_racers is not None:
            cls.current_laps = [0 for _ in range(cls.num_racers)]
        else:
            cls.current_laps = [0]
        
        # Asegurar que el semáforo esté apagado
        if cls.traffic_light:
            cls.traffic_light.race_previous_stop()
            cls.traffic_light.race_stop()
        
        # Configurar display para estado STOPPED
        cls._update_display()
        
        # Desactivar IRQ del sensor si existe instancia
        if cls.instance:
            cls.instance.lap_detected = False
            cls.instance._finish_time = None
            cls.instance.enable_sensor_irq()

    @classmethod
    def _update_display(cls):
        """Actualiza el display según el estado actual de la carrera"""
        if not cls.display:
            return
        if cls.race_state == "STOPPED":
            # Mostrar patrón FULL_CIRCLE (con titileo opcional)
            cls._show_circle_pattern()
        elif cls.race_state == "PREVIOUS":
            # Detener titileo de STOPPED si está activo
            cls.display.stop_pattern_blink()
            # Mostrar cantidad de vueltas totales (sin titileo)
            cls._show_max_laps()
        elif cls.race_state == "STARTED":
            # Detener titileo de STOPPED si está activo
            cls.display.stop_pattern_blink()
            # Mostrar vueltas del corredor 1
            cls._show_current_laps()
        elif cls.race_state == "FINISHED":
            # No escribir nada aquí, la animación la maneja update()
            cls.display.stop_pattern_blink()

    @classmethod
    def _show_circle_pattern(cls):
        """Muestra el patrón FULL_CIRCLE en el display (con titileo opcional)"""
        if not cls.display:
            return
        
        if cls.stopped_blink_enabled:
            # Iniciar titileo continuo usando el display
            cls.display.start_pattern_blink(FULL_CIRCLE, interval=CHECKERED_FLAG_BLINK_INTERVAL)
        else:
            # Detener titileo si está activo
            cls.display.stop_pattern_blink()
            # Mostrar patrón fijo inmediatamente después
            for row in range(8):
                cls.display.write_register_all(row + 1, FULL_CIRCLE[row])

    @classmethod
    def _blink_max_laps(cls):
        """Hace titilar la cantidad de vueltas totales"""
        if not cls.display:
            return
        # Mostrar max_laps
        cls.display.show_two_digits(cls.max_laps)

    @classmethod
    def _show_max_laps(cls):
        """Muestra la cantidad de vueltas totales (sin titileo)"""
        if not cls.display:
            return
        # Mostrar max_laps
        cls.display.show_two_digits(cls.max_laps)

    @classmethod
    def _show_current_laps(cls):
        """Muestra las vueltas actuales del corredor 1"""
        if not cls.display or cls.current_laps is None:
            return
        laps = cls.current_laps[0]  # Corredor 1
        cls.display.show_two_digits(laps)

    @classmethod
    def _show_checkered_flag(cls):
        """Muestra la bandera a cuadros fija"""
        if not cls.display:
            return
        
        # Usar el primer patrón de bandera a cuadros
        checkered_pattern = CHECKERED_FLAG_PATTERNS[0]
        for row in range(8):
            cls.display.write_register_all(row + 1, checkered_pattern[row])

    @classmethod
    def get_race_params(cls):
        """Devuelve los parámetros actuales de la carrera."""
        return {
            'max_laps': cls.max_laps,
            'num_racers': cls.num_racers,
            'racer_names': cls.racer_names,
            'current_laps': cls.current_laps,
            'race_state': cls.race_state
        }

    @classmethod
    def start_race_previous(cls):
        """Inicia la previa de la carrera: semáforo titilando + display mostrando max_laps. Sensor desactivado."""
        # Iniciar titileo del semáforo
        if cls.traffic_light:
            success = cls.traffic_light.race_previous()
            if not success:
                if DEBUG_ENABLED:
                    print("[RACE] ERROR: No se pudo iniciar titileo del semáforo")
                return False
        else:
            if DEBUG_ENABLED:
                print("[RACE] ERROR: traffic_light es None")
            return False
        
        # Cambiar estado y actualizar display
        cls.race_state = "PREVIOUS"
        cls._update_display()
        
        # Desactivar IRQ del sensor si existe instancia
        if cls.instance:
            # cls.instance.disable_sensor_irq() # Eliminado
            pass

        return True

    @classmethod
    def stop_race_previous(cls):
        """Detiene la previa de la carrera: apaga semáforo + vuelve a display titilando. Sensor desactivado."""
        # Detener titileo del semáforo
        if cls.traffic_light:
            success = cls.traffic_light.race_previous_stop()
            if not success and DEBUG_ENABLED:
                print("[RACE] WARNING: No se pudo detener titileo del semáforo")
        else:
            if DEBUG_ENABLED:
                print("[RACE] ERROR: traffic_light es None")
        
        # Volver a estado STOPPED (display titilando)
        cls.race_state = "STOPPED"
        cls._update_display()
        
        # Desactivar IRQ del sensor si existe instancia
        if cls.instance:
            # cls.instance.disable_sensor_irq() # Eliminado
            pass

        return True

    @classmethod
    def start_race(cls):
        """Inicia la carrera: detiene previa, inicia secuencia de semáforo, resetea vueltas."""
        # Verificar si traffic_light existe
        if not cls.traffic_light:
            if DEBUG_ENABLED:
                print("[RACE] ERROR: traffic_light es None")
            return False
        
        # Detener previa si está activa
        if cls.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            cls.stop_race_previous()
            time.sleep(0.2)  # Esperar a que se detenga completamente
        
        # Resetear vueltas
        if cls.num_racers is not None:
            cls.current_laps = [0 for _ in range(cls.num_racers)]
        else:
            cls.current_laps = [0]
        
        # Iniciar secuencia de semáforo (roja -> amarilla -> verde)
        ok = cls.traffic_light.race_start()
        
        if ok:
            # Esperar a que la luz verde esté encendida (máximo RACE_START_TIMEOUT segundos)
            timeout = RACE_START_TIMEOUT
            start_time = time.time()
            while cls.traffic_light.current_state != TRAFFIC_LIGHT_STATE_GREEN:
                if time.time() - start_time > timeout:
                    if DEBUG_ENABLED:
                        print(f"[RACE] TIMEOUT: No se alcanzó luz verde en {timeout} segundos")
                    return False
                time.sleep(0.1)
            
            cls.race_state = "STARTED"
            cls._update_display()
            # Activar IRQ del sensor solo en STARTED
            if cls.instance:
                cls.instance.lap_detected = False
                cls.instance._finish_time = None
                cls.instance.enable_sensor_irq()
            return True
        else:
            if DEBUG_ENABLED:
                print("[RACE] ERROR: No se pudo iniciar la secuencia del semáforo")
        return False

    @classmethod
    def stop_race(cls):
        """Detiene la carrera: reinicializa el estado de la carrera y desactiva el sensor."""
        # Desactivar IRQ del sensor
        if cls.instance:
            cls.instance.lap_detected = False
            cls.instance._finish_time = None
            cls.instance.disable_sensor_irq()
        # Reutilizar el inicializador para resetear todo
        cls.inicializar_carrera()
        
        return True

    @classmethod
    def set_race_state(cls, state):
        """Cambia el estado de la carrera."""
        if state in ["STOPPED", "PREVIOUS", "STARTED", "FINISHED"]:
            cls.race_state = state
            cls._update_display()
            if cls.instance:
                if state == "STARTED":
                    cls.instance.enable_sensor_irq()
                else:
                    cls.instance.disable_sensor_irq()
            return True
        else:
            if DEBUG_ENABLED:
                print(f"[RACE] ERROR: Estado inválido: {state}")
        return False

    @classmethod
    def set_stopped_blink(cls, enabled):
        """Habilita o deshabilita el titileo del patrón en estado STOPPED"""
        cls.stopped_blink_enabled = enabled
        
        # Actualizar display si está en estado STOPPED
        if cls.race_state == "STOPPED":
            cls._update_display()

    @classmethod
    def get_stopped_blink_status(cls):
        """Retorna el estado actual del titileo en STOPPED"""
        return cls.stopped_blink_enabled

    @classmethod
    def update(cls):
        """Actualiza el estado del controlador (debe ser llamado desde el bucle principal)"""
        if cls.traffic_light:
            cls.traffic_light.update_blinking()
        if cls.display:
            cls.display.update_pattern_blink()
        
        # Procesar vuelta detectada
        if cls.instance and cls.instance.lap_detected:
            cls.instance.lap_detected = False
            cls.instance.process_lap()
        
        # Si está en FINISHED, mostrar bandera a cuadros durante FLAG_ANIMATION_DURATION segundos
        if cls.race_state == "FINISHED" and cls.instance and cls.instance._finish_time:
            now = ticks_ms()
            elapsed_ms = ticks_diff(now, cls.instance._finish_time)
            elapsed = elapsed_ms / 1000.0
            if elapsed < FLAG_ANIMATION_DURATION:
                # Animación regular: alternar patrón cada CHECKERED_FLAG_BLINK_INTERVAL segundos
                if cls._last_anim_time is None:
                    cls._last_anim_time = now
                if ticks_diff(now, cls._last_anim_time) >= int(CHECKERED_FLAG_BLINK_INTERVAL * 1000):
                    cls._anim_pattern_idx = (cls._anim_pattern_idx + 1) % 2
                    cls._last_anim_time = now
                pattern_idx = cls._anim_pattern_idx
                pattern = CHECKERED_FLAG_PATTERNS[pattern_idx]
                for row in range(8):
                    cls.display.write_register_all(row + 1, pattern[row])
            else:
                cls.inicializar_carrera()

    # El método poll_sensor_and_update_laps ya no es necesario con el modelo event-driven, pero se puede dejar para compatibilidad o debug.
    def poll_sensor_and_update_laps(self):
        """
        Método obsoleto: ya no se usa con el modelo event-driven basado en interrupciones.
        Se deja vacío para compatibilidad con código legado.
        """
        pass 