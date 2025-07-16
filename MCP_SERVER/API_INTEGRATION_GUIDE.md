# Guía de Integración - MCP Server para API Scalextric

## ¿Qué es el MCP Server?

El **MCP Server (Model Context Protocol)** es un servidor intermediario que facilita la integración de otras APIs con el sistema de contador de vueltas Scalextric. Proporciona:

- **Recursos documentados**: Información detallada sobre componentes del sistema
- **Herramientas de control**: Métodos estandarizados para interactuar con la API
- **Documentación automática**: Esquemas y ejemplos para facilitar la integración

## Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Otra API      │    │   MCP Server    │    │  API Scalextric │
│                 │◄──►│                 │◄──►│                 │
│ (Tu aplicación) │    │ (Intermediario) │    │ (Raspberry Pi)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Componentes del Sistema Scalextric

### 1. Sensor IR TCRT5000
- **Pin**: GPIO 16
- **Función**: Detectar vueltas del coche
- **Tipo**: Infrarrojo
- **Voltaje**: 3.3V
- **Rango de detección**: 2-15mm

### 2. Display MAX7219
- **Pines**: DIN (3), CS (5), CLK (2)
- **Módulos**: 2 en cascada
- **Brillo**: 0-15
- **Rotación**: 90°
- **Función**: Mostrar información de carrera

### 3. Semáforo LED
- **Pines**: Rojo (11), Amarillo (12), Verde (13)
- **Voltaje**: 5V (con compensación a 3.3V)
- **PWM**: 1000Hz
- **Función**: Control de salida

## Endpoints de la API Scalextric

### Estado de la Carrera
```
GET /api/status
```

**Respuesta:**
```json
{
  "success": true,
  "race_state": "STOPPED|PREVIOUS|STARTED|FINISHED",
  "current_laps": 0,
  "max_laps": 9,
  "remaining_laps": 9,
  "progress_percentage": 0.0,
  "is_completed": false,
  "racer_name": "Racer 1",
  "sensor_active": true,
  "timestamp": 1234567890.123
}
```

### Control de Carrera
```
GET /start_race    # Iniciar carrera
GET /stop_race     # Detener carrera
GET /reset         # Resetear parámetros
GET /start_previous # Iniciar previa
GET /stop_previous  # Detener previa
```

## Integración con MCP Server

### Paso 1: Conectar al MCP Server

```python
import httpx

async def connect_to_mcp():
    client = httpx.AsyncClient()
    response = await client.get("http://localhost:8000/")
    return response.json()
```

### Paso 2: Consultar Recursos

```python
async def get_resources():
    client = httpx.AsyncClient()
    response = await client.get("http://localhost:8000/resources")
    return response.json()

async def get_race_resource():
    client = httpx.AsyncClient()
    response = await client.get("http://localhost:8000/resources/race")
    return response.json()
```

### Paso 3: Usar Herramientas de Control

```python
async def control_race():
    client = httpx.AsyncClient()
    
    # Obtener estado
    status = await client.get("http://localhost:8000/tools/get_race_status")
    
    # Iniciar carrera
    start = await client.post("http://localhost:8000/tools/start_race")
    
    # Detener carrera
    stop = await client.post("http://localhost:8000/tools/stop_race")
    
    return {
        "status": status.json(),
        "start": start.json(),
        "stop": stop.json()
    }
```

### Paso 4: Obtener Documentación

```python
async def get_documentation():
    client = httpx.AsyncClient()
    
    # Documentación de la API
    api_doc = await client.get("http://localhost:8000/tools/get_api_documentation")
    
    # Guía de integración
    guide = await client.get("http://localhost:8000/tools/get_integration_guide")
    
    return {
        "api_documentation": api_doc.json(),
        "integration_guide": guide.json()
    }
```

## Ejemplo Completo de Integración

```python
import asyncio
import httpx
from typing import Dict, Any

class ScalextricIntegration:
    def __init__(self, mcp_server_url: str = "http://localhost:8000"):
        self.mcp_url = mcp_server_url
        self.client = httpx.AsyncClient()
    
    async def initialize(self):
        """Inicializa la integración"""
        # Verificar conexión con MCP Server
        response = await self.client.get(f"{self.mcp_url}/")
        if response.status_code != 200:
            raise Exception("No se puede conectar al MCP Server")
        
        # Obtener recursos disponibles
        resources = await self.client.get(f"{self.mcp_url}/resources")
        print(f"Recursos disponibles: {len(resources.json()['resources'])}")
        
        return True
    
    async def get_race_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual de la carrera"""
        response = await self.client.get(f"{self.mcp_url}/tools/get_race_status")
        return response.json()
    
    async def start_race(self) -> Dict[str, Any]:
        """Inicia una nueva carrera"""
        response = await self.client.post(f"{self.mcp_url}/tools/start_race")
        return response.json()
    
    async def stop_race(self) -> Dict[str, Any]:
        """Detiene la carrera actual"""
        response = await self.client.post(f"{self.mcp_url}/tools/stop_race")
        return response.json()
    
    async def monitor_race(self, callback):
        """Monitorea la carrera en tiempo real"""
        while True:
            status = await self.get_race_status()
            if status['success']:
                callback(status['data'])
            
            await asyncio.sleep(1)  # Polling cada segundo
    
    async def close(self):
        """Cierra la conexión"""
        await self.client.aclose()

# Ejemplo de uso
async def main():
    integration = ScalextricIntegration()
    
    try:
        await integration.initialize()
        
        # Obtener estado inicial
        status = await integration.get_race_status()
        print(f"Estado inicial: {status}")
        
        # Iniciar carrera
        result = await integration.start_race()
        print(f"Carrera iniciada: {result}")
        
        # Monitorear carrera
        def on_status_update(data):
            print(f"Estado: {data['race_state']}, Vueltas: {data['current_laps']}/{data['max_laps']}")
        
        await integration.monitor_race(on_status_update)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await integration.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Mejores Prácticas

### 1. Manejo de Errores
```python
async def safe_api_call(func):
    try:
        return await func()
    except httpx.ConnectError:
        return {"success": False, "error": "No se puede conectar al servidor"}
    except httpx.TimeoutException:
        return {"success": False, "error": "Timeout en la solicitud"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 2. Polling Inteligente
```python
async def smart_polling(interval: float = 1.0, max_retries: int = 3):
    retries = 0
    while retries < max_retries:
        try:
            # Hacer solicitud
            return await make_request()
        except Exception:
            retries += 1
            await asyncio.sleep(interval * retries)  # Backoff exponencial
    raise Exception("Máximo de reintentos alcanzado")
```

### 3. Configuración Flexible
```python
class Config:
    def __init__(self):
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self.timeout = int(os.getenv("MCP_TIMEOUT", "10"))
        self.polling_interval = float(os.getenv("MCP_POLLING_INTERVAL", "1.0"))
```

## Configuración del Entorno

### Variables de Entorno
```bash
# MCP Server
MCP_SERVER_URL=http://localhost:8000
MCP_TIMEOUT=10
MCP_POLLING_INTERVAL=1.0

# API Scalextric
SCALEXTRIX_API_URL=http://192.168.1.100
SCALEXTRIX_TIMEOUT=5
```

### Instalación
```bash
# Clonar repositorio
git clone <repository-url>
cd MCP_SERVER

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env_example.txt .env
# Editar .env con tu configuración

# Ejecutar servidor
python main.py
```

## Troubleshooting

### Problemas Comunes

1. **No se puede conectar al MCP Server**
   - Verificar que el servidor esté ejecutándose
   - Verificar puerto y host en configuración
   - Verificar firewall

2. **Timeout en solicitudes**
   - Aumentar timeout en configuración
   - Verificar latencia de red
   - Verificar estado de la API Scalextric

3. **Errores de API**
   - Verificar estado de la Raspberry Pi
   - Verificar conectividad WiFi
   - Verificar configuración de la API

### Logs y Debug
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# En tus funciones
logger.debug(f"Enviando solicitud a {url}")
logger.info(f"Respuesta recibida: {response.status_code}")
logger.error(f"Error en solicitud: {e}")
```

## Recursos Adicionales

- **Documentación completa**: http://localhost:8000/docs
- **Recursos disponibles**: http://localhost:8000/resources
- **Herramientas**: http://localhost:8000/tools
- **Código fuente**: [Repositorio del proyecto]

---

**Nota**: Esta guía asume que el MCP Server está ejecutándose en `localhost:8000`. Ajusta la URL según tu configuración. 