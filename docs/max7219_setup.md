# Configuración del Display MAX7219

## Descripción

El display MAX7219 es una matriz de LEDs de 8x8 que se integra con el controlador LED para mostrar el estado del LED rojo:
- **"R"**: Cuando el LED rojo está encendido
- **"N"**: Cuando el LED rojo está apagado

## Conexiones Hardware

### Pines del Display MAX7219
- **DIN** (Data In) → GP2
- **CS** (Chip Select) → GP3  
- **CLK** (Clock) → GP4
- **VCC** → 3.3V
- **GND** → GND

### Diagrama de Conexión
```
Raspberry Pi Pico 2W    Display MAX7219
┌─────────────────┐     ┌─────────────┐
│                 │     │             │
│ GP2 ──────────→│ DIN │             │
│                 │     │             │
│ GP3 ──────────→│ CS  │             │
│                 │     │             │
│ GP4 ──────────→│ CLK │             │
│                 │     │             │
│ 3.3V ─────────→│ VCC │             │
│                 │     │             │
│ GND ──────────→│ GND │             │
│                 │     │             │
└─────────────────┘     └─────────────┘
```

## Configuración Software

### Archivos Principales
- `src/max7219_display.py`: Controlador del display
- `src/led_controller.py`: Integración con el controlador LED
- `src/config.py`: Configuración de pines

### Funcionalidades

#### Clase MAX7219Display
```python
# Inicialización
display = MAX7219Display(din_pin=2, cs_pin=3, clk_pin=4)

# Mostrar letra
display.display_letter('R')  # Muestra "R"
display.display_letter('N')  # Muestra "N"

# Limpiar display
display.clear_display()

# Limpieza de recursos
display.cleanup()
```

#### Integración Automática
El display se integra automáticamente con el controlador LED:
- Cuando se enciende el LED: muestra "R"
- Cuando se apaga el LED: muestra "N"

## Patrones de Letras

### Letra "R"
```
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
```

### Letra "N"
```
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
█ █ █ █ █ █ █ █
```

## Pruebas

### Ejemplo de Prueba
Ejecuta `examples/test_max7219_simple.py` para probar el display:

```bash
# En la Raspberry Pi Pico
# Copia el archivo test_max7219_simple.py a la Pico
# Luego ejecuta:
exec(open('test_max7219_simple.py').read())
```

### Verificación
1. El display debe mostrar "R" por 3 segundos
2. Luego mostrar "N" por 3 segundos
3. Finalmente limpiar el display

## Solución de Problemas

### Display no se enciende
- Verificar conexiones de alimentación (VCC y GND)
- Comprobar que los pines están correctamente conectados
- Verificar que el código se ejecuta sin errores

### Letras no se muestran correctamente
- Verificar la configuración de pines en `config.py`
- Comprobar que el SPI está configurado correctamente
- Revisar los patrones de letras en el código

### Comunicación SPI falla
- Verificar que los pines DIN, CS y CLK están bien conectados
- Comprobar que no hay conflictos con otros dispositivos SPI
- Verificar la velocidad del SPI (baudrate)

## Personalización

### Agregar Nuevas Letras
Para agregar nuevas letras, edita el diccionario `patterns` en `max7219_display.py`:

```python
patterns = {
    'R': [...],  # Patrón para R
    'N': [...],  # Patrón para N
    'A': [...],  # Nuevo patrón para A
    # Agregar más letras aquí
}
```

### Cambiar Intensidad
Modifica el valor de intensidad en `init_display()`:
```python
self.write_register(0x0A, 0x08)  # 0x08 = intensidad media
```

## Referencias

- [Datasheet MAX7219](https://www.analog.com/media/en/technical-documentation/data-sheets/max7219.pdf)
- [Documentación MicroPython SPI](https://docs.micropython.org/en/latest/library/machine.SPI.html) 