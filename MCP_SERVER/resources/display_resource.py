"""
Recurso MCP para el display MAX7219
"""

from typing import Dict, Any
from schemas.display import DisplayStatus, DisplayConfig, DisplayOrientation

class DisplayResource:
    """Recurso MCP para el display MAX7219"""
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del display"""
        return {
            "resource_id": "display",
            "name": "Display MAX7219",
            "description": "Display LED para mostrar información de carrera",
            "data": {
                "num_modules": 2,
                "brightness": 8,
                "rotation": 90,
                "orientation": "vertical",
                "is_connected": True,
                "current_pattern": None,
                "is_blinking": False,
                "blink_interval": 0.5
            },
            "schema": {
                "num_modules": "int - Número de módulos en cascada",
                "brightness": "int - Brillo (0-15)",
                "rotation": "int - Rotación (0, 90, 180, 270)",
                "orientation": "string - Orientación (horizontal|vertical)",
                "is_connected": "bool - Si el display está conectado",
                "current_pattern": "array|null - Patrón actual mostrado",
                "is_blinking": "bool - Si está titilando",
                "blink_interval": "float - Intervalo de titileo en segundos"
            },
            "technical_details": {
                "din_pin": 3,
                "cs_pin": 5,
                "clk_pin": 2,
                "voltage": "3.3V",
                "resolution": "8x8 por módulo",
                "max_modules": 8,
                "max_brightness": 15
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Obtiene la configuración del display"""
        return {
            "resource_id": "display_config",
            "name": "Configuración del Display",
            "description": "Configuración del display MAX7219",
            "data": {
                "din_pin": 3,
                "cs_pin": 5,
                "clk_pin": 2,
                "num_modules": 2,
                "brightness": 8,
                "rotation": 90,
                "orientation": "vertical"
            },
            "schema": {
                "din_pin": "int - Pin de datos (MOSI)",
                "cs_pin": "int - Pin de chip select",
                "clk_pin": "int - Pin de reloj (SCK)",
                "num_modules": "int - Número de módulos en cascada",
                "brightness": "int - Brillo (0-15)",
                "rotation": "int - Rotación (0, 90, 180, 270)",
                "orientation": "string - Orientación (horizontal|vertical)"
            }
        } 