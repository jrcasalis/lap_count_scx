# 🏁 Controlador de Carrera - Raspberry Pi Pico 2W

Sistema completo de control de carrera para pista Scalextric con interfaz web moderna y control de semáforo.

## 🌟 Características Principales

### ✅ Hardware
- **Display MAX7219** dual configurable con titileo
- **Semáforo LED** con secuencia de largada
- **Sensor TCRT5000** para detección de vueltas
- **Conexión WiFi** integrada

### ✅ Software
- **Servidor web** optimizado para MicroPython
- **Interfaz web** moderna y responsiva
- **API REST** completa
- **Polling optimizado** del titileo
- **Control remoto** desde cualquier dispositivo

### 🚀 Funcionalidades
- 🏁 Iniciar/Detener carrera con secuencia de semáforo
- ⚠️ Previa con titileo del semáforo
- 💡 Control del titileo del display
- 🏎️ Configuración de nombres de pilotos
- 📊 Monitoreo en tiempo real
- 🔄 Reinicio automático del sistema

## 🚀 Instalación y Uso

### 1. Configuración WiFi
Edita `src/config.py` y configura tus credenciales WiFi:
```python
WIFI_SSID = "tu_red_wifi"
WIFI_PASSWORD = "tu_contraseña"
```

### 2. Conexión Hardware
Conecta los componentes según la configuración en `config.py`:
- **Display MAX7219**: Pines 3, 5, 2 (DIN, CS, CLK)
- **Semáforo**: Pines 11, 12, 13 (Rojo, Amarillo, Verde)
- **Sensor**: Pin 16 (TCRT5000)

### 3. Ejecutar Sistema
```bash
# En el Raspberry Pi Pico W
python src/main.py
```

### 4. Acceder a la Interfaz
El sistema mostrará la dirección IP:
```
[WEB] 🌐 Servidor web disponible en: http://192.168.1.100:80
```

Abre tu navegador y ve a esa dirección.

## 📁 Estructura del Proyecto

```
src/
├── main.py                           # 🚀 Archivo principal (servidor web)
├── web_server.py                     # 🌐 Servidor web optimizado
├── config.py                         # ⚙️ Configuración unificada
├── race_controller.py                # 🏁 Controlador de carrera
├── traffic_light_controller.py       # 🚦 Controlador del semáforo
├── max7219_dual_display_configurable.py  # 📺 Display configurable
└── patterns/                         # 🎨 Patrones y animaciones
    ├── animations.py
    ├── digits.py
    ├── letters.py
    └── various.py
```

## 🌐 Interfaz Web

### Características
- **Diseño responsivo** - Funciona en móviles y tablets
- **Actualización en tiempo real** - Estado del sistema
- **Control completo** - Todas las funciones desde el navegador
- **API REST** - Para integración con otras aplicaciones

### Funciones Disponibles
- 🏁 **Iniciar Carrera** - Secuencia completa de semáforo
- 🛑 **Parar Carrera** - Detener y reiniciar
- ⚠️ **Previa** - Titileo del semáforo
- 💡 **Titileo Display** - Control del parpadeo
- 🏎️ **Configurar Piloto** - Cambiar nombres
- 📊 **Estado en Tiempo Real** - Monitoreo continuo

## ⚙️ Configuración

### Servidor Web
```python
WEB_SERVER_PORT = 80              # Puerto HTTP
WEB_UPDATE_INTERVAL = 0.1         # Polling del titileo (100ms)
WEB_DEBUG_ENABLED = False         # Debug del servidor
```

### Carrera
```python
RACE_MAX_LAPS = 15               # Vueltas máximas
RACE_AUTO_RESET = True           # Reinicio automático
```

### Display
```python
MAX7219_BRIGHTNESS = 8           # Brillo (0-15)
MAX7219_ROTATION = 90            # Rotación
```

## 🔧 API REST

### Endpoints Disponibles

#### `GET /api/status`
Obtiene el estado actual del sistema.

#### `GET /api/start_race`
Inicia la carrera con secuencia de semáforo.

#### `GET /api/stop_race`
Detiene la carrera.

#### `GET /api/start_previous`
Inicia la previa (titileo del semáforo).

#### `GET /api/stop_previous`
Detiene la previa.

#### `GET /api/reset_race`
Reinicia el sistema.

#### `GET /api/toggle_blink`
Alterna el titileo del display.

#### `GET /api/racer_name`
Obtiene el nombre del piloto.

#### `POST /api/update_racer_name`
Actualiza el nombre del piloto.

## 🎯 Optimizaciones

### Polling No Bloqueante
- El titileo funciona continuamente
- Timeout no bloqueante para conexiones
- Actualización cada 100ms

### Gestión de Memoria
- Garbage collector automático
- Liberación de recursos
- Límite de solicitudes HTTP

### Manejo de Errores
- Try-catch en operaciones críticas
- Respuestas HTTP apropiadas
- Logging configurable

## 🐛 Solución de Problemas

### El servidor no inicia
1. Verifica la conexión WiFi
2. Asegúrate de que el puerto no esté en uso
3. Revisa los logs de debug

### La interfaz no se carga
1. Verifica la dirección IP mostrada
2. Asegúrate de estar en la misma red WiFi
3. Intenta desde otro navegador

### El titileo no funciona
1. El polling continúa en el servidor
2. Verifica las conexiones del hardware
3. Revisa los logs del controlador

## 🔮 Próximas Mejoras

- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Autenticación de usuarios
- [ ] Configuración desde la interfaz web
- [ ] Logs de eventos
- [ ] Backup automático de configuración
- [ ] Modo offline con cache
- [ ] Notificaciones push
- [ ] Integración con sensores adicionales

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuir

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Prueba exhaustivamente
5. Envía un pull request

---

**🏁 ¡Disfruta de tu pista de Scalextric controlada! 🏁**