"""
Recurso MCP para la carrera
"""

import httpx
import time
from typing import Dict, Any, Optional
from config import SCALEXTRIX_API_BASE_URL, SCALEXTRIX_API_TIMEOUT
from schemas.race import RaceStatus, RaceState, RaceConfig

class RaceResource:
    """Recurso MCP para gestionar carreras"""
    
    def __init__(self):
        self.base_url = SCALEXTRIX_API_BASE_URL
        self.timeout = SCALEXTRIX_API_TIMEOUT
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual de la carrera"""
        try:
            response = await self.client.get(f"{self.base_url}/api/status")
            response.raise_for_status()
            data = response.json()
            
            return {
                "resource_id": "race",
                "name": "Carrera",
                "description": "Control y estado de la carrera actual",
                "data": data,
                "endpoints": {
                    "status": "/api/status",
                    "start": "/start_race", 
                    "stop": "/stop_race",
                    "reset": "/reset",
                    "start_previous": "/start_previous",
                    "stop_previous": "/stop_previous"
                },
                "schema": {
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
            }
        except Exception as e:
            return {
                "resource_id": "race",
                "name": "Carrera",
                "description": "Control y estado de la carrera actual",
                "error": str(e),
                "endpoints": {
                    "status": "/api/status",
                    "start": "/start_race",
                    "stop": "/stop_race", 
                    "reset": "/reset"
                }
            }
    
    async def get_config(self) -> Dict[str, Any]:
        """Obtiene la configuración de la carrera"""
        return {
            "resource_id": "race_config",
            "name": "Configuración de Carrera",
            "description": "Configuración actual de la carrera",
            "data": {
                "max_laps": 9,
                "num_racers": 1,
                "racer_names": ["Racer 1"],
                "auto_reset": True,
                "show_flag_animation": True
            },
            "schema": {
                "max_laps": "int - Número máximo de vueltas",
                "num_racers": "int - Número de corredores",
                "racer_names": "List[str] - Nombres de los corredores",
                "auto_reset": "bool - Reset automático al completar",
                "show_flag_animation": "bool - Mostrar animación de bandera"
            }
        }
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose() 