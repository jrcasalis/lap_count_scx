#!/usr/bin/env python3
"""
MCP Server compatible con Cursor para API Scalextric
Implementa el protocolo MCP estándar
"""

import json
import sys
import asyncio
import httpx
from typing import Dict, Any, List
import os

class ScalextricMCPServer:
    def __init__(self):
        self.scalextric_api_url = os.getenv("SCALEXTRIX_API_BASE_URL", "http://192.168.1.100")
        self.client = httpx.AsyncClient()
        self.tools = {
            "get_race_status": {
                "name": "get_race_status",
                "description": "Obtiene el estado actual de la carrera Scalextric",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "start_race": {
                "name": "start_race", 
                "description": "Inicia una nueva carrera en la pista Scalextric",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "stop_race": {
                "name": "stop_race",
                "description": "Detiene la carrera actual en la pista Scalextric", 
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "reset_race": {
                "name": "reset_race",
                "description": "Resetea los parámetros de la carrera Scalextric",
                "inputSchema": {
                    "type": "object", 
                    "properties": {},
                    "required": []
                }
            },
            "get_system_info": {
                "name": "get_system_info",
                "description": "Obtiene información del sistema Scalextric",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la inicialización del servidor MCP"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "scalextric-api",
                "version": "1.0.0"
            }
        }

    async def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Lista las herramientas disponibles"""
        return {
            "tools": list(self.tools.values())
        }

    async def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una herramienta específica"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if name == "get_race_status":
            return await self._get_race_status()
        elif name == "start_race":
            return await self._start_race()
        elif name == "stop_race":
            return await self._stop_race()
        elif name == "reset_race":
            return await self._reset_race()
        elif name == "get_system_info":
            return await self._get_system_info()
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Herramienta '{name}' no encontrada"
                    }
                ]
            }

    async def _get_race_status(self) -> Dict[str, Any]:
        """Obtiene el estado de la carrera"""
        try:
            response = await self.client.get(f"{self.scalextric_api_url}/api/status")
            data = response.json()
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Estado de la carrera: {data.get('race_state', 'N/A')}\n"
                               f"Vueltas: {data.get('current_laps', 0)}/{data.get('max_laps', 0)}\n"
                               f"Progreso: {data.get('progress_percentage', 0)}%\n"
                               f"Completada: {data.get('is_completed', False)}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"Error obteniendo estado de carrera: {str(e)}"
                    }
                ]
            }

    async def _start_race(self) -> Dict[str, Any]:
        """Inicia una carrera"""
        try:
            response = await self.client.get(f"{self.scalextric_api_url}/start_race")
            data = response.json()
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Carrera iniciada: {data.get('message', 'OK')}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error iniciando carrera: {str(e)}"
                    }
                ]
            }

    async def _stop_race(self) -> Dict[str, Any]:
        """Detiene una carrera"""
        try:
            response = await self.client.get(f"{self.scalextric_api_url}/stop_race")
            data = response.json()
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Carrera detenida: {data.get('message', 'OK')}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error deteniendo carrera: {str(e)}"
                    }
                ]
            }

    async def _reset_race(self) -> Dict[str, Any]:
        """Resetea una carrera"""
        try:
            response = await self.client.get(f"{self.scalextric_api_url}/reset")
            data = response.json()
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Carrera reseteada: {data.get('message', 'OK')}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error reseteando carrera: {str(e)}"
                    }
                ]
            }

    async def _get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": "Sistema de Contador de Vueltas Scalextric\n"
                           "Plataforma: Raspberry Pi Pico 2W\n"
                           "Firmware: MicroPython\n"
                           "Componentes:\n"
                           "- Sensor IR TCRT5000 (Pin 16)\n"
                           "- Display MAX7219 (Pines 3, 5, 2)\n"
                           "- Semáforo LED (Pines 11, 12, 13)\n"
                           "API URL: " + self.scalextric_api_url
                }
            ]
        }

    async def run(self):
        """Ejecuta el servidor MCP"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                message = json.loads(line.strip())
                method = message.get("method")
                params = message.get("params", {})
                id = message.get("id")
                
                response = {"jsonrpc": "2.0", "id": id}
                
                if method == "initialize":
                    result = await self.handle_initialize(params)
                    response["result"] = result
                elif method == "tools/list":
                    result = await self.handle_tools_list(params)
                    response["result"] = result
                elif method == "tools/call":
                    result = await self.handle_tools_call(params)
                    response["result"] = result
                else:
                    response["error"] = {"code": -32601, "message": "Method not found"}
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": id if 'id' in locals() else None,
                    "error": {"code": -32603, "message": str(e)}
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

async def main():
    server = ScalextricMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main()) 