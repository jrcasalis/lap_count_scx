# Documentación de la API - Controlador de Carrera Scalextric

Esta documentación describe los endpoints de la API REST para controlar el sistema de carrera desde la Raspberry Pi Pico 2W.

## 🌐 Información General

- **Base URL**: `http://<ip-pico>:80`
- **Protocolo**: HTTP/1.1
- **Formato de respuesta**: Texto plano
- **Codificación**: UTF-8
- **Puerto**: 80 (configurable en config.py)

## 📋 Endpoints Disponibles

### 1. Página Principal
**GET** `/`

Sirve la interfaz web principal para controlar el sistema de carrera.

**Respuesta**: HTML de la interfaz web

---

### 2. Control de Carrera

#### **GET** `/start_race`
Inicia la carrera con secuencia completa del semáforo.

**Secuencia automática:**
1. Luz roja (3 segundos)
2. Luz amarilla (3 segundos)  
3. Luz verde (carrera iniciada)
4. Sensor IR activado para detectar vueltas

**Respuesta:**
```
Carrera iniciada
```

#### **GET** `/stop_race`
Detiene la carrera y reinicia el sistema.

**Acciones:**
- Detiene la secuencia del semáforo
- Desactiva el sensor IR
- Resetea el contador de vueltas
- Vuelve al estado inicial

**Respuesta:**
```
Carrera detenida
```

#### **GET** `/start_previous`
Inicia la previa (titileo del semáforo).

**Funcionalidad:**
- Activa el titileo del semáforo
- Muestra el número máximo de vueltas en el display
- Modo de calentamiento

**Respuesta:**
```
Previa iniciada
```

#### **GET** `/stop_previous`
Detiene la previa.

**Acciones:**
- Detiene el titileo del semáforo
- Vuelve al estado STOPPED
- Display muestra patrón circular titilando

**Respuesta:**
```
Previa detenida
```

#### **GET** `/reset`
Reinicia el sistema completo.

**Acciones:**
- Resetea todos los controladores
- Vuelve al estado inicial
- Limpia contadores y estados

**Respuesta:**
```
Parámetros reseteados
```

---

## 🏁 Estados del Sistema

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

## 🔧 Configuración

### Parámetros de Carrera (config.py)
```python
RACE_MAX_LAPS = 9        # Número de vueltas para completar
RACE_NUM_RACERS = 1      # Número de corredores
RACER_NAME = "Racer 1"   # Nombre del piloto
RACE_START_TIMEOUT = 10  # Timeout para inicio (segundos)
```

### Parámetros del Servidor (config.py)
```python
WEB_SERVER_PORT = 80     # Puerto del servidor
WEB_SERVER_TIMEOUT = 0.1 # Timeout no bloqueante
WEB_UPDATE_INTERVAL = 0.1 # Intervalo de polling (100ms)
```

### Parámetros de Animación (config.py)
```python
FLAG_ANIMATION_DURATION = 15  # Duración animación bandera (segundos)
CHECKERED_FLAG_BLINK_INTERVAL = 0.5  # Intervalo titileo bandera
```

---

## 🌐 Uso con JavaScript

```javascript
async function controlCarrera(accion) {
    try {
        const response = await fetch(`/${accion}`);
        const mensaje = await response.text();
        console.log('Respuesta:', mensaje);
        return mensaje;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Ejemplos de uso
await controlCarrera('start_race');    // Iniciar carrera
await controlCarrera('start_previous'); // Iniciar previa
await controlCarrera('stop_race');     // Detener carrera
await controlCarrera('reset');         // Reiniciar sistema
```

---

## 🌐 Uso con cURL

```bash
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

## 🔄 Uso con Python

```python
import requests

base_url = "http://192.168.1.100:80"

def control_carrera(accion):
    try:
        response = requests.get(f"{base_url}/{accion}")
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ejemplos
control_carrera('start_race')     # Iniciar carrera
control_carrera('start_previous') # Iniciar previa
control_carrera('stop_race')      # Detener carrera
control_carrera('reset')          # Reiniciar sistema
```

---

## 📊 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 400 | Bad Request - Petición malformada |
| 404 | Not Found - Endpoint no encontrado |
| 405 | Method Not Allowed - Método HTTP no permitido |

---

## 🔍 Monitoreo del Sistema

### Información de Estado
El sistema proporciona información en tiempo real a través de:

1. **Display MAX7219**: Muestra vueltas actuales y estado
2. **Semáforo LED**: Indica estado de la carrera
3. **Consola**: Logs de debug (si están habilitados)

### Estados del Display
- **Patrón circular titilando**: Sistema en STOPPED
- **Número máximo**: Modo PREVIOUS
- **Vueltas actuales**: Carrera STARTED
- **Animación bandera**: Carrera FINISHED

---

## 🚀 Limitaciones Actuales

- **Sin autenticación**: Solo red local
- **Un corredor**: Soporte para un solo carro por defecto
- **Sin persistencia**: Estado se resetea al reiniciar
- **Respuestas simples**: Texto plano, no JSON estructurado

---

## 🔮 Próximas Mejoras

### API JSON
```json
{
  "success": true,
  "race_state": "STARTED",
  "current_laps": 5,
  "max_laps": 9,
  "traffic_light_state": "green",
  "message": "Carrera iniciada"
}
```

### Endpoints Futuros
- `GET /api/status` - Estado completo del sistema
- `GET /api/laps` - Información de vueltas
- `POST /api/config` - Configurar parámetros
- `GET /api/history` - Historial de carreras

---

## 📝 Notas de Implementación

### Polling No Bloqueante
- El servidor mantiene el polling del titileo funcionando
- Timeout no bloqueante para aceptar conexiones
- Actualización cada 100ms para fluidez

### Gestión de Memoria
- Garbage collector automático
- Liberación de recursos al cerrar conexiones
- Límite de tamaño de solicitudes HTTP

### Manejo de Errores
- Try-catch en todas las operaciones críticas
- Respuestas HTTP apropiadas
- Logging de errores para debug

---

## 🔧 Solución de Problemas

### El servidor no responde
1. Verificar conexión WiFi
2. Comprobar que el puerto 80 esté libre
3. Revisar logs de debug

### La carrera no inicia
1. Verificar conexiones del semáforo
2. Comprobar configuración en config.py
3. Revisar logs del controlador

### El sensor no detecta vueltas
1. Verificar conexiones del TCRT5000
2. Comprobar posición del sensor en la pista
3. Ajustar SENSOR_DEBOUNCE_TIME si es necesario

### El display no funciona
1. Verificar conexiones del MAX7219
2. Comprobar configuración de pines
3. Verificar alimentación (VCC y GND) 