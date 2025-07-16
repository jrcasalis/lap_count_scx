"""
Recurso MCP para el semáforo LED
"""

from typing import Dict, Any
from schemas.traffic_light import TrafficLightStatus, TrafficLightConfig, TrafficLightState

class TrafficLightResource:
    """Recurso MCP para el semáforo LED"""
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del semáforo"""
        return {
            "resource_id": "traffic_light",
            "name": "Semáforo LED",
            "description": "Semáforo para control de salida de carrera",
            "data": {
                "current_state": "off",
                "red_pin": 11,
                "yellow_pin": 12,
                "green_pin": 13,
                "is_connected": True,
                "blink_interval": 0.5,
                "pwm_freq": 1000,
                "duty_on": 1023,
                "duty_off": 0
            },
            "schema": {
                "current_state": "string - Estado actual (off|blinking|red|yellow|green)",
                "red_pin": "int - Pin GPIO de luz roja",
                "yellow_pin": "int - Pin GPIO de luz amarilla", 
                "green_pin": "int - Pin GPIO de luz verde",
                "is_connected": "bool - Si el semáforo está conectado",
                "blink_interval": "float - Intervalo de titileo en segundos",
                "pwm_freq": "int - Frecuencia PWM en Hz",
                "duty_on": "int - Duty cycle máximo (100%)",
                "duty_off": "int - Duty cycle mínimo (0%)"
            },
            "technical_details": {
                "voltage": "5V (con compensación a 3.3V)",
                "pwm_frequency": "1000Hz",
                "blink_interval": "0.5s",
                "red_duration": "3.0s",
                "yellow_duration": "3.0s",
                "green_duration": "indefinido"
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Obtiene la configuración del semáforo"""
        return {
            "resource_id": "traffic_light_config",
            "name": "Configuración del Semáforo",
            "description": "Configuración del semáforo LED",
            "data": {
                "red_pin": 11,
                "yellow_pin": 12,
                "green_pin": 13,
                "blink_interval": 0.5,
                "red_duration": 3.0,
                "yellow_duration": 3.0,
                "green_duration": 0,
                "pwm_freq": 1000,
                "duty_on": 1023,
                "duty_off": 0,
                "voltage_compensation": True
            },
            "schema": {
                "red_pin": "int - Pin GPIO de luz roja",
                "yellow_pin": "int - Pin GPIO de luz amarilla",
                "green_pin": "int - Pin GPIO de luz verde",
                "blink_interval": "float - Intervalo de titileo en segundos",
                "red_duration": "float - Duración de luz roja en segundos",
                "yellow_duration": "float - Duración de luz amarilla en segundos",
                "green_duration": "float - Duración de luz verde en segundos (0=indefinido)",
                "pwm_freq": "int - Frecuencia PWM en Hz",
                "duty_on": "int - Duty cycle máximo (100%)",
                "duty_off": "int - Duty cycle mínimo (0%)",
                "voltage_compensation": "bool - Habilitar compensación de voltaje"
            }
        } 