# Documentación de la API - Controlador LED y Contador de Vueltas

Esta documentación describe los endpoints de la API REST para controlar el LED, el contador de vueltas y las animaciones desde la Raspberry Pi Pico 2W.

## 🌐 Información General

- **Base URL**: `http://<ip-pico>:8080`
- **Protocolo**: HTTP/1.1
- **Formato de respuesta**: JSON
- **Codificación**: UTF-8

## 📋 Endpoints Disponibles

### 1. Página Principal
**GET** `/`

Sirve la interfaz web principal para controlar el sistema.

---

### 2. Control de LED

- **GET** `/api/led/on` - Enciende el LED
- **GET** `/api/led/off` - Apaga el LED
- **GET** `/api/led/toggle` - Alterna el estado del LED
- **GET** `/api/led/status` - Obtiene el estado actual del LED

**Ejemplo de respuesta:**
```json
{
    "success": true,
    "is_on": true,
    "message": "LED encendido"
}
```

---

### 3. Contador de Vueltas

- **GET** `/api/lap/increment` - Incrementa el contador de vueltas
- **GET** `/api/lap/reset` - Reinicia la carrera
- **GET** `/api/lap/status` - Obtiene el estado actual de la carrera

**Ejemplo de respuesta para `/api/lap/status`:**
```json
{
    "success": true,
    "race_status": {
        "current_laps": 7,
        "max_laps": 15,
        "remaining_laps": 8,
        "is_completed": false,
        "progress_percentage": 46.7,
        "led_status": { "is_on": false }
    }
}
```

---

### 4. Animaciones

- **GET** `/api/animation/test` - Prueba la animación de bandera a cuadros (o la animación configurada)
- **GET** `/api/animation/set` - Cambia la animación de finalización (por ahora, fija a bandera a cuadros)
- **GET** `/api/animation/list` - Lista las animaciones disponibles

**Ejemplo de respuesta para `/api/animation/list`:**
```json
{
    "success": true,
    "animations": {
        "checkered_flag": "Bandera a cuadros clásica",
        "spinning_flag": "Bandera giratoria",
        "pulse_flag": "Bandera pulsante",
        "wave_flag": "Bandera ondulante",
        "none": "Sin animación"
    }
}
```

---

### 5. Nombre del Piloto

- **GET** `/api/racer/name` - Obtiene el nombre actual del piloto
- **GET** `/api/racer/display` - Muestra el nombre del piloto en el display con emoji de casco

**Ejemplo de respuesta para `/api/racer/name`:**
```json
{
    "success": true,
    "racer_name": "Jose Casalis",
    "message": "Nombre del piloto obtenido"
}
```

**Ejemplo de respuesta para `/api/racer/display`:**
```json
{
    "success": true,
    "message": "Nombre del piloto mostrado en display"
}
```

---

### 6. Archivos Web

- **GET** `/style.css` - Sirve los estilos CSS
- **GET** `/script.js` - Sirve el JavaScript del frontend

---

## 📊 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 400 | Bad Request - Petición malformada |
| 404 | Not Found - Endpoint no encontrado |

---

## 🔧 Uso con JavaScript

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

// Incrementar vuelta
await apiCall('/api/lap/increment');
// Reiniciar carrera
await apiCall('/api/lap/reset');
// Obtener estado de la carrera
const status = await apiCall('/api/lap/status');
console.log('Vueltas:', status.race_status.current_laps);
```

## 🌐 Uso con cURL

```bash
curl -X GET http://192.168.1.100:8080/api/lap/increment
curl -X GET http://192.168.1.100:8080/api/lap/status
curl -X GET http://192.168.1.100:8080/api/animation/list
```

## 🔄 Uso con Python

```python
import requests
base_url = "http://192.168.1.100:8080"
# Incrementar vuelta
requests.get(f"{base_url}/api/lap/increment")
# Obtener estado
status = requests.get(f"{base_url}/api/lap/status").json()
print(status)
```

## 🚀 Limitaciones
- Sin autenticación (solo red local)
- Un solo LED y un solo contador de vueltas por instancia
- Sin persistencia de estado

## 📝 Notas de Implementación
- Todas las respuestas incluyen el campo `success`
- Los errores se manejan con códigos HTTP apropiados
- La API es stateless (no mantiene estado entre peticiones) 