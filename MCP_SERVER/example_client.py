"""
Cliente de ejemplo para probar el servidor MCP
"""

import asyncio
import httpx
import json
from typing import Dict, Any

class MCPClient:
    """Cliente para interactuar con el servidor MCP"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def get_resources(self) -> Dict[str, Any]:
        """Obtiene lista de recursos disponibles"""
        response = await self.client.get(f"{self.base_url}/resources")
        return response.json()
    
    async def get_race_resource(self) -> Dict[str, Any]:
        """Obtiene información del recurso carrera"""
        response = await self.client.get(f"{self.base_url}/resources/race")
        return response.json()
    
    async def get_system_resource(self) -> Dict[str, Any]:
        """Obtiene información del recurso sistema"""
        response = await self.client.get(f"{self.base_url}/resources/system")
        return response.json()
    
    async def get_race_status(self) -> Dict[str, Any]:
        """Obtiene el estado de la carrera"""
        response = await self.client.get(f"{self.base_url}/tools/get_race_status")
        return response.json()
    
    async def start_race(self) -> Dict[str, Any]:
        """Inicia una carrera"""
        response = await self.client.post(f"{self.base_url}/tools/start_race")
        return response.json()
    
    async def stop_race(self) -> Dict[str, Any]:
        """Detiene una carrera"""
        response = await self.client.post(f"{self.base_url}/tools/stop_race")
        return response.json()
    
    async def get_api_documentation(self) -> Dict[str, Any]:
        """Obtiene documentación de la API"""
        response = await self.client.get(f"{self.base_url}/tools/get_api_documentation")
        return response.json()
    
    async def get_integration_guide(self) -> Dict[str, Any]:
        """Obtiene guía de integración"""
        response = await self.client.get(f"{self.base_url}/tools/get_integration_guide")
        return response.json()
    
    async def close(self):
        """Cierra el cliente"""
        await self.client.aclose()

async def main():
    """Función principal de ejemplo"""
    print("🧪 Cliente de ejemplo para MCP Server")
    print("=" * 50)
    
    client = MCPClient()
    
    try:
        # 1. Obtener recursos disponibles
        print("\n1️⃣ Obteniendo recursos disponibles...")
        resources = await client.get_resources()
        print(f"✅ Recursos encontrados: {len(resources['resources'])}")
        for resource in resources['resources']:
            print(f"   - {resource['name']}: {resource['description']}")
        
        # 2. Obtener información del sistema
        print("\n2️⃣ Obteniendo información del sistema...")
        system_info = await client.get_system_resource()
        print(f"✅ Sistema: {system_info['info']['data']['name']}")
        print(f"   Versión: {system_info['info']['data']['version']}")
        print(f"   Plataforma: {system_info['info']['data']['platform']}")
        
        # 3. Obtener documentación de la API
        print("\n3️⃣ Obteniendo documentación de la API...")
        api_doc = await client.get_api_documentation()
        print(f"✅ API: {api_doc['data']['title']}")
        print(f"   Endpoints disponibles: {len(api_doc['data']['endpoints'])}")
        
        # 4. Obtener estado de la carrera
        print("\n4️⃣ Obteniendo estado de la carrera...")
        race_status = await client.get_race_status()
        if race_status['success']:
            data = race_status['data']
            print(f"✅ Estado: {data.get('race_state', 'N/A')}")
            print(f"   Vueltas: {data.get('current_laps', 0)}/{data.get('max_laps', 0)}")
            print(f"   Progreso: {data.get('progress_percentage', 0)}%")
        else:
            print(f"❌ Error: {race_status.get('error', 'Error desconocido')}")
        
        # 5. Obtener guía de integración
        print("\n5️⃣ Obteniendo guía de integración...")
        integration_guide = await client.get_integration_guide()
        print(f"✅ Guía: {integration_guide['data']['title']}")
        print(f"   Pasos: {len(integration_guide['data']['steps'])}")
        
        print("\n🎉 ¡Prueba completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 