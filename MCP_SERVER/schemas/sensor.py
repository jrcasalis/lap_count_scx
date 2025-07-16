"""
Esquemas para datos del sensor IR TCRT5000
"""

from typing import Optional
from enum import Enum

class SensorType(str, Enum):
    """Tipos de sensor disponibles"""
    TCRT5000 = "TCRT5000"
    IR_SENSOR = "IR_SENSOR"

class SensorStatus:
    """Estado del sensor IR"""
    def __init__(self, 
                 pin: int = 16,
                 sensor_type: SensorType = SensorType.TCRT5000,
                 is_active: bool = True,
                 is_connected: bool = True,
                 last_detection: Optional[float] = None,
                 detection_count: int = 0):
        self.pin = pin
        self.sensor_type = sensor_type
        self.is_active = is_active
        self.is_connected = is_connected
        self.last_detection = last_detection
        self.detection_count = detection_count

class SensorConfig:
    """Configuración del sensor"""
    def __init__(self,
                 pin: int = 16,
                 sensor_type: SensorType = SensorType.TCRT5000,
                 debounce_time: float = 0.1,
                 auto_increment: bool = True):
        self.pin = pin
        self.sensor_type = sensor_type
        self.debounce_time = debounce_time
        self.auto_increment = auto_increment 