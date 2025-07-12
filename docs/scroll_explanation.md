# Scroll de Texto en Display MAX7219

## Cómo Funciona el Scroll de "ROJO"

### 1. Proceso de Scroll

El scroll de texto funciona desplazando las letras de izquierda a derecha por el display:

```
Paso 1:    Paso 2:    Paso 3:    Paso 4:
████████   ████████   ████████   ████████
█     █    █     █    █     █    █     █
█     █    █     █    █     █    █     █
████████   ████████   ████████   ████████
█   █      █   █      █   █      █   █
█    █     █    █     █    █     █    █
█     █    █     █    █     █    █     █
█      █   █      █   █      █   █      █
```

### 2. Algoritmo de Scroll

```python
def scroll_text(self, text, delay=0.3):
    # 1. Convertir texto a patrones de letras
    text_patterns = []
    for letter in text.upper():
        if letter in patterns:
            text_patterns.append(patterns[letter])
    
    # 2. Crear matriz completa del texto
    full_text = []
    for letter_pattern in text_patterns:
        full_text.extend(letter_pattern)
    
    # 3. Agregar espacios al final
    full_text.extend([0] * 8)
    
    # 4. Desplazar ventana de 8 filas
    for start_pos in range(len(full_text) - 7):
        display_rows = full_text[start_pos:start_pos + 8]
        
        # 5. Mostrar en display
        for i, row in enumerate(display_rows, 1):
            self.write_register(i, row)
        
        time.sleep(delay)
```

### 3. Patrones de Letras para "ROJO"

#### Letra "R":
```
████████
█     █
█     █
████████
█   █
█    █
█     █
█      █
```

#### Letra "O":
```
  ████
 ██  ██
██    ██
██    ██
██    ██
██    ██
 ██  ██
  ████
```

#### Letra "J":
```
       ██
       ██
       ██
       ██
██    ██
██    ██
 ██  ██
  ████
```

### 4. Secuencia de Scroll para "ROJO"

```
Frames del scroll:
Frame 1:  [R][O][J][O][ ][ ][ ][ ]
Frame 2:  [O][J][O][ ][ ][ ][ ][ ]
Frame 3:  [J][O][ ][ ][ ][ ][ ][ ]
Frame 4:  [O][ ][ ][ ][ ][ ][ ][ ]
Frame 5:  [ ][ ][ ][ ][ ][ ][ ][ ]
```

### 5. Configuración de Velocidad

```python
# Scroll lento (0.5 segundos por frame)
display.scroll_text('ROJO', delay=0.5)

# Scroll medio (0.3 segundos por frame)
display.scroll_text('ROJO', delay=0.3)

# Scroll rápido (0.1 segundos por frame)
display.scroll_text('ROJO', delay=0.1)
```

### 6. Integración con LED Controller

```python
def turn_on(self):
    """Enciende el LED"""
    self.pin.value(1)
    self.is_on = True
    self.display.scroll_text('ROJO')  # Scroll automático
    print("LED encendido")

def turn_off(self):
    """Apaga el LED"""
    self.pin.value(0)
    self.is_on = False
    self.display.display_letter('N')  # Letra estática
    print("LED apagado")
```

### 7. Personalización

#### Agregar Nuevas Letras:
```python
patterns = {
    'R': [...],  # Patrón existente
    'O': [...],  # Patrón existente
    'J': [...],  # Patrón existente
    'A': [       # Nueva letra
        0b00111100,
        0b01100110,
        0b11000011,
        0b11000011,
        0b11111111,
        0b11000011,
        0b11000011,
        0b11000011
    ]
}
```

#### Cambiar Texto:
```python
# Cambiar "ROJO" por otro texto
self.display.scroll_text('HOLA')
self.display.scroll_text('TEST')
self.display.scroll_text('OK')
```

### 8. Ventajas del Scroll

1. **Más información**: Muestra palabras completas en lugar de letras individuales
2. **Mejor legibilidad**: El texto se desplaza de forma clara y ordenada
3. **Efecto visual atractivo**: Crea un efecto dinámico en el display
4. **Flexibilidad**: Permite mostrar cualquier texto soportado

### 9. Consideraciones de Rendimiento

- **Velocidad**: El scroll puede ser lento en MicroPython
- **Memoria**: Cada letra ocupa 8 bytes de memoria
- **Timing**: El delay afecta la fluidez del scroll
- **Compatibilidad**: Funciona con comunicación SPI y manual

### 10. Solución de Problemas

#### Scroll muy lento:
```python
# Reducir delay
display.scroll_text('ROJO', delay=0.1)
```

#### Texto no se muestra:
```python
# Verificar letras soportadas
print("Letras soportadas:", list(patterns.keys()))
```

#### Scroll interrumpido:
```python
# Agregar manejo de excepciones
try:
    display.scroll_text('ROJO')
except Exception as e:
    print(f"Error en scroll: {e}")
```

¡El scroll de texto agrega una dimensión completamente nueva al display MAX7219! 