# Tests Disponibles - Controlador de Carrera

## 🔍 Tests del Sensor IR TCRT5000

### **test_ir_sensor.py** - Test Básico
**Uso**: Test inicial para verificar que el sensor funciona
- Lee el sensor y muestra 0 o 1
- Muy simple y directo
- Ideal para verificar conexiones básicas

### **test_ir_sensor_debug.py** - Test de Debug
**Uso**: Diagnóstico detallado del sensor
- Información completa del sensor
- Instrucciones de diagnóstico
- Resumen de problemas comunes

### **test_ir_sensor_config.py** - Test de Configuración
**Uso**: Probar diferentes configuraciones del pin
- Prueba con pull-up, sin pull, pull-down
- Diagnóstico de problemas de configuración
- Lectura continua para pruebas

### **test_sensor_count.py** - Test de Conteo
**Uso**: Probar conteo de vueltas con debounce
- Cuenta vueltas detectadas
- Implementa debounce para evitar múltiples detecciones
- Ideal para probar lógica de carrera

## 🎨 Tests del Display MAX7219

### **test_animations.py** - Test de Animaciones
**Uso**: Probar todas las animaciones disponibles
- Bandera a cuadros
- Animaciones giratorias
- Efectos visuales

### **test_letters.py** - Test de Letras
**Uso**: Probar visualización de letras
- Todas las letras A-Z
- Verificar legibilidad
- Test de caracteres especiales

### **test_various_patterns.py** - Test de Patrones
**Uso**: Probar patrones varios
- Patrones geométricos
- Efectos visuales
- Verificar display completo

### **test_patterns_centralized.py** - Test de Patrones Centralizados
**Uso**: Probar sistema de patrones centralizado
- Patrones desde archivo central
- Verificar importación
- Test de organización

## 🏎️ Tests del Sistema de Carrera

### **test_racer_name.py** - Test de Nombre del Piloto
**Uso**: Probar visualización de nombres
- Nombres de pilotos
- Scroll de texto
- Verificar legibilidad

### **test_racer_name_fixed.py** - Test de Nombre del Piloto (Corregido)
**Uso**: Versión corregida del test de nombres
- Mejoras en scroll
- Mejor legibilidad
- Correcciones de bugs

### **test_helmet_display.py** - Test de Display con Casco
**Uso**: Probar visualización con emoji de casco
- Emoji de casco 🏎️
- Nombres con prefijo
- Verificar formato

## 🌐 Tests de Integración Web

### **test_web_integration_fixed.py** - Test de Integración Web (Corregido)
**Uso**: Probar integración con interfaz web
- API REST
- Comunicación web
- Verificar endpoints

### **test_web_api.py** - Test de API Web
**Uso**: Probar endpoints específicos de la API
- Endpoints individuales
- Respuestas JSON
- Verificar funcionalidad

## 🎵 Tests de Sonido

### **create_wav_sounds.py** - Creación de Sonidos
**Uso**: Crear archivos de sonido
- Generar sonidos WAV
- Convertir formatos
- Preparar archivos de audio

### **test_server_sounds.py** - Test de Sonidos del Servidor
**Uso**: Probar reproducción de sonidos
- Sonidos del servidor web
- Archivos MP3/WAV
- Verificar reproducción

## 🔧 Tests de Debug

### **debug_controller.py** - Controlador de Debug
**Uso**: Herramientas de debug del sistema
- Debug de componentes
- Verificación de estado
- Diagnóstico de problemas

## 🏁 Test del Sistema Completo

### **test_complete_system.py** - Test del Sistema Completo
**Uso**: Probar todo el sistema integrado
- Sensor + Display + Web
- Funcionalidad completa
- Verificar integración

## 🚀 Cómo Usar los Tests

### **Para el Sensor IR:**
1. **Conexión básica**: `test_ir_sensor.py`
2. **Diagnóstico**: `test_ir_sensor_debug.py`
3. **Configuración**: `test_ir_sensor_config.py`
4. **Conteo**: `test_sensor_count.py`

### **Para el Display:**
1. **Animaciones**: `test_animations.py`
2. **Letras**: `test_letters.py`
3. **Patrones**: `test_various_patterns.py`

### **Para el Sistema:**
1. **Nombres**: `test_racer_name_fixed.py`
2. **Web**: `test_web_integration_fixed.py`
3. **API**: `test_web_api.py`
4. **Completo**: `test_complete_system.py`

### **Para Sonidos:**
1. **Creación**: `create_wav_sounds.py`
2. **Reproducción**: `test_server_sounds.py`

### **Para Debug:**
1. **Debug general**: `debug_controller.py`

## 📋 Orden Recomendado de Tests

1. **Sensor IR**: `test_ir_sensor.py` → `test_ir_sensor_debug.py`
2. **Display**: `test_animations.py` → `test_letters.py`
3. **Web**: `test_web_api.py` → `test_web_integration_fixed.py`
4. **Sonidos**: `create_wav_sounds.py` → `test_server_sounds.py`
5. **Sistema**: `test_racer_name_fixed.py` → `test_complete_system.py`

## 🔧 Solución de Problemas

### **Sensor no detecta:**
- Verificar conexiones (VCC, GND, OUT)
- Usar `test_ir_sensor_config.py`
- Verificar voltaje (3.3V, no 5V)

### **Display no funciona:**
- Verificar conexiones SPI
- Usar `test_animations.py`
- Verificar configuración de pines

### **Web no responde:**
- Verificar WiFi
- Usar `test_web_api.py`
- Verificar puerto 8080

### **Sonidos no funcionan:**
- Verificar archivos de sonido
- Usar `test_server_sounds.py`
- Verificar formato MP3

### **Debug general:**
- Usar `debug_controller.py`
- Verificar logs del sistema
- Revisar configuración 