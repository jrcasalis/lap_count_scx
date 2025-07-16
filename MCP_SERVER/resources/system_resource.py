"""
Recurso MCP para información del sistema
"""

from typing import Dict, Any
from schemas.system import SystemInfo, SystemStatus

class SystemResource:
    """Recurso MCP para información del sistema"""
    
    def get_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema"""
        return {
            "resource_id": "system_info",
            "name": "Información del Sistema",
            "description": "Información general del sistema de control de carrera",
            "data": {
                "name": "Controlador de Carrera Scalextric",
                "version": "1.0.0",
                "description": "Sistema de control de carrera para pista Scalextric",
                "platform": "Raspberry Pi Pico 2W",
                "firmware": "MicroPython",
                "api_version": "1.0.0",
                "uptime": None,
                "memory_usage": None,
                "cpu_usage": None
            },
            "schema": {
                "name": "string - Nombre del sistema",
                "version": "string - Versión del software",
                "description": "string - Descripción del sistema",
                "platform": "string - Plataforma hardware",
                "firmware": "string - Firmware utilizado",
                "api_version": "string - Versión de la API",
                "uptime": "float|null - Tiempo de funcionamiento en segundos",
                "memory_usage": "object|null - Información de uso de memoria",
                "cpu_usage": "float|null - Uso de CPU en porcentaje"
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del sistema"""
        return {
            "resource_id": "system_status",
            "name": "Estado del Sistema",
            "description": "Estado actual del sistema",
            "data": {
                "is_online": True,
                "is_healthy": True,
                "wifi_connected": True,
                "wifi_ip": None,
                "server_running": True,
                "last_error": None,
                "error_count": 0,
                "request_count": 0,
                "last_request": None
            },
            "schema": {
                "is_online": "bool - Si el sistema está en línea",
                "is_healthy": "bool - Si el sistema está funcionando correctamente",
                "wifi_connected": "bool - Si WiFi está conectado",
                "wifi_ip": "string|null - Dirección IP WiFi",
                "server_running": "bool - Si el servidor web está ejecutándose",
                "last_error": "string|null - Último error ocurrido",
                "error_count": "int - Número total de errores",
                "request_count": "int - Número total de solicitudes",
                "last_request": "string|null - Timestamp de última solicitud"
            }
        }
    
    def get_api_documentation(self) -> Dict[str, Any]:
        """Obtiene la documentación de la API"""
        return {
            "resource_id": "api_documentation",
            "name": "Documentación de la API",
            "description": "Documentación completa de la API de Scalextric",
            "data": {
                "title": "API de Contador de Vueltas Scalextric",
                "description": "Sistema de control de carrera para pista Scalextric con sensor IR y display LED",
                "version": "1.0.0",
                "endpoints": {
                    "GET /api/status": "Obtiene el estado actual de la carrera",
                    "GET /start_race": "Inicia una nueva carrera",
                    "GET /stop_race": "Detiene la carrera actual",
                    "GET /reset": "Resetea los parámetros de la carrera",
                    "GET /start_previous": "Inicia la previa",
                    "GET /stop_previous": "Detiene la previa"
                },
                "components": {
                    "sensor": "Sensor IR TCRT5000 en pin 16",
                    "display": "Display MAX7219 en pines 3, 5, 2",
                    "traffic_light": "Semáforo LED en pines 11, 12, 13"
                }
            }
        } 