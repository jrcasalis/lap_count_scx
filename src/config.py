# Configuración del Sistema de Contador de Vueltas
# Raspberry Pi Pico 2W

# Configuración WiFi
WIFI_SSID = "jrcsistemas"
WIFI_PASSWORD = "jrcs1st3m4s"

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
MAX7219_ORIENTATION = "horizontal"  # "horizontal" o "vertical"

# =============================================================================
# CONFIGURACIÓN DE LA CARRERA
# =============================================================================
RACE_MAX_LAPS = 15       # Máximo número de vueltas
RACE_AUTO_RESET = True    # Reiniciar automáticamente al completar
RACE_SHOW_FLAG_ANIMATION = True  # Mostrar animación de bandera al finalizar

# =============================================================================
# CONFIGURACIÓN DE ANIMACIONES
# =============================================================================
# Animación de bandera a cuadros
FLAG_ANIMATION_DURATION = 5  # Duración en segundos
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
# CONFIGURACIÓN DEL SERVIDOR WEB
# =============================================================================
WEB_UPDATE_INTERVAL = 1000  # Intervalo de actualización en ms
WEB_ENABLE_NOTIFICATIONS = True  # Habilitar notificaciones

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
DEBUG_ENABLED = True      # Habilitar mensajes de debug
DEBUG_LEVEL = "INFO"      # Nivel de debug: "DEBUG", "INFO", "WARNING", "ERROR" 