# Controlador LED, Contador de Vueltas y Semáforo - Raspberry Pi Pico 2W

Este proyecto permite controlar un LED, un contador de vueltas con display doble MAX7219 (8x16 LEDs), un semáforo para la largada de carreras y animaciones, todo mediante una interfaz web moderna y una API HTTP REST, ejecutándose en una Raspberry Pi Pico 2W.

## 🚀 Características principales

- Control de LED mediante interfaz web y API
- Contador de vueltas de carrera con animaciones
- Display MAX7219 flexible (8x8 o 16x8 LEDs, doble módulo en cascada)
- **Sistema de semáforo para largada de carreras**
- Animaciones de bandera a cuadros y otras configurables desde la web
- Servidor web integrado en MicroPython
- Interfaz moderna y responsive
- Documentación y ejemplos completos
- Estructura de proyecto escalable

## ✅ Driver y sistema configurables

### Parámetros configurables:
- **`brightness`** (0-15): Control de brillo
- **`rotation`** (0°, 90°, 180°, 270°): Rotación del texto
- **`orientation`** ('horizontal'/'vertical'): Orientación del display

### Funciones de configuración:
- **`set_brightness(brightness)`** - Cambiar brillo en tiempo real
- **`set_rotation(rotation)`** - Cambiar rotación
- **`set_orientation(orientation)`** - Cambiar orientación

### Funciones de visualización:
- **`show_two_digits(value)`** - Muestra números con configuración aplicada
- **`show_text(text)`** - Muestra texto (números)
- **Animaciones de bandera a cuadros, giratoria, pulsante, ondulante y alternante**

## 📁 Estructura de archivos principales

- `src/max7219_dual_display_configurable.py` - Driver principal configurable
- `src/race_controller.py` - Lógica de carrera y animaciones
- `src/web_server.py` - Servidor web y API
- `src/main.py` - Arranque principal
- `src/config.py` - Configuración centralizada
- `patterns/` - Patrones centralizados (dígitos, letras, varios, animaciones)
- `examples/` - Ejemplos de uso y pruebas
- `web/` - Interfaz web (HTML, CSS, JS)

## 🧪 Ejemplos disponibles

- Pruebas de animaciones, integración web, nombre del piloto, scroll, semáforo, etc. (ver carpeta `examples/`)

# 📋 Documentación de la API HTTP REST

La API permite controlar el sistema desde cualquier cliente HTTP (web, scripts, etc). Todas las respuestas son en formato JSON y contienen el campo `success`.

- **Base URL**: `http://<ip-pico>:8080`
- **Protocolo**: HTTP/1.1
- **Codificación**: UTF-8

## Endpoints principales

### Página principal y archivos web
- `GET /` - Interfaz web principal
- `GET /style.css` - Estilos CSS
- `GET /script.js` - JavaScript del frontend
- `GET /sounds/<archivo>` - Archivos de sonido (mp3, wav)
- `GET /test-sound.html` y `/test-sound-fix.html` - Pruebas de sonido

### LED
- `GET /api/led/on` - Enciende el LED
- `GET /api/led/off` - Apaga el LED
- `GET /api/led/toggle` - Alterna el estado del LED
- `GET /api/led/status` - Obtiene el estado actual del LED

### Contador de vueltas y carrera
- `GET /api/lap/increment` - Incrementa el contador de vueltas
- `GET /api/lap/reset` - Reinicia la carrera
- `GET /api/lap/status` - Obtiene el estado actual de la carrera
- `GET /api/race/start` - Inicia la carrera
- `GET /api/race/stop` - Detiene la carrera
- `GET /api/race/status` - Estado detallado de la carrera

### Animaciones
- `GET /api/animation/test` - Prueba la animación de bandera a cuadros (o la animación configurada)
- `GET /api/animation/set` - Cambia la animación de finalización (por ahora, fija a bandera a cuadros)
- `GET /api/animation/list` - Lista las animaciones disponibles

### Nombre del piloto
- `GET /api/racer/name` - Obtiene el nombre actual del piloto
- `GET /api/racer/name/set?name=NuevoNombre` - Cambia el nombre del piloto
- `GET /api/racer/display` - Muestra el nombre del piloto en el display con emoji de casco
- `GET /api/racer/scroll/speed` - Obtiene la velocidad de scroll del nombre del piloto

### Semáforo (Traffic Light)
- `GET /api/traffic-light/previous` - Inicia el titileo de todas las luces del semáforo (previa)
- `GET /api/traffic-light/previous-stop` - Detiene el titileo de todas las luces del semáforo
- `GET /api/traffic-light/start` - Inicia la secuencia de largada (Roja -> Amarilla -> Verde)
- `GET /api/traffic-light/stop` - Apaga las luces del semáforo
- `GET /api/traffic-light/status` - Obtiene el estado actual del semáforo

## Ejemplos de respuesta

**Respuesta típica de estado:**
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

**Respuesta de lista de animaciones:**
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

## 📊 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 400 | Bad Request - Petición malformada |
| 404 | Not Found - Endpoint no encontrado |

## 🔧 Ejemplos de uso

### JavaScript
```javascript
async function apiCall(endpoint) {
    const response = await fetch(endpoint);
    const data = await response.json();
    if (data.success) {
        console.log('Operación exitosa:', data.message);
        return data;
    } else {
        console.error('Error:', data.message);
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

### cURL
```bash
curl -X GET http://192.168.1.100:8080/api/lap/increment
curl -X GET http://192.168.1.100:8080/api/lap/status
curl -X GET http://192.168.1.100:8080/api/animation/list
```

### Python
```python
import requests
base_url = "http://192.168.1.100:8080"
# Incrementar vuelta
requests.get(f"{base_url}/api/lap/increment")
# Obtener estado
status = requests.get(f"{base_url}/api/lap/status").json()
print(status)
```

## 🚦 Limitaciones y advertencias
- Sin autenticación (solo red local)
- Un solo LED y un solo contador de vueltas por instancia
- Sin persistencia de estado
- La API es stateless (no mantiene estado entre peticiones)

## 📝 Notas de implementación
- Todas las respuestas incluyen el campo `success`
- Los errores se manejan con códigos HTTP apropiados
- El sistema está pensado para uso educativo, hobby y prototipado

---

Para más detalles sobre la lógica interna, revisa los archivos en `src/` y los ejemplos en `examples/`.