# MCP Server - API de Contador de Vueltas Scalextric

Este servidor MCP (Model Context Protocol) proporciona una interfaz estandarizada para interactuar con el sistema de contador de vueltas Scalextric.

## Propósito

El MCP server facilita la integración de otras APIs con el sistema de carrera, proporcionando:

- **Recursos documentados**: Información detallada sobre carreras, sensores, displays
- **Herramientas de control**: Métodos para iniciar, detener y gestionar carreras
- **Documentación automática**: Esquemas y ejemplos para facilitar la integración

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

El servidor se ejecutará en `http://localhost:8000`

## Estructura

- `main.py` - Servidor principal
- `resources/` - Definición de recursos (carreras, sensores, etc.)
- `tools/` - Herramientas de control
- `schemas/` - Esquemas de datos
- `config.py` - Configuración del servidor

## Endpoints MCP

- `GET /resources` - Lista todos los recursos disponibles
- `GET /resources/{resource_id}` - Obtiene información de un recurso específico
- `POST /tools/{tool_name}` - Ejecuta una herramienta de control

## Integración

Para integrar con otra API:

1. Conectarse al servidor MCP
2. Consultar recursos disponibles
3. Usar herramientas para controlar el sistema
4. Obtener documentación automática de la API 