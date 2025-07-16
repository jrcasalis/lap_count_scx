"""
Servidor MCP para API de Contador de Vueltas Scalextric
"""

import asyncio
import json
import time
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Importar recursos y herramientas
from resources import (
    RaceResource, SensorResource, DisplayResource, 
    TrafficLightResource, SystemResource
)
from tools import RaceTools, SystemTools
from config import (
    MCP_SERVER_HOST, MCP_SERVER_PORT, MCP_SERVER_DEBUG,
    MCP_RESOURCES, MCP_TOOLS, API_DOCUMENTATION
)

# Crear aplicación FastAPI
app = FastAPI(
    title="MCP Server - API Scalextric",
    description="Servidor MCP para facilitar la integración con la API de Contador de Vueltas Scalextric",
    version="1.0.0",
    debug=MCP_SERVER_DEBUG
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar recursos y herramientas
race_resource = RaceResource()
sensor_resource = SensorResource()
display_resource = DisplayResource()
traffic_light_resource = TrafficLightResource()
system_resource = SystemResource()

race_tools = RaceTools()
system_tools = SystemTools()

@app.get("/")
async def root():
    """Endpoint raíz con información del servidor MCP"""
    return {
        "message": "MCP Server - API de Contador de Vueltas Scalextric",
        "version": "1.0.0",
        "description": "Servidor MCP para facilitar la integración con la API de Scalextric",
        "endpoints": {
            "resources": "/resources",
            "tools": "/tools",
            "documentation": "/docs"
        }
    }

@app.get("/resources")
async def list_resources():
    """Lista todos los recursos disponibles"""
    return {
        "resources": [
            {
                "id": "race",
                "name": "Carrera",
                "description": "Control y estado de la carrera actual",
                "endpoint": "/resources/race"
            },
            {
                "id": "sensor",
                "name": "Sensor IR TCRT5000", 
                "description": "Sensor infrarrojo para detectar vueltas",
                "endpoint": "/resources/sensor"
            },
            {
                "id": "display",
                "name": "Display MAX7219",
                "description": "Display LED para mostrar información de carrera",
                "endpoint": "/resources/display"
            },
            {
                "id": "traffic_light",
                "name": "Semáforo LED",
                "description": "Semáforo para control de salida de carrera",
                "endpoint": "/resources/traffic_light"
            },
            {
                "id": "system",
                "name": "Sistema",
                "description": "Información del sistema",
                "endpoint": "/resources/system"
            }
        ]
    }

@app.get("/resources/race")
async def get_race_resource():
    """Obtiene información del recurso carrera"""
    try:
        status = await race_resource.get_status()
        config = await race_resource.get_config()
        return {
            "resource": status,
            "config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recurso carrera: {str(e)}")

@app.get("/resources/sensor")
async def get_sensor_resource():
    """Obtiene información del recurso sensor"""
    try:
        status = sensor_resource.get_status()
        config = sensor_resource.get_config()
        return {
            "resource": status,
            "config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recurso sensor: {str(e)}")

@app.get("/resources/display")
async def get_display_resource():
    """Obtiene información del recurso display"""
    try:
        status = display_resource.get_status()
        config = display_resource.get_config()
        return {
            "resource": status,
            "config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recurso display: {str(e)}")

@app.get("/resources/traffic_light")
async def get_traffic_light_resource():
    """Obtiene información del recurso semáforo"""
    try:
        status = traffic_light_resource.get_status()
        config = traffic_light_resource.get_config()
        return {
            "resource": status,
            "config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recurso semáforo: {str(e)}")

@app.get("/resources/system")
async def get_system_resource():
    """Obtiene información del recurso sistema"""
    try:
        info = system_resource.get_info()
        status = system_resource.get_status()
        documentation = system_resource.get_api_documentation()
        return {
            "info": info,
            "status": status,
            "documentation": documentation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recurso sistema: {str(e)}")

@app.get("/tools")
async def list_tools():
    """Lista todas las herramientas disponibles"""
    return {
        "tools": [
            {
                "name": "get_race_status",
                "description": "Obtiene el estado actual de la carrera",
                "endpoint": "/tools/get_race_status"
            },
            {
                "name": "start_race",
                "description": "Inicia una nueva carrera",
                "endpoint": "/tools/start_race"
            },
            {
                "name": "stop_race",
                "description": "Detiene la carrera actual",
                "endpoint": "/tools/stop_race"
            },
            {
                "name": "reset_race",
                "description": "Resetea los parámetros de la carrera",
                "endpoint": "/tools/reset_race"
            },
            {
                "name": "get_system_info",
                "description": "Obtiene información completa del sistema",
                "endpoint": "/tools/get_system_info"
            }
        ]
    }

@app.get("/tools/get_race_status")
async def tool_get_race_status():
    """Herramienta: Obtiene el estado de la carrera"""
    try:
        result = await race_tools.get_race_status()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado de carrera: {str(e)}")

@app.post("/tools/start_race")
async def tool_start_race():
    """Herramienta: Inicia una carrera"""
    try:
        result = await race_tools.start_race()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error iniciando carrera: {str(e)}")

@app.post("/tools/stop_race")
async def tool_stop_race():
    """Herramienta: Detiene una carrera"""
    try:
        result = await race_tools.stop_race()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deteniendo carrera: {str(e)}")

@app.post("/tools/reset_race")
async def tool_reset_race():
    """Herramienta: Resetea una carrera"""
    try:
        result = await race_tools.reset_race()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reseteando carrera: {str(e)}")

@app.get("/tools/get_system_info")
async def tool_get_system_info():
    """Herramienta: Obtiene información del sistema"""
    try:
        result = system_tools.get_system_info()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo información del sistema: {str(e)}")

@app.get("/tools/get_api_documentation")
async def tool_get_api_documentation():
    """Herramienta: Obtiene documentación de la API"""
    try:
        result = system_tools.get_api_documentation()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo documentación: {str(e)}")

@app.get("/tools/get_integration_guide")
async def tool_get_integration_guide():
    """Herramienta: Obtiene guía de integración"""
    try:
        result = system_tools.get_integration_guide()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo guía de integración: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre del servidor"""
    await race_resource.close()
    await race_tools.close()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando MCP Server para API Scalextric...")
    print(f"📍 Servidor: http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔧 Recursos: http://localhost:8000/resources")
    print("🛠️  Herramientas: http://localhost:8000/tools")
    
    uvicorn.run(
        "main:app",
        host=MCP_SERVER_HOST,
        port=MCP_SERVER_PORT,
        reload=MCP_SERVER_DEBUG
    ) 