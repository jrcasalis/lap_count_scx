"""
Herramientas MCP para control de carrera
"""

import httpx
import time
from typing import Dict, Any, Optional
from config import SCALEXTRIX_API_BASE_URL, SCALEXTRIX_API_TIMEOUT

class RaceTools:
    """Herramientas para controlar carreras"""
    
    def __init__(self):
        self.base_url = SCALEXTRIX_API_BASE_URL
        self.timeout = SCALEXTRIX_API_TIMEOUT
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def get_race_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual de la carrera"""
        try:
            response = await self.client.get(f"{self.base_url}/api/status")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "message": "Estado de carrera obtenido exitosamente",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al obtener estado de carrera",
                "timestamp": time.time()
            }
    
    async def start_race(self) -> Dict[str, Any]:
        """Inicia una nueva carrera"""
        try:
            response = await self.client.get(f"{self.base_url}/start_race")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "message": "Carrera iniciada exitosamente",
                "action": "start_race",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al iniciar carrera",
                "action": "start_race",
                "timestamp": time.time()
            }
    
    async def stop_race(self) -> Dict[str, Any]:
        """Detiene la carrera actual"""
        try:
            response = await self.client.get(f"{self.base_url}/stop_race")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "message": "Carrera detenida exitosamente",
                "action": "stop_race",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al detener carrera",
                "action": "stop_race",
                "timestamp": time.time()
            }
    
    async def reset_race(self) -> Dict[str, Any]:
        """Resetea los parámetros de la carrera"""
        try:
            response = await self.client.get(f"{self.base_url}/reset")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "message": "Carrera reseteada exitosamente",
                "action": "reset",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al resetear carrera",
                "action": "reset",
                "timestamp": time.time()
            }
    
    async def start_previous(self) -> Dict[str, Any]:
        """Inicia la previa"""
        try:
            response = await self.client.get(f"{self.base_url}/start_previous")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "message": "Previa iniciada exitosamente",
                "action": "start_previous",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al iniciar previa",
                "action": "start_previous",
                "timestamp": time.time()
            }
    
    async def stop_previous(self) -> Dict[str, Any]:
        """Detiene la previa"""
        try:
            response = await self.client.get(f"{self.base_url}/stop_previous")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "message": "Previa detenida exitosamente",
                "action": "stop_previous",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al detener previa",
                "action": "stop_previous",
                "timestamp": time.time()
            }
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose() 