# Configuración del Sistema de Contador de Vueltas
# Raspberry Pi Pico 2W

# =============================================================================
# CONFIGURACIÓN DE MODO DE OPERACIÓN
# =============================================================================
# Modo de operación del sistema
SERVER_ONLY_MODE = True  # True = Solo servidor API, False = Con interfaz web
ENABLE_WEB_INTERFACE = False  # Habilitar interfaz web (solo si SERVER_ONLY_MODE = False)

# Configuración WiFi
WIFI_SSID = "jrcsistemas"
WIFI_PASSWORD = "jrcs1st3m4s"
WIFI_CONNECT_TIMEOUT = 10  # Timeout para conexión WiFi (segundos)

# Configuración del servidor
SERVER_PORT = 8080

# =============================================================================
# CONFIGURACIÓN DE PINES
# =============================================================================
LED_PIN_RED = 0          # LED rojo en GP0
SENSOR_TCRT5000_PIN = 16 # Sensor TCRT5000 en GP16

# =============================================================================
# CONFIGURACIÓN DEL DISPLAY MAX7219
# =============================================================================
# Pines del display
MAX7219_DIN_PIN = 3      # Datos (MOSI)
MAX7219_CS_PIN = 5       # Chip Select
MAX7219_CLK_PIN = 2      # Reloj (SCK)

# Configuración del display
MAX7219_NUM_MODULES = 2  # Número de módulos en cascada
MAX7219_BRIGHTNESS = 8    # Brillo (0-15)
MAX7219_ROTATION = 90     # Rotación (0, 90, 180, 270)
MAX7219_ORIENTATION = "vertical"  # "horizontal" o "vertical"

# =============================================================================
# CONFIGURACIÓN DE LA CARRERA
# =============================================================================
RACE_MAX_LAPS = 9       # Máximo número de vueltas
RACE_NUM_RACERS = 1      # Número de corredores por defecto
RACE_AUTO_RESET = True    # Reiniciar automáticamente al completar
RACE_SHOW_FLAG_ANIMATION = True  # Mostrar animación de bandera al finalizar
RACE_START_TIMEOUT = 10   # Timeout para inicio de carrera (segundos)

# =============================================================================
# CONFIGURACIÓN DE ANIMACIONES
# =============================================================================
# Animación de bandera a cuadros
FLAG_ANIMATION_DURATION = 15  # Duración en segundos
FLAG_ANIMATION_SPEED = 0.2   # Velocidad de cambio (segundos)
CHECKERED_FLAG_BLINK_INTERVAL = 0.5  # Intervalo de titileo para bandera a cuadros (segundos)

# Tipos de animación disponibles
ANIMATION_TYPES = {
    "checkered_flag": "Bandera a cuadros clásica",
    "spinning_flag": "Bandera giratoria",
    "pulse_flag": "Bandera pulsante",
    "wave_flag": "Bandera ondulante",
    "none": "Sin animación"
}

# Animación por defecto al completar carrera
DEFAULT_COMPLETION_ANIMATION = "checkered_flag"

# =============================================================================
# CONFIGURACIÓN DE SENSORES
# =============================================================================
SENSOR_DEBOUNCE_TIME = 0.1  # Tiempo de debounce en segundos
SENSOR_AUTO_INCREMENT = True  # Incrementar automáticamente con sensor

# =============================================================================
# CONFIGURACIÓN DEL SEMÁFORO
# =============================================================================
# Pines del semáforo
TRAFFIC_LIGHT_RED_PIN = 11    # Luz roja en GPIO11
TRAFFIC_LIGHT_YELLOW_PIN = 12 # Luz amarilla en GPIO12
TRAFFIC_LIGHT_GREEN_PIN = 13  # Luz verde en GPIO13

# Tiempos del semáforo (en segundos)
TRAFFIC_LIGHT_BLINK_INTERVAL = 0.5  # Tiempo de intermitencia para titileo
TRAFFIC_LIGHT_RED_DURATION = 3.0     # Duración de luz roja
TRAFFIC_LIGHT_YELLOW_DURATION = 3.0  # Duración de luz amarilla
TRAFFIC_LIGHT_GREEN_DURATION = 0     # Duración de luz verde (0 = indefinido)

# Configuración PWM para módulo de 5V en 3.3V
TRAFFIC_LIGHT_PWM_FREQ = 1000       # Frecuencia PWM (Hz)
TRAFFIC_LIGHT_DUTY_ON = 1023         # Duty cycle máximo (100%)
TRAFFIC_LIGHT_DUTY_OFF = 0           # Duty cycle mínimo (0%)
TRAFFIC_LIGHT_VOLTAGE_COMPENSATION = True  # Habilitar compensación de voltaje

# Estados del semáforo
TRAFFIC_LIGHT_STATE_OFF = "off"
TRAFFIC_LIGHT_STATE_BLINKING = "blinking"
TRAFFIC_LIGHT_STATE_RED = "red"
TRAFFIC_LIGHT_STATE_YELLOW = "yellow"
TRAFFIC_LIGHT_STATE_GREEN = "green"

# =============================================================================
# CONFIGURACIÓN DEL PILOTO
# =============================================================================
RACER_NAME = "Racer 1"  # Nombre por defecto del piloto
RACER_NAME_MAX_LENGTH = 10  # Longitud máxima del nombre
RACER_DISPLAY_PREFIX = "🏎️ "  # Prefijo para mostrar en display
RACER_NAME_SCROLL_SPEED = 0.15  # Velocidad del scroll del nombre (segundos) - Más rápido para mejor fluidez

# =============================================================================
# CONFIGURACIÓN DE DEBUG
# =============================================================================
DEBUG_ENABLED = False     # Habilitar mensajes de debug
DEBUG_LEVEL = "INFO"      # Nivel de debug: "DEBUG", "INFO", "WARNING", "ERROR"

# =============================================================================
# CONFIGURACIÓN DEL SERVIDOR WEB
# =============================================================================
# Configuración del servidor web
WEB_SERVER_PORT = 80  # Puerto estándar HTTP
WEB_SERVER_HOST = "0.0.0.0"  # Escuchar en todas las interfaces
WEB_SERVER_TIMEOUT = 0.1  # Timeout no bloqueante en segundos
WEB_SERVER_MAX_CONNECTIONS = 5  # Máximo número de conexiones simultáneas

# Configuración de actualización
WEB_UPDATE_INTERVAL = 0.1  # Intervalo de polling del titileo (100ms)
WEB_STATUS_UPDATE_INTERVAL = 2.0  # Intervalo de actualización de estado en la web (2s)
WEB_SERVER_UPDATE_INTERVAL = 0.1  # Intervalo de actualización del servidor web (100ms)

# Configuración de memoria
WEB_GC_INTERVAL = 100  # Ejecutar garbage collector cada 100 iteraciones
WEB_MAX_REQUEST_SIZE = 1024  # Tamaño máximo de solicitud HTTP

# Configuración de CORS
WEB_ENABLE_CORS = True
WEB_CORS_ORIGIN = "*"
WEB_CORS_METHODS = "GET, POST, OPTIONS"
WEB_CORS_HEADERS = "Content-Type"

# Configuración de debug del servidor web
WEB_DEBUG_ENABLED = False
WEB_LOG_REQUESTS = True
WEB_LOG_ERRORS = True

# Configuración de seguridad
WEB_MAX_REQUEST_TIME = 30  # Tiempo máximo de procesamiento de solicitud (segundos)
WEB_RATE_LIMIT_ENABLED = False  # Habilitar limitación de tasa (no implementado aún)

# Configuración de la interfaz web
WEB_TITLE = "🏁 Controlador de Carrera"
WEB_DESCRIPTION = "Control remoto de carrera para pista Scalextric"
WEB_VERSION = "0.0.1"

# Configuración de notificaciones
WEB_ENABLE_NOTIFICATIONS = True
WEB_NOTIFICATION_DURATION = 3000  # Duración de notificaciones en ms

# Configuración de WebSockets (para futuras implementaciones)
WEB_WEBSOCKET_ENABLED = False
WEB_WEBSOCKET_PORT = 8080 