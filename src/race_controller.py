"""
Controlador Principal de Carrera
Integra contador de vueltas, display y LED de forma modular
"""

from lap_counter import LapCounter
from number_display import NumberDisplay
from max7219_display import MAX7219Display
from led_controller import LEDController
from config import MAX7219_DIN_PIN, MAX7219_CS_PIN, MAX7219_CLK_PIN, LED_PIN_RED

class RaceController:
    def __init__(self, max_laps=10, brightness_normal=8, brightness_flag=4):
        """
        Inicializa el controlador principal de carrera
        Args:
            max_laps (int): Número máximo de vueltas
            brightness_normal (int): Brillo normal del display (0-15)
            brightness_flag (int): Brillo para la bandera a cuadros (0-15)
        """
        self.max_laps = max_laps
        self.brightness_normal = brightness_normal
        self.brightness_flag = brightness_flag
        # Inicializar contador de vueltas
        self.lap_counter = LapCounter(max_laps)
        # Inicializar display MAX7219
        self.max7219_display = MAX7219Display(MAX7219_DIN_PIN, MAX7219_CS_PIN, MAX7219_CLK_PIN)
        self.max7219_display.set_brightness(self.brightness_normal)
        # Inicializar display de números
        self.number_display = NumberDisplay(self.max7219_display)
        # Inicializar controlador LED
        self.led_controller = LEDController(LED_PIN_RED)
        # Mostrar estado inicial
        self.update_display()

    def increment_lap(self):
        prev_lap = self.lap_counter.get_current_laps()
        success = self.lap_counter.increment_lap()
        new_lap = self.lap_counter.get_current_laps()
        if success:
            if new_lap == 0:
                self.number_display.display_number(0)
            else:
                self.number_display.scroll_number_horizontal(prev_lap, new_lap, delay=0.02)
            print(f"Vuelta {new_lap}/{self.lap_counter.get_max_laps()}")
            if self.lap_counter.is_race_completed():
                print("¡Carrera completada!")
                self.show_completion_message()
        else:
            print("Ya se alcanzó el número máximo de vueltas")
        return success

    def show_completion_message(self):
        """Muestra bandera a cuadros titilando y luego fija, con brillo atenuado"""
        self.max7219_display.set_brightness(self.brightness_flag)
        self.max7219_display.show_checkered_flag(
            blink_time=10, blink_interval=0.5, brightness=self.brightness_flag, keep_on=True)

    def reset_race(self):
        self.lap_counter.reset_counter()
        self.led_controller.turn_off()
        self.max7219_display.set_brightness(self.brightness_normal)
        self.update_display()
        print("Carrera reiniciada")

    def update_display(self):
        current_laps = self.lap_counter.get_current_laps()
        max_laps = self.lap_counter.get_max_laps()
        if current_laps == 0:
            self.number_display.display_number(0)
        elif self.lap_counter.is_race_completed():
            self.max7219_display.show_checkered_flag(
                blink_time=0, blink_interval=0.5, brightness=self.brightness_flag, keep_on=True)
        else:
            self.number_display.display_progress(current_laps, max_laps)

    def get_race_status(self):
        """Retorna el estado completo de la carrera"""
        status = self.lap_counter.get_status()
        status.update({
            "led_status": self.led_controller.get_status()
        })
        return status

    def set_max_laps(self, max_laps):
        """
        Cambia el número máximo de vueltas
        
        Args:
            max_laps (int): Nuevo número máximo de vueltas
        """
        self.lap_counter.set_max_laps(max_laps)
        self.update_display()
        print(f"Número máximo de vueltas cambiado a: {max_laps}")

    def cleanup(self):
        """Limpia todos los recursos"""
        self.led_controller.cleanup()
        self.max7219_display.cleanup()
        print("Race controller cleanup completado") 