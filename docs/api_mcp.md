# API MCP (Maestro de Control de Pista) - JSON

## Descripción

API REST para el control de carrera Scalextric desde aplicaciones externas. La Raspberry Pi Pico W funciona como servidor MCP que expone endpoints JSON para controlar el sistema de carrera.

## Información General

- **Base URL**: `http://<ip-pico>:80`
- **Protocolo**: HTTP/1.1
- **Formato de respuesta**: JSON
- **Codificación**: UTF-8
- **Puerto**: 80 (configurable en config.py)

## Endpoints Disponibles

### 1. Estado de la Carrera
**GET** `/api/status`

Obtiene el estado completo del sistema de carrera.

**Respuesta:**
```json
{
  "success": true,
  "race_state": "STOPPED",
  "current_laps": 0,
  "max_laps": 9,
  "remaining_laps": 9,
  "progress_percentage": 0.0,
  "is_completed": false,
  "traffic_light_state": "off",
  "racer_name": "Racer 1",
  "sensor_active": true,
  "timestamp": 1703123456.789
}
```

**Campos:**
- `race_state`: Estado actual ("STOPPED", "PREVIOUS", "STARTED", "FINISHED")
- `current_laps`: Vueltas completadas actualmente
- `max_laps`: Número máximo de vueltas configurado
- `remaining_laps`: Vueltas restantes para completar
- `progress_percentage`: Porcentaje de progreso (0-100)
- `is_completed`: Boolean indicando si la carrera está completada
- `traffic_light_state`: Estado del semáforo ("off", "blinking", "red", "yellow", "green")
- `racer_name`: Nombre del piloto configurado
- `sensor_active`: Si el sensor IR está activo
- `timestamp`: Timestamp Unix de la respuesta

---

### 2. Iniciar Carrera
**GET** `/start_race`

Inicia la carrera con secuencia completa del semáforo.

**Respuesta:**
```json
{
  "success": true,
  "message": "Carrera iniciada",
  "action": "start_race"
}
```

**Secuencia automática:**
1. Luz roja (3 segundos)
2. Luz amarilla (3 segundos)
3. Luz verde (carrera iniciada)
4. Sensor IR activado para detectar vueltas

---

### 3. Detener Carrera
**GET** `/stop_race`

Detiene la carrera y reinicia el sistema.

**Respuesta:**
```json
{
  "success": true,
  "message": "Carrera detenida",
  "action": "stop_race"
}
```

**Acciones:**
- Detiene la secuencia del semáforo
- Desactiva el sensor IR
- Resetea el contador de vueltas
- Vuelve al estado inicial

---

### 4. Iniciar Previa
**GET** `/start_previous`

Inicia la previa (titileo del semáforo).

**Respuesta:**
```json
{
  "success": true,
  "message": "Previa iniciada",
  "action": "start_previous"
}
```

**Funcionalidad:**
- Activa el titileo del semáforo
- Muestra el número máximo de vueltas en el display
- Modo de calentamiento

---

### 5. Detener Previa
**GET** `/stop_previous`

Detiene la previa.

**Respuesta:**
```json
{
  "success": true,
  "message": "Previa detenida",
  "action": "stop_previous"
}
```

**Acciones:**
- Detiene el titileo del semáforo
- Vuelve al estado STOPPED
- Display muestra patrón circular titilando

---

### 6. Reiniciar Sistema
**GET** `/reset`

Reinicia el sistema completo.

**Respuesta:**
```json
{
  "success": true,
  "message": "Parámetros reseteados",
  "action": "reset"
}
```

**Acciones:**
- Resetea todos los controladores
- Vuelve al estado inicial
- Limpia contadores y estados

---

## Códigos de Error

### 404 Not Found
```json
{
  "success": false,
  "error": "404 Not Found",
  "message": "Endpoint no encontrado"
}
```

### 405 Method Not Allowed
```json
{
  "success": false,
  "error": "405 Method Not Allowed",
  "message": "Método HTTP no permitido"
}
```

### Error de Sistema
```json
{
  "success": false,
  "error": "Error específico",
  "message": "Descripción del error"
}
```

---

## Ejemplos de Uso

### JavaScript
```javascript
// Obtener estado de la carrera
async function getRaceStatus() {
    try {
        const response = await fetch('http://192.168.1.100:80/api/status');
        const data = await response.json();
        
        if (data.success) {
            console.log('Estado:', data.race_state);
            console.log('Vueltas:', data.current_laps + '/' + data.max_laps);
            console.log('Progreso:', data.progress_percentage + '%');
        } else {
            console.error('Error:', data.message);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

// Iniciar carrera
async function startRace() {
    try {
        const response = await fetch('http://192.168.1.100:80/start_race');
        const data = await response.json();
        
        if (data.success) {
            console.log('Carrera iniciada:', data.message);
        } else {
            console.error('Error:', data.message);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}
```

### Python
```python
import requests
import json

base_url = "http://192.168.1.100:80"

def get_race_status():
    try:
        response = requests.get(f"{base_url}/api/status")
        data = response.json()
        
        if data['success']:
            print(f"Estado: {data['race_state']}")
            print(f"Vueltas: {data['current_laps']}/{data['max_laps']}")
            print(f"Progreso: {data['progress_percentage']}%")
            return data
        else:
            print(f"Error: {data['message']}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

def start_race():
    try:
        response = requests.get(f"{base_url}/start_race")
        data = response.json()
        
        if data['success']:
            print(f"Carrera iniciada: {data['message']}")
            return True
        else:
            print(f"Error: {data['message']}")
            return False
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False
```

### cURL
```bash
# Obtener estado
curl -X GET http://192.168.1.100:80/api/status

# Iniciar carrera
curl -X GET http://192.168.1.100:80/start_race

# Iniciar previa
curl -X GET http://192.168.1.100:80/start_previous

# Detener carrera
curl -X GET http://192.168.1.100:80/stop_race

# Reiniciar sistema
curl -X GET http://192.168.1.100:80/reset
```

---

## Configuración del Servidor MCP

### Modo de Operación
En `config.py` puedes configurar el modo de operación:

```python
# Modo servidor únicamente (recomendado para MCP)
SERVER_ONLY_MODE = True
ENABLE_WEB_INTERFACE = False

# Modo con interfaz web (para pruebas)
SERVER_ONLY_MODE = False
ENABLE_WEB_INTERFACE = True
```

### Parámetros de Red
```python
WIFI_SSID = "tu_red_wifi"
WIFI_PASSWORD = "tu_contraseña"
WIFI_CONNECT_TIMEOUT = 10
```

### Parámetros de Carrera
```python
RACE_MAX_LAPS = 9
RACE_NUM_RACERS = 1
RACER_NAME = "Racer 1"
```

---

## Estados del Sistema

### Estados de Carrera
- **STOPPED**: Sistema en espera, display con patrón circular
- **PREVIOUS**: Modo previa, semáforo titilando
- **STARTED**: Carrera activa, sensor IR funcionando
- **FINISHED**: Carrera completada, animación de bandera

### Estados del Semáforo
- **off**: Semáforo apagado
- **blinking**: Modo titileo (previa)
- **red**: Luz roja encendida
- **yellow**: Luz amarilla encendida
- **green**: Luz verde encendida

---

## Integración con Aplicaciones Mobile

### Flutter/Dart
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class RaceController {
  static const String baseUrl = 'http://192.168.1.100:80';
  
  static Future<Map<String, dynamic>> getStatus() async {
    final response = await http.get(Uri.parse('$baseUrl/api/status'));
    return json.decode(response.body);
  }
  
  static Future<Map<String, dynamic>> startRace() async {
    final response = await http.get(Uri.parse('$baseUrl/start_race'));
    return json.decode(response.body);
  }
}
```

### React Native
```javascript
import { Alert } from 'react-native';

const API_BASE = 'http://192.168.1.100:80';

export const raceAPI = {
  getStatus: async () => {
    try {
      const response = await fetch(`${API_BASE}/api/status`);
      return await response.json();
    } catch (error) {
      Alert.alert('Error', 'No se pudo conectar al servidor MCP');
      return null;
    }
  },
  
  startRace: async () => {
    try {
      const response = await fetch(`${API_BASE}/start_race`);
      return await response.json();
    } catch (error) {
      Alert.alert('Error', 'No se pudo iniciar la carrera');
      return null;
    }
  }
};
```

---

## Monitoreo en Tiempo Real

Para monitoreo continuo, se recomienda:

1. **Polling cada 2-5 segundos** del endpoint `/api/status`
2. **Actualizar UI** con los datos recibidos
3. **Manejar errores** de conexión graciosamente
4. **Mostrar indicadores** de estado de conexión

### Ejemplo de Monitoreo
```javascript
class RaceMonitor {
  constructor(ip) {
    this.baseUrl = `http://${ip}:80`;
    this.isMonitoring = false;
  }
  
  startMonitoring(callback) {
    this.isMonitoring = true;
    this.monitorLoop(callback);
  }
  
  stopMonitoring() {
    this.isMonitoring = false;
  }
  
  async monitorLoop(callback) {
    while (this.isMonitoring) {
      try {
        const response = await fetch(`${this.baseUrl}/api/status`);
        const data = await response.json();
        callback(data);
      } catch (error) {
        callback({ success: false, error: 'Connection lost' });
      }
      
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
}
```

---

## Solución de Problemas

### El servidor no responde
1. Verificar conexión WiFi
2. Comprobar que el puerto 80 esté libre
3. Revisar logs de debug

### Error de CORS
- La API no incluye headers CORS por defecto
- Para desarrollo web, configurar proxy en el servidor de desarrollo
- Para apps mobile, no es necesario

### Problemas de Conexión
1. Verificar que la app y el servidor estén en la misma red
2. Comprobar la dirección IP del servidor MCP
3. Verificar que no haya firewall bloqueando el puerto 80

---

## Próximas Mejoras

- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Autenticación de API
- [ ] Rate limiting
- [ ] Logs de eventos
- [ ] Configuración remota via API
- [ ] Múltiples carreras simultáneas 