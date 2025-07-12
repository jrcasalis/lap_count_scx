# Controlador LED - Raspberry Pi Pico 2W

Este proyecto permite controlar un LED conectado a la Raspberry Pi Pico 2W mediante una interfaz web moderna.

## 🚀 Características

- Control de LED mediante interfaz web
- Display MAX7219 integrado que muestra "R" cuando el LED está encendido y "N" cuando está apagado
- Servidor web integrado en MicroPython
- Interfaz moderna y responsive
- Documentación completa
- Estructura de proyecto escalable

## 📋 Requisitos

### Hardware
- Raspberry Pi Pico 2W
- LED rojo
- Resistencia de 220Ω
- Display MAX7219 (matriz de 8x8 LEDs)
- Cables de conexión

### Conexiones
- LED positivo → GP0 (con resistencia de 220Ω)
- LED negativo → GND
- Display MAX7219:
  - DIN → GP2
  - CS → GP3
  - CLK → GP4
  - VCC → 3.3V
  - GND → GND

## 📁 Estructura del Proyecto

```
lap_count_scx/
├── README.md                 # Documentación principal
├── requirements.txt          # Dependencias de Python
├── src/
│   ├── main.py              # Código principal de MicroPython
│   ├── web_server.py        # Servidor web
│   ├── led_controller.py    # Controlador del LED
│   ├── max7219_display.py   # Controlador del display MAX7219
│   └── config.py            # Configuración centralizada
├── web/
│   ├── index.html           # Página principal
│   ├── style.css            # Estilos CSS
│   └── script.js            # JavaScript del frontend
├── docs/
│   ├── setup.md             # Guía de configuración
│   └── api.md               # Documentación de la API
└── examples/
    ├── basic_led.py         # Ejemplo básico de control LED
    ├── test_max7219_display.py  # Ejemplo de prueba del display MAX7219
    └── test_max7219_simple.py   # Test simple del display (recomendado)
```

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd lap_count_scx
   ```

2. **Conectar el hardware**
   - Conectar LED positivo a GP0 (con resistencia de 220Ω)
   - Conectar LED negativo a GND
   - Conectar display MAX7219:
     - DIN → GP2
     - CS → GP3
     - CLK → GP4
     - VCC → 3.3V
     - GND → GND

3. **Subir código a la Pico**
   ```bash
   # Usar Thonny IDE o rshell para subir archivos
   # Copiar src/main.py a la Pico
   ```

4. **Ejecutar**
   - Conectar la Pico al ordenador
   - Ejecutar `main.py` en la Pico usando Thonny IDE
   - Acceder a la interfaz web en `http://<ip-pico>:8080`

   **Para probar el display MAX7219:**
   ```python
   # En Thonny IDE, ejecutar:
   exec(open('test_max7219_simple.py').read())
   ```

## 🌐 Uso

1. Conecta la Raspberry Pi Pico 2W a tu red WiFi
2. Ejecuta el código principal
3. Accede a la interfaz web desde cualquier dispositivo en la red
4. Usa los botones para controlar el LED

## 🔧 Configuración WiFi

Edita las credenciales WiFi en `src/main.py`:

```python
WIFI_SSID = "tu-red-wifi"
WIFI_PASSWORD = "tu-contraseña"
```

## 📚 Documentación

- [Guía de Configuración](docs/setup.md)
- [Documentación de la API](docs/api.md)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si tienes problemas o preguntas, abre un issue en el repositorio. 