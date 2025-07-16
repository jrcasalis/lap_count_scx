"""
Esquemas para datos del display MAX7219
"""

from typing import Optional, List
from enum import Enum

class DisplayOrientation(str, Enum):
    """Orientaciones del display"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

class DisplayStatus:
    """Estado del display MAX7219"""
    def __init__(self,
                 num_modules: int = 2,
                 brightness: int = 8,
                 rotation: int = 90,
                 orientation: DisplayOrientation = DisplayOrientation.VERTICAL,
                 is_connected: bool = True,
                 current_pattern: Optional[List[List[int]]] = None,
                 is_blinking: bool = False,
                 blink_interval: float = 0.5):
        self.num_modules = num_modules
        self.brightness = brightness
        self.rotation = rotation
        self.orientation = orientation
        self.is_connected = is_connected
        self.current_pattern = current_pattern
        self.is_blinking = is_blinking
        self.blink_interval = blink_interval

class DisplayConfig:
    """Configuración del display"""
    def __init__(self,
                 din_pin: int = 3,
                 cs_pin: int = 5,
                 clk_pin: int = 2,
                 num_modules: int = 2,
                 brightness: int = 8,
                 rotation: int = 90,
                 orientation: DisplayOrientation = DisplayOrientation.VERTICAL):
        self.din_pin = din_pin
        self.cs_pin = cs_pin
        self.clk_pin = clk_pin
        self.num_modules = num_modules
        self.brightness = brightness
        self.rotation = rotation
        self.orientation = orientation 