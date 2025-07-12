# Controlador LED y Contador de Vueltas - Raspberry Pi Pico 2W

Este proyecto permite controlar un LED y un contador de vueltas con display doble MAX7219 (8x16 LEDs) en la Raspberry Pi Pico 2W, todo mediante una interfaz web moderna.

## 🚀 Características

- Control de LED mediante interfaz web
- Contador de vueltas de carrera con animaciones
- Display MAX7219 flexible (8x8 o 16x8 LEDs, doble módulo en cascada)
- Animación de bandera a cuadros alternante (siempre visible)
- Animaciones configurables desde la web
- Servidor web integrado en MicroPython
- Interfaz moderna y responsive
- Documentación completa
- Estructura de proyecto escalable

## ✅ Driver y sistema configurables

### **Nuevas características implementadas:**

#### **🔧 Parámetros configurables:**
- **`brightness`** (0-15): Control de brillo
- **`rotation`** (0°, 90°, 180°, 270°): Rotación del texto
- **`orientation`** ('horizontal'/'vertical'): Orientación del display

#### **🔄 Funciones de configuración:**
- **`set_brightness(brightness)`** - Cambiar brillo en tiempo real
- **`set_rotation(rotation)`** - Cambiar rotación
- **`set_orientation(orientation)`** - Cambiar orientación

#### **📱 Funciones de visualización:**
- **`show_two_digits(value)`** - Muestra números con configuración aplicada
- **`show_text(text)`** - Muestra texto (números)
- **Animaciones de bandera a cuadros, giratoria, pulsante, ondulante y alternante**

### **📁 Archivos principales:**

- `src/max7219_dual_display_configurable.py` - Driver principal configurable
- `src/race_controller.py` - Lógica de carrera y animaciones
- `src/web_server.py` - Servidor web y API
- `src/main.py` - Arranque principal
- `src/config.py` - Configuración centralizada
- `patterns/` - Patrones centralizados (dígitos, letras, varios, animaciones)
- `examples/` - Ejemplos de uso y pruebas
- `web/` - Interfaz web (HTML, CSS, JS)

### **🧪 Ejemplos disponibles:**

- `examples/test_checkered_flag_alternating.py` - Prueba de animación de bandera a cuadros alternante
- `examples/test_checkered_flag_blink.py` - Prueba de bandera a cuadros (alternancia)
- `examples/test_animations.py` - Prueba de todas las animaciones disponibles
- `examples/test_web_integration.py` - Prueba de integración web
- `examples/test_web_integration_fixed.py` - Prueba de integración web con patrones centralizados
- `examples/test_complete_system.py` - Prueba del sistema completo
- `examples/test_racer_name_fixed.py` - Prueba del nombre del piloto con casco
- `examples/test_helmet_display.py` - Prueba del display con casco
- `examples/test_patterns_centralized.py` - Prueba de patrones centralizados
- `examples/test_various_patterns.py` - Prueba de todos los patrones varios
- `examples/test_letters.py` - Prueba de todas las letras A-Z
- `examples/test_racer_name_scroll.py` - Prueba el scroll del nombre del piloto después de guardarlo
- `examples/test_web_racer_name_fixed.py` - Prueba el nombre del piloto desde la interfaz web
- `examples/test_racer_name_web_fixed.py` - Prueba el nombre del piloto desde la web (versión corregida)
- `examples/test_helmet_scroll_fixed.py` - Prueba el scroll con casco real y velocidad configurable
- `examples/test_long_names_scroll.py` - Prueba nombres largos con scroll mejorado

## 📋 API HTTP REST

### Endpoints principales:

#### LED
- `GET /api/led/on` - Enciende el LED
- `GET /api/led/off` - Apaga el LED
- `GET /api/led/toggle` - Alterna el LED
- `GET /api/led/status` - Estado del LED

#### Contador de vueltas
- `GET /api/lap/increment` - Incrementa el contador de vueltas
- `GET /api/lap/reset` - Reinicia la carrera
- `GET /api/lap/status` - Estado actual de la carrera (vueltas, progreso, completado)

#### Animaciones
- `GET /api/animation/test` - Prueba la animación de bandera a cuadros
- `GET /api/animation/set` - Cambia la animación de finalización
- `GET /api/animation/list` - Lista las animaciones disponibles

#### Nombre del piloto
- `GET /api/racer/name` - Obtiene el nombre del piloto
- `GET /api/racer/display` - Muestra el nombre del piloto en el display

#### Web
- `/` - Interfaz web principal
- `/style.css` - Estilos CSS
- `/script.js` - JavaScript del frontend

## 🛠️ Instalación y uso

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd lap_count_scx
   ```
2. **Conectar el hardware** (ver docs y esquemas)
3. **Subir código a la Pico** (ver guía en docs/setup.md)
4. **Ejecutar**
   - Ejecuta `main.py` en la Pico usando Thonny IDE
   - Accede a la interfaz web en `http://<ip-pico>:8080`

## 📚 Documentación

- [Guía de Configuración](docs/setup.md)
- [Documentación de la API](docs/api.md)
- [Configuración de Módulos MAX7219 en Cascada](docs/max7219_cascade_setup.md)
- [Configuración Flexible del Display](docs/flexible_display_config.md)
- [Configuración de Rotación del Display](docs/display_rotation_config.md)
- [Scroll de Texto](docs/scroll_explanation.md)
- [Generación de Letras](docs/letter_generation_explanation.md)

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