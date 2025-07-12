# Documentación de la API - Controlador LED

Esta documentación describe los endpoints de la API REST para controlar el LED desde la Raspberry Pi Pico 2W.

## 🌐 Información General

- **Base URL**: `http://<ip-pico>:8080`
- **Protocolo**: HTTP/1.1
- **Formato de respuesta**: JSON
- **Codificación**: UTF-8

## 📋 Endpoints Disponibles

### 1. Página Principal
**GET** `/`

Sirve la interfaz web principal para controlar el LED.

**Respuesta:**
- **Content-Type**: `text/html`
- **Descripción**: Página HTML con la interfaz de usuario

**Ejemplo:**
```bash
curl http://192.168.1.100:8080/
```

### 2. Encender LED
**GET** `/api/led/on`

Enciende el LED conectado al pin GP0.

**Respuesta:**
```json
{
    "success": true,
    "is_on": true,
    "message": "LED encendido"
}
```

**Ejemplo:**
```bash
curl http://192.168.1.100:8080/api/led/on
```

### 3. Apagar LED
**GET** `/api/led/off`

Apaga el LED conectado al pin GP0.

**Respuesta:**
```json
{
    "success": true,
    "is_on": false,
    "message": "LED apagado"
}
```

**Ejemplo:**
```bash
curl http://192.168.1.100:8080/api/led/off
```

### 4. Alternar LED
**GET** `/api/led/toggle`

Cambia el estado del LED (si está encendido lo apaga, si está apagado lo enciende).

**Respuesta:**
```json
{
    "success": true,
    "is_on": true,
    "message": "LED alternado"
}
```

**Ejemplo:**
```bash
curl http://192.168.1.100:8080/api/led/toggle
```

### 5. Estado del LED
**GET** `/api/led/status`

Obtiene el estado actual del LED.

**Respuesta:**
```json
{
    "success": true,
    "is_on": false,
    "pin": 0
}
```

**Ejemplo:**
```bash
curl http://192.168.1.100:8080/api/led/status
```

### 6. Estilos CSS
**GET** `/style.css`

Sirve los estilos CSS para la interfaz web.

**Respuesta:**
- **Content-Type**: `text/css`
- **Descripción**: Archivo CSS con estilos modernos

### 7. JavaScript
**GET** `/script.js`

Sirve el código JavaScript del frontend.

**Respuesta:**
- **Content-Type**: `application/javascript`
- **Descripción**: Archivo JavaScript para la funcionalidad del frontend

## 📊 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 400 | Bad Request - Petición malformada |
| 404 | Not Found - Endpoint no encontrado |

## 🔧 Uso con JavaScript

### Función para hacer peticiones
```javascript
async function apiCall(endpoint) {
    try {
        const response = await fetch(endpoint);
        const data = await response.json();
        
        if (data.success) {
            console.log('Operación exitosa:', data.message);
            return data;
        } else {
            console.error('Error:', data.message);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}
```

### Ejemplos de uso
```javascript
// Encender LED
await apiCall('/api/led/on');

// Apagar LED
await apiCall('/api/led/off');

// Alternar LED
await apiCall('/api/led/toggle');

// Obtener estado
const status = await apiCall('/api/led/status');
console.log('LED encendido:', status.is_on);
```

## 🌐 Uso con cURL

### Encender LED
```bash
curl -X GET http://192.168.1.100:8080/api/led/on
```

### Apagar LED
```bash
curl -X GET http://192.168.1.100:8080/api/led/off
```

### Alternar LED
```bash
curl -X GET http://192.168.1.100:8080/api/led/toggle
```

### Obtener estado
```bash
curl -X GET http://192.168.1.100:8080/api/led/status
```

## 🔄 Uso con Python

### Ejemplo con requests
```python
import requests

# Configurar la URL base
base_url = "http://192.168.1.100:8080"

# Encender LED
response = requests.get(f"{base_url}/api/led/on")
print(response.json())

# Apagar LED
response = requests.get(f"{base_url}/api/led/off")
print(response.json())

# Obtener estado
response = requests.get(f"{base_url}/api/led/status")
status = response.json()
print(f"LED encendido: {status['is_on']}")
```

## 🔒 Consideraciones de Seguridad

- La API no implementa autenticación
- Solo funciona en la red local
- No expone información sensible
- Recomendado para uso doméstico/educativo

## 🚀 Limitaciones

- Solo un LED por instancia
- Pin fijo (GP0)
- Sin persistencia de estado
- Memoria limitada de MicroPython

## 📝 Notas de Implementación

- Todas las respuestas incluyen el campo `success`
- Los errores se manejan con códigos HTTP apropiados
- La API es stateless (no mantiene estado entre peticiones)
- Compatible con CORS para desarrollo web

## 🔧 Personalización

Para modificar la API:

1. **Cambiar pin del LED**: Edita `LED_PIN` en `main.py`
2. **Agregar nuevos endpoints**: Modifica `process_request()` en `web_server.py`
3. **Cambiar formato de respuesta**: Modifica `json_response()` en `web_server.py`
4. **Agregar autenticación**: Implementa verificación en `process_request()` 