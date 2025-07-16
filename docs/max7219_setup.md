# Configuración del Display MAX7219 - Controlador de Carrera

## Descripción

El display MAX7219 es una matriz de LEDs de 8x8 que se integra con el controlador de carrera para mostrar información en tiempo real:
- **Patrón circular**: Se muestra titilando cuando el sistema está en estado STOPPED
- **Número de vueltas**: Muestra las vueltas actuales durante la carrera
- **Número máximo**: Muestra el total de vueltas en modo previa
- **Animación de bandera**: Se muestra al completar la carrera

## Conexiones Hardware

### Pines del Display MAX7219 (2 módulos en cascada)
- **DIN** (Data In) → GP3
- **CS** (Chip Select) → GP5  
- **CLK** (Clock) → GP2
- **VCC** → 3.3V
- **GND** → GND

### Diagrama de Conexión
```
Raspberry Pi Pico 2W    Display MAX7219 (2 módulos)
┌─────────────────┐     ┌─────────────┐
│                 │     │             │
│ GP2 ──────────→│ CLK │             │
│                 │     │             │
│ GP3 ──────────→│ DIN │             │
│                 │     │             │
│ GP5 ──────────→│ CS  │             │
│                 │     │             │
│ 3.3V ─────────→│ VCC │             │
│                 │     │             │
│ GND ──────────→│ GND │             │
│                 │     │             │
└─────────────────┘     └─────────────┘
```

## Configuración Software

### Archivos Principales
- `src/max7219_dual_display_configurable.py`: Controlador avanzado del display
- `src/race_controller.py`: Integración con el controlador de carrera
- `src/config.py`: Configuración centralizada de pines y parámetros

### Configuración en config.py
```python
# Pines del display
MAX7219_DIN_PIN = 3      # Datos (MOSI)
MAX7219_CS_PIN = 5       # Chip Select
MAX7219_CLK_PIN = 2      # Reloj (SCK)

# Configuración del display
MAX7219_NUM_MODULES = 2  # Número de módulos en cascada
MAX7219_BRIGHTNESS = 8    # Brillo (0-15)
MAX7219_ROTATION = 90     # Rotación (0, 90, 180, 270)
MAX7219_ORIENTATION = "vertical"  # "horizontal" o "vertical"
```

## Funcionalidades

### Clase MAX7219DualDisplayConfigurable
```python
# Inicialización automática desde config.py
display = MAX7219DualDisplayConfigurable()

# Mostrar números
display.show_two_digits(15)  # Muestra "15"
display.show_two_digits(7)   # Muestra "07"

# Mostrar patrones
display.start_pattern_blink(FULL_CIRCLE, interval=0.5)
display.stop_pattern_blink()

# Desplazar texto
display.scroll_text_smooth("ROJO", scroll_speed=0.15)

# Limpiar display
display.clear_display()

# Limpieza de recursos
display.cleanup()
```

### Integración Automática con RaceController
El display se integra automáticamente con el controlador de carrera:

#### Estado STOPPED
- Muestra patrón circular titilando
- Indica que el sistema está listo

#### Estado PREVIOUS
- Muestra el número máximo de vueltas
- Sin titileo, información fija

#### Estado STARTED
- Muestra las vueltas actuales del corredor
- Se actualiza en tiempo real

#### Estado FINISHED
- Muestra animación de bandera a cuadros
- Duración configurable (15 segundos por defecto)

## Patrones Disponibles

### Patrón Circular (FULL_CIRCLE)
```
    ████    
  ██    ██  
██        ██
██        ██
██        ██
██        ██
  ██    ██  
    ████    
```

### Bandera a Cuadros (CHECKERED_FLAG_PATTERNS)
```
██  ██  ██  ██
  ██  ██  ██  
██  ██  ██  ██
  ██  ██  ██  
██  ██  ██  ██
  ██  ██  ██  
██  ██  ██  ██
  ██  ██  ██  
```

### Números (0-99)
- Formato de dos dígitos
- Optimizados para legibilidad
- Soporte para números del 00 al 99

## Configuración Avanzada

### Cambiar Brillo
```python
# En config.py
MAX7219_BRIGHTNESS = 12  # Brillo alto (0-15)
```

### Cambiar Rotación
```python
# En config.py
MAX7219_ROTATION = 180  # Rotación 180 grados
```

### Cambiar Orientación
```python
# En config.py
MAX7219_ORIENTATION = "horizontal"  # Orientación horizontal
```

### Configurar Animaciones
```python
# En config.py
CHECKERED_FLAG_BLINK_INTERVAL = 0.3  # Animación más rápida
FLAG_ANIMATION_DURATION = 10         # Duración más corta
```

## Pruebas

### Verificación Básica
1. El display debe mostrar patrón circular titilando al iniciar
2. Al iniciar previa, debe mostrar el número máximo de vueltas
3. Durante la carrera, debe mostrar las vueltas actuales
4. Al finalizar, debe mostrar la animación de bandera

### Prueba de Números
```python
# Probar números del 0 al 99
for i in range(100):
    display.show_two_digits(i)
    time.sleep(0.5)
```

### Prueba de Patrones
```python
# Probar patrón circular
display.start_pattern_blink(FULL_CIRCLE, interval=0.5)
time.sleep(5)
display.stop_pattern_blink()
```

## Solución de Problemas

### Display no se enciende
- Verificar conexiones de alimentación (VCC y GND)
- Comprobar que los pines están correctamente conectados
- Verificar que el código se ejecuta sin errores
- Comprobar la configuración en `config.py`

### Números no se muestran correctamente
- Verificar la configuración de pines en `config.py`
- Comprobar que el SPI está configurado correctamente
- Verificar que `MAX7219_NUM_MODULES = 2` está configurado
- Revisar la orientación y rotación

### Comunicación SPI falla
- Verificar que los pines DIN, CS y CLK están bien conectados
- Comprobar que no hay conflictos con otros dispositivos SPI
- Verificar la velocidad del SPI (baudrate)
- Asegurarse de que los módulos están en cascada correctamente

### Animaciones no funcionan
- Verificar que los patrones están definidos correctamente
- Comprobar que el polling está funcionando
- Revisar la configuración de intervalos
- Verificar que el display no está bloqueado

### Problemas de memoria
- El display incluye gestión automática de memoria
- Verificar que no hay otros procesos consumiendo memoria
- Reiniciar la Pico si es necesario

## Personalización

### Agregar Nuevos Patrones
Para agregar nuevos patrones, edita el archivo `patterns/various.py`:

```python
NEW_PATTERN = [
    0b11111111,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b11111111
]
```

### Cambiar Intensidad Dinámicamente
```python
display.set_brightness(15)  # Máximo brillo
display.set_brightness(4)   # Brillo bajo
```

### Configurar Animaciones Personalizadas
```python
# Crear animación personalizada
custom_patterns = [pattern1, pattern2, pattern3]
display.start_pattern_blink(custom_patterns, interval=0.2)
```

## Integración con el Sistema

### RaceController
- Control automático del display según el estado
- Actualización en tiempo real de vueltas
- Animaciones de finalización

### Web Server
- El display continúa funcionando durante el servidor web
- Polling no bloqueante mantiene las animaciones
- Integración transparente

### Configuración Centralizada
- Todos los parámetros en `config.py`
- Fácil modificación sin tocar código
- Configuración consistente en todo el sistema

## Referencias

- [Datasheet MAX7219](https://www.analog.com/media/en/technical-documentation/data-sheets/max7219.pdf)
- [Documentación MicroPython SPI](https://docs.micropython.org/en/latest/library/machine.SPI.html)
- [Patrones de LED Matrix](https://github.com/micropython/micropython/tree/master/examples/display) 