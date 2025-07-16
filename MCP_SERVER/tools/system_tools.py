"""
Herramientas MCP para información del sistema
"""

import time
from typing import Dict, Any
from config import API_DOCUMENTATION

class SystemTools:
    """Herramientas para obtener información del sistema"""
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información completa del sistema"""
        return {
            "success": True,
            "data": {
                "name": "Controlador de Carrera Scalextric",
                "version": "1.0.0",
                "description": "Sistema de control de carrera para pista Scalextric",
                "platform": "Raspberry Pi Pico 2W",
                "firmware": "MicroPython",
                "api_version": "1.0.0",
                "uptime": None,
                "memory_usage": None,
                "cpu_usage": None,
                "timestamp": time.time()
            },
            "message": "Información del sistema obtenida exitosamente"
        }
    
    def get_api_documentation(self) -> Dict[str, Any]:
        """Obtiene la documentación completa de la API"""
        return {
            "success": True,
            "data": {
                "title": "API de Contador de Vueltas Scalextric",
                "description": "Sistema de control de carrera para pista Scalextric con sensor IR y display LED",
                "version": "1.0.0",
                "endpoints": {
                    "GET /api/status": {
                        "description": "Obtiene el estado actual de la carrera",
                        "response": {
                            "race_state": "STOPPED|PREVIOUS|STARTED|FINISHED",
                            "current_laps": "int",
                            "max_laps": "int",
                            "remaining_laps": "int",
                            "progress_percentage": "float",
                            "is_completed": "bool",
                            "racer_name": "string",
                            "sensor_active": "bool",
                            "timestamp": "float"
                        }
                    },
                    "GET /start_race": {
                        "description": "Inicia una nueva carrera",
                        "response": {
                            "success": "bool",
                            "message": "string",
                            "action": "start_race"
                        }
                    },
                    "GET /stop_race": {
                        "description": "Detiene la carrera actual",
                        "response": {
                            "success": "bool",
                            "message": "string",
                            "action": "stop_race"
                        }
                    },
                    "GET /reset": {
                        "description": "Resetea los parámetros de la carrera",
                        "response": {
                            "success": "bool",
                            "message": "string",
                            "action": "reset"
                        }
                    },
                    "GET /start_previous": {
                        "description": "Inicia la previa",
                        "response": {
                            "success": "bool",
                            "message": "string",
                            "action": "start_previous"
                        }
                    },
                    "GET /stop_previous": {
                        "description": "Detiene la previa",
                        "response": {
                            "success": "bool",
                            "message": "string",
                            "action": "stop_previous"
                        }
                    }
                },
                "components": {
                    "sensor": {
                        "name": "Sensor IR TCRT5000",
                        "pin": 16,
                        "type": "TCRT5000",
                        "voltage": "3.3V",
                        "detection_range": "2-15mm"
                    },
                    "display": {
                        "name": "Display MAX7219",
                        "pins": {"din": 3, "cs": 5, "clk": 2},
                        "modules": 2,
                        "brightness": 8,
                        "rotation": 90
                    },
                    "traffic_light": {
                        "name": "Semáforo LED",
                        "pins": {"red": 11, "yellow": 12, "green": 13},
                        "voltage": "5V (con compensación a 3.3V)",
                        "pwm_frequency": "1000Hz"
                    }
                },
                "configuration": {
                    "race_max_laps": 9,
                    "race_num_racers": 1,
                    "sensor_debounce_time": 0.1,
                    "traffic_light_blink_interval": 0.5
                }
            },
            "message": "Documentación de la API obtenida exitosamente"
        }
    
    def get_integration_guide(self) -> Dict[str, Any]:
        """Obtiene la guía de integración para otras APIs"""
        return {
            "success": True,
            "data": {
                "title": "Guía de Integración - API Scalextric",
                "description": "Guía para integrar otras APIs con el sistema de carrera",
                "steps": [
                    {
                        "step": 1,
                        "title": "Conectar al servidor MCP",
                        "description": "Establecer conexión con el servidor MCP en localhost:8000",
                        "example": "GET http://localhost:8000/resources"
                    },
                    {
                        "step": 2,
                        "title": "Consultar recursos disponibles",
                        "description": "Obtener lista de recursos y sus esquemas",
                        "example": "GET http://localhost:8000/resources/race"
                    },
                    {
                        "step": 3,
                        "title": "Usar herramientas de control",
                        "description": "Ejecutar acciones usando las herramientas disponibles",
                        "example": "POST http://localhost:8000/tools/start_race"
                    },
                    {
                        "step": 4,
                        "title": "Monitorear estado",
                        "description": "Obtener estado en tiempo real de la carrera",
                        "example": "GET http://localhost:8000/tools/get_race_status"
                    }
                ],
                "best_practices": [
                    "Usar el servidor MCP como intermediario para todas las operaciones",
                    "Consultar recursos antes de ejecutar herramientas",
                    "Manejar errores y timeouts apropiadamente",
                    "Implementar polling para estado en tiempo real"
                ],
                "error_handling": {
                    "connection_error": "Verificar conectividad con la API de Scalextric",
                    "timeout_error": "Aumentar timeout o verificar latencia de red",
                    "api_error": "Verificar estado de la API y parámetros enviados"
                }
            },
            "message": "Guía de integración obtenida exitosamente"
        } 