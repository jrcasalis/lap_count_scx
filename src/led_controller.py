"""
Controlador LED para Raspberry Pi Pico 2W
Maneja el control del LED conectado al pin especificado
"""

from machine import Pin
from max7219_display import MAX7219Display
from config import MAX7219_DIN_PIN, MAX7219_CS_PIN, MAX7219_CLK_PIN

class LEDController:
    def __init__(self, pin_number):
        """
        Inicializa el controlador LED
        
        Args:
            pin_number (int): Número del pin GPIO donde está conectado el LED
        """
        self.pin_number = pin_number  # Guardar el número de pin
        self.pin = Pin(pin_number, Pin.OUT)
        self.is_on = False
        
        # Inicializar display MAX7219
        self.display = MAX7219Display(MAX7219_DIN_PIN, MAX7219_CS_PIN, MAX7219_CLK_PIN)
        
        self.turn_off()  # Inicializar apagado
        
    def turn_on(self):
        """Enciende el LED"""
        self.pin.value(1)
        self.is_on = True
        self.display.display_letter('R')  # Mostrar 'R' en el display
        print("LED encendido")
        
    def turn_off(self):
        """Apaga el LED"""
        self.pin.value(0)
        self.is_on = False
        self.display.display_letter('N')  # Mostrar 'N' en el display
        print("LED apagado")
        
    def toggle(self):
        """Cambia el estado del LED (encendido ↔ apagado)"""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
            
    def get_status(self):
        """Retorna el estado actual del LED"""
        return {
            "is_on": self.is_on,
            "pin": self.pin_number  # Usar el atributo guardado
        }
        
    def cleanup(self):
        """Limpia los recursos del LED"""
        self.turn_off()
        self.display.cleanup()  # Limpiar display
        print("LED controller cleanup completado") 