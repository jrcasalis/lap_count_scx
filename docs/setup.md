# Guía de Configuración - Controlador LED

Esta guía te ayudará a configurar el proyecto Controlador LED en tu Raspberry Pi Pico 2W.

## 📋 Requisitos Previos

### Hardware Necesario
- Raspberry Pi Pico 2W
- LED rojo (5mm o 3mm)
- Resistencia de 100Ω (1/4W)
- Cables de conexión (jumper wires)
- Cable USB-C para conectar la Pico

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

### Diagrama de Conexión
```
Raspberry Pi Pico 2W
┌─────────────────┐
│                 │
│  GP0 ──[220Ω]──┼── LED+ ── LED- ── GND
│                 │
└─────────────────┘
```

### Pasos de Conexión
1. **Conectar resistencia**
   - Un extremo de la resistencia de 220Ω al pin GP0
   - El otro extremo al ánodo del LED (pata larga)

2. **Conectar LED**
   - El cátodo del LED (pata corta) al pin GND
   - El ánodo ya está conectado a la resistencia

3. **Verificar conexiones**
   - Asegúrate de que todas las conexiones estén firmes
   - No debe haber cortocircuitos

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
   - `main.py`
   - `led_controller.py`
   - `web_server.py`
   - `race_controller.py`
   - `max7219_display.py`
   - `number_display.py`
   - `lap_counter.py`
   - `config.py`

### 3. Configurar WiFi
Edita el archivo `main.py` y cambia las credenciales WiFi:

```python
WIFI_SSID = "tu-nombre-de-red"
WIFI_PASSWORD = "tu-contraseña"
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
   - Ve a `http://192.168.x.x:8080`
   - Reemplaza con la IP real de tu Pico

3. **Usar la interfaz**
   - Haz clic en los botones para controlar el LED
   - El estado se actualiza en tiempo real

## 🔍 Solución de Problemas

### La Pico no se conecta a WiFi
- Verifica que las credenciales WiFi sean correctas
- Asegúrate de que la red WiFi esté disponible
- Revisa la salida de la consola para errores

### El LED no se enciende
- Verifica las conexiones del hardware
- Asegúrate de que la resistencia esté conectada
- Comprueba que el LED esté en la orientación correcta

### No se puede acceder a la interfaz web
- Verifica que la Pico esté conectada a la misma red WiFi
- Comprueba que el puerto 8080 no esté bloqueado
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