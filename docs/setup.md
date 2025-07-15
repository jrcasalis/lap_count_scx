# Guía de Configuración - Controlador de Carrera Scalextric

Esta guía te ayudará a configurar el proyecto Controlador de Carrera para pista Scalextric en tu Raspberry Pi Pico 2W.

## 📋 Requisitos Previos

### Hardware Necesario
- Raspberry Pi Pico 2W
- **Sensor TCRT5000** (sensor infrarrojo para detectar vueltas)
- **Módulo de semáforo LED** (rojo, amarillo, verde)
- **Display MAX7219** (2 módulos en cascada para mostrar información)
- **LED rojo** (5mm o 3mm) - opcional
- **Resistencias** de 220Ω (1/4W) para LEDs
- **Cables de conexión** (jumper wires)
- **Cable USB-C** para conectar la Pico
- **Pista Scalextric** con carro

### Software Necesario
- Thonny IDE (recomendado) o cualquier editor de código
- MicroPython firmware para Raspberry Pi Pico 2W

## 🔧 Instalación del Firmware

1. **Descargar MicroPython**
   - Ve a [micropython.org](https://micropython.org/download/rp2-pico/)
   - Descarga la versión más reciente para Raspberry Pi Pico

2. **Instalar en la Pico**
   - Mantén presionado el botón BOOTSEL mientras conectas la Pico
   - La Pico aparecerá como unidad USB
   - Copia el archivo `.uf2` descargado a la unidad
   - La Pico se reiniciará automáticamente

## 🔌 Conexiones del Hardware

### Diagrama de Conexión Completo
```
Raspberry Pi Pico 2W
┌─────────────────┐
│                 │
│ GP0 ──[220Ω]──┼── LED Rojo (opcional)
│                 │
│ GP2 ──────────→│ CLK (MAX7219)
│ GP3 ──────────→│ DIN (MAX7219)
│ GP5 ──────────→│ CS  (MAX7219)
│                 │
│ GP11 ─────────→│ LED Rojo (Semáforo)
│ GP12 ─────────→│ LED Amarillo (Semáforo)
│ GP13 ─────────→│ LED Verde (Semáforo)
│                 │
│ GP16 ─────────→│ TCRT5000 (Sensor IR)
│                 │
└─────────────────┘
```

### Pasos de Conexión

#### 1. Display MAX7219 (2 módulos en cascada)
- **DIN** (Data In) → GP3
- **CS** (Chip Select) → GP5  
- **CLK** (Clock) → GP2
- **VCC** → 3.3V
- **GND** → GND

#### 2. Módulo de Semáforo
- **LED Rojo** → GP11 (con resistencia de 220Ω)
- **LED Amarillo** → GP12 (con resistencia de 220Ω)
- **LED Verde** → GP13 (con resistencia de 220Ω)
- **GND** → GND

#### 3. Sensor TCRT5000
- **VCC** → 3.3V
- **GND** → GND
- **OUT** → GP16

#### 4. LED Rojo (opcional)
- **Ánodo** → GP0 (con resistencia de 220Ω)
- **Cátodo** → GND

## 💻 Configuración del Software

### 1. Conectar Thonny IDE
1. Abre Thonny IDE
2. Ve a **Herramientas → Opciones → Interpreter**
3. Selecciona **MicroPython (Raspberry Pi Pico)**
4. Selecciona el puerto COM correspondiente
5. Haz clic en **OK**

### 2. Subir Archivos
1. Abre cada archivo de la carpeta `src/` en Thonny
2. Guarda cada archivo en la Pico con el mismo nombre:
   - `main.py` - Archivo principal
   - `config.py` - Configuración centralizada
   - `race_controller.py` - Controlador de carrera
   - `traffic_light_controller.py` - Controlador del semáforo
   - `max7219_dual_display_configurable.py` - Controlador del display
   - `web_server.py` - Servidor web

### 3. Configurar WiFi
Edita el archivo `config.py` y cambia las credenciales WiFi:

```python
WIFI_SSID = "tu-nombre-de-red"
WIFI_PASSWORD = "tu-contraseña"
```

### 4. Configurar Parámetros de Carrera
En `config.py` puedes ajustar:

```python
RACE_MAX_LAPS = 9        # Número de vueltas para completar
RACE_NUM_RACERS = 1      # Número de corredores
RACER_NAME = "Racer 1"   # Nombre del piloto
```

## 🚀 Ejecución

### Método 1: Desde Thonny
1. Abre `main.py` en Thonny
2. Presiona **F5** o haz clic en **Run**
3. Observa la salida en la consola

### Método 2: Ejecución Automática
1. La Pico ejecutará automáticamente `main.py` al reiniciar
2. Desconecta y reconecta la Pico para reiniciar

## 🌐 Acceso a la Interfaz Web

1. **Obtener la IP**
   - Observa la salida en la consola de Thonny
   - Busca la línea: `Dirección IP: 192.168.x.x`

2. **Acceder desde el navegador**
   - Abre tu navegador web
   - Ve a `http://192.168.x.x:80`
   - Reemplaza con la IP real de tu Pico

3. **Usar la interfaz**
   - **Iniciar Carrera**: Comienza la secuencia del semáforo
   - **Iniciar Previa**: Activa el titileo del semáforo
   - **Detener**: Para la carrera actual
   - **Reiniciar**: Resetea el sistema

## 🏁 Funcionalidades del Sistema

### Control de Carrera
- **Secuencia automática**: Rojo → Amarillo → Verde
- **Conteo de vueltas**: Detecta automáticamente con sensor IR
- **Display informativo**: Muestra vueltas actuales y máximo
- **Animación de finalización**: Bandera a cuadros al completar

### Semáforo
- **Luz roja**: Preparación (3 segundos)
- **Luz amarilla**: Atención (3 segundos)
- **Luz verde**: ¡Carrera iniciada!
- **Modo previa**: Titileo para calentamiento

### Display MAX7219
- **Estado STOPPED**: Patrón circular titilando
- **Estado PREVIOUS**: Muestra número máximo de vueltas
- **Estado STARTED**: Muestra vueltas actuales
- **Estado FINISHED**: Animación de bandera a cuadros

## 🔍 Solución de Problemas

### La Pico no se conecta a WiFi
- Verifica que las credenciales WiFi sean correctas
- Asegúrate de que la red WiFi esté disponible
- Revisa la salida de la consola para errores

### El sensor no detecta vueltas
- Verifica las conexiones del sensor TCRT5000
- Asegúrate de que el sensor esté bien posicionado en la pista
- Comprueba que el carro pase por encima del sensor

### El semáforo no funciona
- Verifica las conexiones de los LEDs
- Asegúrate de que las resistencias estén conectadas
- Comprueba que los pines estén correctamente configurados

### El display no muestra información
- Verifica las conexiones del MAX7219
- Comprueba que los pines DIN, CS y CLK estén bien conectados
- Verifica la alimentación (VCC y GND)

### No se puede acceder a la interfaz web
- Verifica que la Pico esté conectada a la misma red WiFi
- Comprueba que el puerto 80 no esté bloqueado
- Intenta acceder desde otro dispositivo en la red

### Error de memoria
- MicroPython tiene memoria limitada
- Cierra otras aplicaciones en la Pico
- Reinicia la Pico si es necesario

## 📱 Acceso desde Dispositivos Móviles

La interfaz web es responsive y funciona en:
- Smartphones Android
- iPhones
- Tablets
- Cualquier dispositivo con navegador web

## 🔄 Actualizaciones

Para actualizar el código:
1. Modifica los archivos en tu ordenador
2. Sube los archivos actualizados a la Pico
3. Reinicia la Pico para aplicar los cambios

## 📞 Soporte

Si tienes problemas:
1. Revisa esta guía de configuración
2. Verifica las conexiones del hardware
3. Comprueba la configuración WiFi
4. Abre un issue en el repositorio del proyecto 