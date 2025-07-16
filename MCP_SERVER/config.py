"""
Configuración del MCP Server para API de Contador de Vueltas Scalextric
"""

import os
from typing import Dict, Any

# Configuración del servidor MCP
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8000"))
MCP_SERVER_DEBUG = os.getenv("MCP_SERVER_DEBUG", "True").lower() == "true"

# Configuración de la API de Scalextric
SCALEXTRIX_API_BASE_URL = os.getenv("SCALEXTRIX_API_BASE_URL", "http://192.168.0.20")
SCALEXTRIX_API_TIMEOUT = int(os.getenv("SCALEXTRIX_API_TIMEOUT", "10"))

# Configuración de recursos MCP
MCP_RESOURCES = {
    "race": {
        "name": "Carrera",
        "description": "Control y estado de la carrera actual",
        "endpoints": {
            "status": "/api/status",
            "start": "/start_race",
            "stop": "/stop_race",
            "reset": "/reset"
        }
    },
    "sensor": {
        "name": "Sensor IR TCRT5000",
        "description": "Sensor infrarrojo para detectar vueltas",
        "pin": 16,
        "type": "TCRT5000"
    },
    "display": {
        "name": "Display MAX7219",
        "description": "Display LED para mostrar información de carrera",
        "modules": 2,
        "brightness": 8,
        "rotation": 90
    },
    "traffic_light": {
        "name": "Semáforo LED",
        "description": "Semáforo para control de salida de carrera",
        "pins": {
            "red": 11,
            "yellow": 12,
            "green": 13
        }
    }
}

# Configuración de herramientas MCP
MCP_TOOLS = {
    "get_race_status": {
        "name": "Obtener Estado de Carrera",
        "description": "Obtiene el estado actual de la carrera",
        "parameters": {},
        "returns": "Dict con información del estado de la carrera"
    },
    "start_race": {
        "name": "Iniciar Carrera",
        "description": "Inicia una nueva carrera",
        "parameters": {},
        "returns": "Dict con resultado de la operación"
    },
    "stop_race": {
        "name": "Detener Carrera",
        "description": "Detiene la carrera actual",
        "parameters": {},
        "returns": "Dict con resultado de la operación"
    },
    "reset_race": {
        "name": "Resetear Carrera",
        "description": "Resetea los parámetros de la carrera",
        "parameters": {},
        "returns": "Dict con resultado de la operación"
    },
    "get_system_info": {
        "name": "Obtener Información del Sistema",
        "description": "Obtiene información completa del sistema",
        "parameters": {},
        "returns": "Dict con información del sistema"
    }
}

# Configuración de documentación
API_DOCUMENTATION = {
    "title": "API de Contador de Vueltas Scalextric",
    "description": "Sistema de control de carrera para pista Scalextric con sensor IR y display LED",
    "version": "1.0.0",
    "contact": {
        "name": "Soporte Técnico",
        "email": "soporte@scalextric-api.com"
    },
    "license": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "mcp_server.log"
} 