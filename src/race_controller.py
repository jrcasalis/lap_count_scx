"""
Controlador de Carrera - Refactorizado para soportar múltiples corredores
"""

from traffic_light_controller import TrafficLightController
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
from config import TRAFFIC_LIGHT_STATE_BLINKING, TRAFFIC_LIGHT_STATE_GREEN, DEBUG_ENABLED
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
    # Variables globales al controlador (de clase)
    max_laps = 15
    num_racers = 2
    racer_names = ["Piloto 1", "Piloto 2"]
    current_laps = [0, 0]
    traffic_light = None
    display = None
    race_state = "STOPPED"  # STOPPED | PREVIOUS | STARTED | FINISHED
    stopped_blink_enabled = True  # Controla si el patrón titila en estado STOPPED
    instance = None  # Referencia a la instancia actual para acceso desde métodos de clase
    _last_anim_time = None  # Para animación regular
    _anim_pattern_idx = 0

    def __init__(self, max_laps=15, num_racers=1, racer_names=None):
        """
        Inicializa el controlador de carrera con parámetros básicos.
        max_laps: cantidad de vueltas para finalizar la carrera
        num_racers: cantidad de corredores
        racer_names: lista de nombres de los corredores
        """
        if DEBUG_ENABLED:
            print("[RACE] Inicializando RaceController...")
        RaceController.instance = self  # Guardar referencia a la instancia actual
        self.max_laps = max_laps
        self.num_racers = num_racers
        if racer_names:
            self.racer_names = racer_names
        else:
            self.racer_names = [f"Piloto {i+1}" for i in range(num_racers)]
        self.current_laps = [0 for _ in range(num_racers)]
        self.race_state = 'STOPPED'
        # Inicializar atributos del sensor IR primero
        self.ir_sensor = Pin(16, Pin.IN, Pin.PULL_UP)
        self.lap_detected = False  # Flag para vuelta detectada
        self._irq_enabled = False
        self._last_lap_time = 0  # Para evitar rebotes
        self._lap_debounce_ms = 200  # Tiempo mínimo entre vueltas (ms)
        self._finish_time = None  # Marca de tiempo para animación de bandera
        # Sensor IR y atributos relacionados eliminados
        if RaceController.traffic_light is None:
            if DEBUG_ENABLED:
                print("[RACE] Creando TrafficLightController...")
            RaceController.traffic_light = TrafficLightController()
            if DEBUG_ENABLED:
                print("[RACE] TrafficLightController creado")
        if RaceController.display is None:
            if DEBUG_ENABLED:
                print("[RACE] Creando MAX7219DualDisplayConfigurable...")
            RaceController.display = MAX7219DualDisplayConfigurable()
            if DEBUG_ENABLED:
                print("[RACE] Display creado")
        # Inicializar estado de carrera
        RaceController.inicializar_carrera()
        if DEBUG_ENABLED:
            print(f"[RACE] RaceController inicializado - Estado: {RaceController.race_state}")
        self.enable_sensor_irq()  # Habilitar IRQ al iniciar

    def enable_sensor_irq(self):
        """Habilita la interrupción del sensor IR."""
        if not self._irq_enabled:
            self.ir_sensor.irq(trigger=Pin.IRQ_FALLING, handler=self.on_car_detected)
            self._irq_enabled = True
            if DEBUG_ENABLED:
                print("[RACE] IRQ del sensor IR habilitada")

    def disable_sensor_irq(self):
        """Deshabilita la interrupción del sensor IR."""
        if self._irq_enabled:
            self.ir_sensor.irq(handler=None)
            self._irq_enabled = False
            if DEBUG_ENABLED:
                print("[RACE] IRQ del sensor IR deshabilitada")

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
            if DEBUG_ENABLED:
                print("[RACE] Vuelta detectada por sensor IR")

    def process_lap(self):
        """Procesa una vuelta detectada: suma, actualiza display y verifica fin de carrera."""
        # Solo cuenta para el corredor 1 (índice 0)
        RaceController.current_laps[0] += 1
        if DEBUG_ENABLED:
            print(f"[RACE] Vuelta sumada. Total: {RaceController.current_laps[0]}")
        # Actualiza el display
        RaceController._show_current_laps()
        # ¿Llegó al máximo?
        if RaceController.current_laps[0] >= RaceController.max_laps:
            if DEBUG_ENABLED:
                print("[RACE] Máximo de vueltas alcanzado. Finalizando carrera...")
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
        if DEBUG_ENABLED:
            print("[RACE] Inicializando estado de carrera...")
        
        # Resetear estado
        cls.race_state = "STOPPED"
        cls.current_laps = [0 for _ in range(cls.num_racers)]
        
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
        if DEBUG_ENABLED:
            print(f"[RACE] Carrera inicializada - Estado: {cls.race_state}")

    @classmethod
    def _update_display(cls):
        """Actualiza el display según el estado actual de la carrera"""
        if not cls.display:
            return
        if DEBUG_ENABLED:
            print(f"[RACE] Actualizando display - Estado: {cls.race_state}")
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
            if DEBUG_ENABLED:
                print("[RACE] FINISHED: Animación de bandera a cuadros la maneja update()")

    @classmethod
    def _show_circle_pattern(cls):
        """Muestra el patrón FULL_CIRCLE en el display (con titileo opcional)"""
        if not cls.display:
            return
        if DEBUG_ENABLED:
            print(f"[RACE] Mostrando patrón FULL_CIRCLE (titileo: {cls.stopped_blink_enabled})")
        
        if cls.stopped_blink_enabled:
            # Iniciar titileo continuo usando el display
            cls.display.start_pattern_blink(FULL_CIRCLE, interval=0.5)
        else:
            # Detener titileo si está activo
            cls.display.stop_pattern_blink()
            # Mostrar patrón fijo inmediatamente después
            for row in range(8):
                cls.display.write_register_all(row + 1, FULL_CIRCLE[row])
            if DEBUG_ENABLED:
                print("[RACE] Patrón FULL_CIRCLE mostrado fijo")

    @classmethod
    def _blink_max_laps(cls):
        """Hace titilar la cantidad de vueltas totales"""
        if not cls.display:
            return
        if DEBUG_ENABLED:
            print(f"[RACE] Titilando max_laps: {cls.max_laps}")
        
        # Mostrar max_laps
        cls.display.show_two_digits(cls.max_laps)

    @classmethod
    def _show_max_laps(cls):
        """Muestra la cantidad de vueltas totales (sin titileo)"""
        if not cls.display:
            return
        if DEBUG_ENABLED:
            print(f"[RACE] Mostrando max_laps: {cls.max_laps}")
        
        # Mostrar max_laps
        cls.display.show_two_digits(cls.max_laps)

    @classmethod
    def _show_current_laps(cls):
        """Muestra las vueltas actuales del corredor 1"""
        if not cls.display:
            return
        laps = cls.current_laps[0]  # Corredor 1
        if DEBUG_ENABLED:
            print(f"[RACE] Mostrando vueltas corredor 1: {laps}")
        
        cls.display.show_two_digits(laps)

    @classmethod
    def _show_checkered_flag(cls):
        """Muestra la bandera a cuadros fija"""
        if not cls.display:
            return
        if DEBUG_ENABLED:
            print("[RACE] Mostrando bandera a cuadros")
        
        # Usar el primer patrón de bandera a cuadros
        checkered_pattern = CHECKERED_FLAG_PATTERNS[0]
        for row in range(8):
            cls.display.write_register_all(row + 1, checkered_pattern[row])

    @classmethod
    def get_race_params(cls):
        """Devuelve los parámetros actuales de la carrera."""
        if DEBUG_ENABLED:
            print(f"[RACE] Obteniendo parámetros - Estado actual: {cls.race_state}")
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
        if DEBUG_ENABLED:
            print(f"[RACE] Iniciando previa - Estado actual: {cls.race_state}")
        
        # Iniciar titileo del semáforo
        if cls.traffic_light:
            if DEBUG_ENABLED:
                print("[RACE] Iniciando titileo del semáforo...")
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

        if DEBUG_ENABLED:
            print(f"[RACE] Previa iniciada - Estado: {cls.race_state}")
            print("[RACE] Semáforo titilando + Display mostrando max_laps")
        return True

    @classmethod
    def stop_race_previous(cls):
        """Detiene la previa de la carrera: apaga semáforo + vuelve a display titilando. Sensor desactivado."""
        if DEBUG_ENABLED:
            print(f"[RACE] Deteniendo previa - Estado actual: {cls.race_state}")
        
        # Detener titileo del semáforo
        if cls.traffic_light:
            if DEBUG_ENABLED:
                print("[RACE] Deteniendo titileo del semáforo...")
            success = cls.traffic_light.race_previous_stop()
            if not success:
                if DEBUG_ENABLED:
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

        if DEBUG_ENABLED:
            print(f"[RACE] Previa detenida - Estado: {cls.race_state}")
            print("[RACE] Semáforo apagado + Display titilando")
        return True

    @classmethod
    def start_race(cls):
        """Inicia la carrera: detiene previa, inicia secuencia de semáforo, resetea vueltas."""
        if DEBUG_ENABLED:
            print(f"[RACE] Iniciando carrera - Estado actual: {cls.race_state}")
        
        # Verificar si traffic_light existe
        if not cls.traffic_light:
            if DEBUG_ENABLED:
                print("[RACE] ERROR: traffic_light es None")
            return False
        
        # Detener previa si está activa
        if cls.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[RACE] Previa activa detectada, deteniendo...")
            cls.stop_race_previous()
            time.sleep(0.2)  # Esperar a que se detenga completamente
            if DEBUG_ENABLED:
                print("[RACE] Previa detenida, espera completada")
        else:
            if DEBUG_ENABLED:
                print(f"[RACE] No hay previa activa. Estado del semáforo: {cls.traffic_light.current_state}")
        
        # Resetear vueltas
        cls.current_laps = [0 for _ in range(cls.num_racers)]
        if DEBUG_ENABLED:
            print(f"[RACE] Vueltas reseteadas: {cls.current_laps}")
        
        # Iniciar secuencia de semáforo (roja -> amarilla -> verde)
        if DEBUG_ENABLED:
            print("[RACE] Llamando a traffic_light.race_start()...")
        ok = cls.traffic_light.race_start()
        if DEBUG_ENABLED:
            print(f"[RACE] Resultado de race_start: {ok}")
        
        if ok:
            if DEBUG_ENABLED:
                print("[RACE] Esperando a que la luz verde esté encendida...")
            # Esperar a que la luz verde esté encendida (máximo 10 segundos)
            timeout = 10
            start_time = time.time()
            while cls.traffic_light.current_state != TRAFFIC_LIGHT_STATE_GREEN:
                if time.time() - start_time > timeout:
                    if DEBUG_ENABLED:
                        print(f"[RACE] TIMEOUT: No se alcanzó luz verde en {timeout} segundos")
                    return False
                # Todos los prints relacionados con el estado del semáforo han sido comentados para limpiar la consola
                time.sleep(0.1)
            
            cls.race_state = "STARTED"
            cls._update_display()
            # Activar IRQ del sensor solo en STARTED
            if cls.instance:
                cls.instance.lap_detected = False
                cls.instance._finish_time = None
                cls.instance.enable_sensor_irq()
            if DEBUG_ENABLED:
                print(f"[RACE] ¡Luz verde alcanzada! Estado cambiado a: {cls.race_state}")
            return True
        else:
            if DEBUG_ENABLED:
                print("[RACE] ERROR: No se pudo iniciar la secuencia del semáforo")
        return False

    @classmethod
    def stop_race(cls):
        """Detiene la carrera: reinicializa el estado de la carrera y desactiva el sensor."""
        if DEBUG_ENABLED:
            print(f"[RACE] Deteniendo carrera - Estado actual: {cls.race_state}")
        
        # Desactivar IRQ del sensor
        if cls.instance:
            cls.instance.lap_detected = False
            cls.instance._finish_time = None
            cls.instance.disable_sensor_irq()
        # Reutilizar el inicializador para resetear todo
        cls.inicializar_carrera()
        
        if DEBUG_ENABLED:
            print("[RACE] Carrera detenida y reinicializada")
        return True

    @classmethod
    def set_race_state(cls, state):
        """Cambia el estado de la carrera."""
        if DEBUG_ENABLED:
            print(f"[RACE] Cambiando estado de {cls.race_state} a {state}")
        
        if state in ["STOPPED", "PREVIOUS", "STARTED", "FINISHED"]:
            cls.race_state = state
            cls._update_display()
            if DEBUG_ENABLED:
                print(f"[RACE] Estado cambiado exitosamente a: {cls.race_state}")
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
        if DEBUG_ENABLED:
            print(f"[RACE] Titileo en STOPPED {'habilitado' if enabled else 'deshabilitado'}")
        
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
        if DEBUG_ENABLED:
            print(f"[RACE] Update() - Estado: {cls.race_state}")
        
        if cls.traffic_light:
            cls.traffic_light.update_blinking()
        if cls.display:
            cls.display.update_pattern_blink()
            # Debug adicional para verificar el estado del titileo
            # if cls.display.is_blinking():
            #     if DEBUG_ENABLED:
            #         print(f"[RACE] Display titilando activamente - blink_state: {cls.display.blink_state}") 
        # Procesar vuelta detectada
        if cls.instance and cls.instance.lap_detected:
            cls.instance.lap_detected = False
            cls.instance.process_lap()
        # Si está en FINISHED, mostrar bandera a cuadros durante 15 segundos
        if cls.race_state == "FINISHED" and cls.instance and cls.instance._finish_time:
            now = ticks_ms()
            elapsed_ms = ticks_diff(now, cls.instance._finish_time)
            elapsed = elapsed_ms / 1000.0
            if elapsed < 15:
                # Animación regular: alternar patrón cada 0.5s
                if cls._last_anim_time is None:
                    cls._last_anim_time = now
                if ticks_diff(now, cls._last_anim_time) >= 500:
                    cls._anim_pattern_idx = (cls._anim_pattern_idx + 1) % 2
                    cls._last_anim_time = now
                pattern_idx = cls._anim_pattern_idx
                pattern = CHECKERED_FLAG_PATTERNS[pattern_idx]
                if DEBUG_ENABLED:
                    print(f"[RACE][ANIM] t={elapsed:.2f}s patrón={pattern_idx}")
                for row in range(8):
                    cls.display.write_register_all(row + 1, pattern[row])
            else:
                if DEBUG_ENABLED:
                    print("[RACE] Animación de bandera finalizada. Reseteando carrera...")
                cls.inicializar_carrera()

    # El método poll_sensor_and_update_laps ya no es necesario con el modelo event-driven, pero se puede dejar para compatibilidad o debug.
    def poll_sensor_and_update_laps(self):
        """
        Método obsoleto: ya no se usa con el modelo event-driven basado en interrupciones.
        Se deja vacío para compatibilidad con código legado.
        """
        pass 