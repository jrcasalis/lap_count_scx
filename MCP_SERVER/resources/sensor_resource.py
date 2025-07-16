"""
Recurso MCP para el sensor IR TCRT5000
"""

from typing import Dict, Any
from schemas.sensor import SensorStatus, SensorConfig, SensorType

class SensorResource:
    """Recurso MCP para el sensor IR"""
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del sensor"""
        return {
            "resource_id": "sensor",
            "name": "Sensor IR TCRT5000",
            "description": "Sensor infrarrojo para detectar vueltas",
            "data": {
                "pin": 16,
                "sensor_type": "TCRT5000",
                "is_active": True,
                "is_connected": True,
                "last_detection": None,
                "detection_count": 0
            },
            "schema": {
                "pin": "int - Pin GPIO del sensor",
                "sensor_type": "string - Tipo de sensor (TCRT5000)",
                "is_active": "bool - Si el sensor está activo",
                "is_connected": "bool - Si el sensor está conectado",
                "last_detection": "float|null - Timestamp de última detección",
                "detection_count": "int - Número total de detecciones"
            },
            "technical_details": {
                "pin": 16,
                "type": "TCRT5000",
                "voltage": "3.3V",
                "detection_range": "2-15mm",
                "response_time": "<1ms",
                "debounce_time": "0.1s"
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Obtiene la configuración del sensor"""
        return {
            "resource_id": "sensor_config",
            "name": "Configuración del Sensor",
            "description": "Configuración del sensor IR TCRT5000",
            "data": {
                "pin": 16,
                "sensor_type": "TCRT5000",
                "debounce_time": 0.1,
                "auto_increment": True
            },
            "schema": {
                "pin": "int - Pin GPIO del sensor",
                "sensor_type": "string - Tipo de sensor",
                "debounce_time": "float - Tiempo de debounce en segundos",
                "auto_increment": "bool - Incrementar automáticamente con sensor"
            }
        } 