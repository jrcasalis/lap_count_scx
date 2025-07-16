# 🌐 Servidor Web - Controlador de Carrera Scalextric

## Descripción

El servidor web proporciona una interfaz gráfica moderna y responsiva para controlar el sistema de carrera desde cualquier dispositivo conectado a la misma red WiFi. Permite controlar el semáforo, monitorear vueltas y gestionar el estado de la carrera.

## Características

### ✅ Implementadas
- **Interfaz web moderna** con diseño responsivo
- **Control completo** de todas las funciones del sistema
- **Actualización en tiempo real** del estado del sistema
- **API REST** para integración con otras aplicaciones
- **Polling optimizado** que mantiene el titileo funcionando
- **Gestión de memoria** automática
- **Manejo de errores** robusto
- **Control de semáforo** (inicio, previa, parada)
- **Monitoreo de vueltas** en tiempo real
- **Configuración centralizada** desde config.py

### 🚀 Funcionalidades
- 🏁 Iniciar/Detener carrera
- ⚠️ Iniciar/Detener previa (titileo del semáforo)
- 🔄 Reiniciar sistema
- 💡 Controlar titileo del display
- 🏎️ Configurar nombre del piloto
- 📊 Monitoreo en tiempo real de vueltas
- 🚦 Control del semáforo (rojo, amarillo, verde)

## Instalación y Uso

### 1. Configuración WiFi
Edita el archivo `config.py` y configura tus credenciales WiFi:

```python
WIFI_SSID = "tu_red_wifi"
WIFI_PASSWORD = "tu_contraseña"
WIFI_CONNECT_TIMEOUT = 10  # Timeout para conexión WiFi
```

### 2. Configuración del Servidor
En `config.py` puedes ajustar los parámetros del servidor:

```python
WEB_SERVER_PORT = 80  # Puerto estándar HTTP
WEB_SERVER_TIMEOUT = 0.1  # Timeout no bloqueante
WEB_UPDATE_INTERVAL = 0.1  # Intervalo de polling (100ms)
```

### 3. Ejecutar el Servidor
```bash
# En el Raspberry Pi Pico W
python src/main.py
```

### 4. Acceder a la Interfaz
Una vez ejecutado, el servidor mostrará la dirección IP:
```
[WEB] 🌐 Servidor web disponible en: http://192.168.1.100:80
```

Abre tu navegador y ve a esa dirección.

## Estructura de Archivos

```
src/
├── main.py                           # Archivo principal
├── web_server.py                     # Implementación del servidor web
├── race_controller.py                # Controlador de carrera
├── traffic_light_controller.py       # Controlador del semáforo
├── max7219_dual_display_configurable.py  # Controlador del display
└── config.py                         # Configuración centralizada
```

## API REST

### Endpoints Disponibles

#### GET `/`
Sirve la interfaz web principal.

#### GET `/start_race`
Inicia la carrera con secuencia completa del semáforo.

#### GET `/stop_race`
Detiene la carrera y reinicia el sistema.

#### GET `/start_previous`
Inicia la previa (titileo del semáforo).

#### GET `/stop_previous`
Detiene la previa.

#### GET `/reset`
Reinicia el sistema completo.

### Respuestas de la API
Todas las respuestas son texto plano con mensajes descriptivos:
- `Carrera iniciada`
- `Carrera detenida`
- `Previa iniciada`
- `Previa detenida`
- `Parámetros reseteados`

## Optimizaciones Implementadas

### 1. Polling No Bloqueante
- El servidor mantiene el polling del titileo funcionando continuamente
- Timeout no bloqueante para aceptar conexiones
- Actualización cada 100ms para titileo fluido
- Integración con `race_controller.update()` y `poll_sensor_and_update_laps()`

### 2. Gestión de Memoria
- Garbage collector automático cada 100 iteraciones
- Liberación de recursos al cerrar conexiones
- Límite de tamaño de solicitudes HTTP (1024 bytes)

### 3. Manejo de Errores
- Try-catch en todas las operaciones críticas
- Respuestas HTTP apropiadas para errores
- Logging de errores para debug
- Manejo de timeouts de conexión

### 4. Configuración Centralizada
- Todas las configuraciones en `config.py`
- Parámetros de WiFi, servidor y sistema unificados
- Fácil modificación sin tocar código

## Configuración Avanzada

### Modificar Puerto
Edita `config.py`:
```python
WEB_SERVER_PORT = 8080  # Cambiar puerto
```

### Habilitar Debug
```python
DEBUG_ENABLED = True
WEB_DEBUG_ENABLED = True
WEB_LOG_REQUESTS = True
```

### Configurar Timeouts
```python
WIFI_CONNECT_TIMEOUT = 15  # Timeout WiFi más largo
WEB_SERVER_TIMEOUT = 0.2   # Timeout servidor más largo
```

### Configurar CORS
```python
WEB_ENABLE_CORS = True
WEB_CORS_ORIGIN = "*"
WEB_CORS_METHODS = "GET, POST, OPTIONS"
```

## Interfaz Web

### Características de la Interfaz
- **Diseño responsivo** que funciona en móviles y tablets
- **Botones de control** para todas las funciones
- **Feedback visual** inmediato
- **Compatibilidad** con todos los navegadores modernos

### Funciones Disponibles
1. **Iniciar Carrera**: Comienza la secuencia rojo → amarillo → verde
2. **Iniciar Previa**: Activa el titileo del semáforo
3. **Detener**: Para la carrera actual
4. **Reiniciar**: Resetea todo el sistema

## Solución de Problemas

### El servidor no inicia
1. Verifica la conexión WiFi en `config.py`
2. Asegúrate de que el puerto no esté en uso
3. Revisa los logs de debug habilitando `DEBUG_ENABLED = True`

### La interfaz no se carga
1. Verifica la dirección IP mostrada en la consola
2. Asegúrate de estar en la misma red WiFi
3. Intenta desde otro navegador o dispositivo

### El titileo no funciona
1. El polling continúa funcionando en el servidor
2. Verifica que el hardware esté conectado correctamente
3. Revisa los logs del controlador

### Error de memoria
1. El sistema incluye garbage collector automático
2. Reinicia la Pico si persisten los problemas
3. Verifica que no haya otros procesos consumiendo memoria

### Problemas de conexión WiFi
1. Verifica las credenciales en `config.py`
2. Asegúrate de que la red esté disponible
3. Ajusta `WIFI_CONNECT_TIMEOUT` si es necesario

## Integración con el Sistema

### RaceController
El servidor web se integra completamente con el `RaceController`:
- Controla todos los estados de la carrera
- Monitorea vueltas en tiempo real
- Gestiona el semáforo y display

### TrafficLightController
Control directo del semáforo:
- Secuencia automática de luces
- Modo previa con titileo
- Control PWM para intensidad

### MAX7219Display
Integración con el display:
- Muestra información de carrera
- Animaciones de finalización
- Patrones de estado

## Próximas Mejoras

- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Autenticación de usuarios
- [ ] Configuración desde la interfaz web
- [ ] Logs de eventos
- [ ] Backup automático de configuración
- [ ] Modo offline con cache
- [ ] Notificaciones push
- [ ] Integración con sensores adicionales
- [ ] API JSON para respuestas estructuradas
- [ ] Historial de carreras

## Contribuir

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Prueba exhaustivamente
5. Envía un pull request

## Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles. 