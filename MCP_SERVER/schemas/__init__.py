"""
Esquemas de datos para el MCP Server
"""

from .race import RaceStatus, RaceAction, RaceConfig
from .sensor import SensorStatus, SensorConfig
from .display import DisplayStatus, DisplayConfig
from .traffic_light import TrafficLightStatus, TrafficLightConfig
from .system import SystemInfo, SystemStatus

__all__ = [
    "RaceStatus", "RaceAction", "RaceConfig",
    "SensorStatus", "SensorConfig", 
    "DisplayStatus", "DisplayConfig",
    "TrafficLightStatus", "TrafficLightConfig",
    "SystemInfo", "SystemStatus"
] 