# Controlador LED y Contador de Vueltas - Raspberry Pi Pico 2W

Este proyecto permite controlar un LED, un contador de vueltas con display doble MAX7219 (8x16 LEDs) y un semáforo para la largada de carreras en la Raspberry Pi Pico 2W, todo mediante una interfaz web moderna.

## 🚀 Características

- Control de LED mediante interfaz web
- Contador de vueltas de carrera con animaciones
- Display MAX7219 flexible (8x8 o 16x8 LEDs, doble módulo en cascada)
- **Sistema de semáforo para largada de carreras**
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
- `examples/test_traffic_light.py` - Prueba el sistema de semáforo para largada de carreras

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

#### Semáforo
- `GET /api/traffic/previous` - Inicia el titileo de todas las luces del semáforo
- `GET /api/traffic/previous/stop` - Detiene el titileo de todas las luces del semáforo
- `GET /api/traffic/start` - Inicia la secuencia de largada (Roja -> Amarilla -> Verde)
- `GET /api/traffic/stop` - Apaga las luces verdes del semáforo
- `GET /api/traffic/status` - Obtiene el estado actual del semáforo

#### Web
- `/` - Interfaz web principal
- `/style.css` - Estilos CSS
- `/script.js` - JavaScript del frontend