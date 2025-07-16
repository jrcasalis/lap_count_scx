"""
Esquemas para datos del sistema
"""

from typing import Dict, Any, Optional
from datetime import datetime

class SystemInfo:
    """Información del sistema"""
    def __init__(self,
                 name: str = "Controlador de Carrera Scalextric",
                 version: str = "1.0.0",
                 description: str = "Sistema de control de carrera para pista Scalextric",
                 platform: str = "Raspberry Pi Pico 2W",
                 firmware: str = "MicroPython",
                 api_version: str = "1.0.0",
                 uptime: Optional[float] = None,
                 memory_usage: Optional[Dict[str, Any]] = None,
                 cpu_usage: Optional[float] = None):
        self.name = name
        self.version = version
        self.description = description
        self.platform = platform
        self.firmware = firmware
        self.api_version = api_version
        self.uptime = uptime
        self.memory_usage = memory_usage
        self.cpu_usage = cpu_usage
        self.timestamp = datetime.now().isoformat()

class SystemStatus:
    """Estado del sistema"""
    def __init__(self,
                 is_online: bool = True,
                 is_healthy: bool = True,
                 wifi_connected: bool = True,
                 wifi_ip: Optional[str] = None,
                 server_running: bool = True,
                 last_error: Optional[str] = None,
                 error_count: int = 0,
                 request_count: int = 0,
                 last_request: Optional[datetime] = None):
        self.is_online = is_online
        self.is_healthy = is_healthy
        self.wifi_connected = wifi_connected
        self.wifi_ip = wifi_ip
        self.server_running = server_running
        self.last_error = last_error
        self.error_count = error_count
        self.request_count = request_count
        self.last_request = last_request
        self.timestamp = datetime.now().isoformat() 