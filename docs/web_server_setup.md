# 🌐 Servidor Web - Controlador de Carrera

## Descripción

El servidor web proporciona una interfaz gráfica moderna y responsiva para controlar el sistema de carrera desde cualquier dispositivo conectado a la misma red WiFi.

## Características

### ✅ Implementadas
- **Interfaz web moderna** con diseño responsivo
- **Control completo** de todas las funciones del sistema
- **Actualización en tiempo real** del estado del sistema
- **API REST** para integración con otras aplicaciones
- **Polling optimizado** que mantiene el titileo funcionando
- **Gestión de memoria** automática
- **Manejo de errores** robusto

### 🚀 Funcionalidades
- 🏁 Iniciar/Detener carrera
- ⚠️ Iniciar/Detener previa (titileo)
- 🔄 Reiniciar sistema
- 💡 Controlar titileo del display
- 🏎️ Configurar nombre del piloto
- 📊 Monitoreo en tiempo real

## Instalación y Uso

### 1. Configuración WiFi
Edita el archivo `config.py` y configura tus credenciales WiFi:

```python
WIFI_SSID = "tu_red_wifi"
WIFI_PASSWORD = "tu_contraseña"
```

### 2. Ejecutar el Servidor
```bash
# En el Raspberry Pi Pico W
python src/main_web.py
```

### 3. Acceder a la Interfaz
Una vez ejecutado, el servidor mostrará la dirección IP:
```
[WEB] 🌐 Servidor web disponible en: http://192.168.1.100:80
```

Abre tu navegador y ve a esa dirección.

## Estructura de Archivos

```
src/
├── main_web.py              # Archivo principal del servidor web
├── web_server.py            # Implementación del servidor web
├── web_config.py            # Configuración específica del servidor
├── race_controller.py       # Controlador de carrera
├── traffic_light_controller.py  # Controlador del semáforo
├── max7219_dual_display_configurable.py  # Controlador del display
└── config.py                # Configuración general
```

## API REST

### Endpoints Disponibles

#### GET `/api/status`
Obtiene el estado actual del sistema.

**Respuesta:**
```json
{
  "success": true,
  "race_state": "STOPPED",
  "current_laps": [0, 0],
  "max_laps": 15,
  "racer_names": ["Piloto 1", "Piloto 2"],
  "traffic_light_state": "off",
  "blink_enabled": true
}
```

#### GET `/api/start_race`
Inicia la carrera.

#### GET `/api/stop_race`
Detiene la carrera.

#### GET `/api/start_previous`
Inicia la previa (titileo del semáforo).

#### GET `/api/stop_previous`
Detiene la previa.

#### GET `/api/reset_race`
Reinicia el sistema.

#### GET `/api/toggle_blink`
Alterna el titileo del display.

#### GET `/api/racer_name`
Obtiene el nombre del piloto.

#### POST `/api/update_racer_name`
Actualiza el nombre del piloto.

## Optimizaciones Implementadas

### 1. Polling No Bloqueante
- El servidor mantiene el polling del titileo funcionando continuamente
- Timeout no bloqueante para aceptar conexiones
- Actualización cada 100ms para titileo fluido

### 2. Gestión de Memoria
- Garbage collector automático cada 100 iteraciones
- Liberación de recursos al cerrar conexiones
- Límite de tamaño de solicitudes HTTP

### 3. Manejo de Errores
- Try-catch en todas las operaciones críticas
- Respuestas HTTP apropiadas para errores
- Logging de errores para debug

### 4. Interfaz Responsiva
- Diseño CSS Grid y Flexbox
- Adaptable a móviles y tablets
- Animaciones suaves y feedback visual

## Configuración Avanzada

### Modificar Puerto
Edita `web_config.py`:
```python
WEB_SERVER_PORT = 8080  # Cambiar puerto
```

### Habilitar Debug
```python
WEB_DEBUG_ENABLED = True
WEB_LOG_REQUESTS = True
```

### Configurar CORS
```python
WEB_CORS_ORIGIN = "http://localhost:3000"  # Origen específico
```

## Solución de Problemas

### El servidor no inicia
1. Verifica la conexión WiFi
2. Asegúrate de que el puerto no esté en uso
3. Revisa los logs de debug

### La interfaz no se carga
1. Verifica la dirección IP mostrada
2. Asegúrate de estar en la misma red WiFi
3. Intenta desde otro navegador

### El titileo no funciona
1. El polling continúa funcionando en el servidor
2. Verifica que el hardware esté conectado correctamente
3. Revisa los logs del controlador

## Próximas Mejoras

- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Autenticación de usuarios
- [ ] Configuración desde la interfaz web
- [ ] Logs de eventos
- [ ] Backup automático de configuración
- [ ] Modo offline con cache
- [ ] Notificaciones push
- [ ] Integración con sensores adicionales

## Contribuir

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Prueba exhaustivamente
5. Envía un pull request

## Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles. 