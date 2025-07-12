# Configuración de Rotación del Display MAX7219

## Descripción

El sistema ahora soporta rotación configurable de los patrones de display para adaptarse a diferentes orientaciones físicas de los módulos MAX7219. Esto es especialmente útil cuando los displays están montados en vertical o en diferentes ángulos.

## Configuración

### Archivo config.py

Para configurar la rotación del display, modifica las siguientes variables en `src/config.py`:

```python
# Configuración de rotación del display
MAX7219_DISPLAY_ROTATION = 0  # 0, 90, 180, 270 grados
MAX7219_DISPLAY_ORIENTATION = "horizontal"  # "horizontal" o "vertical"
```

## Opciones de Configuración

### Rotación (MAX7219_DISPLAY_ROTATION)

- **0 grados**: Sin rotación (orientación normal)
- **90 grados**: Rotación en sentido horario
- **180 grados**: Rotación completa (patrón invertido)
- **270 grados**: Rotación en sentido antihorario

### Orientación (MAX7219_DISPLAY_ORIENTATION)

- **"horizontal"**: Displays montados horizontalmente
- **"vertical"**: Displays montados verticalmente

## Casos de Uso Comunes

### 1. Displays Horizontales (Normal)
```python
MAX7219_DISPLAY_ROTATION = 0
MAX7219_DISPLAY_ORIENTATION = "horizontal"
```
- Módulos montados horizontalmente
- Cables de entrada en la parte superior
- Orientación estándar

### 2. Displays Verticales (Uno al Lado del Otro)
```python
MAX7219_DISPLAY_ROTATION = 90
MAX7219_DISPLAY_ORIENTATION = "vertical"
```
- Módulos montados verticalmente
- Cables de entrada en la parte superior de cada módulo
- Módulos uno al lado del otro

### 3. Displays Verticales Invertidos
```python
MAX7219_DISPLAY_ROTATION = 270
MAX7219_DISPLAY_ORIENTATION = "vertical"
```
- Módulos montados verticalmente
- Cables de entrada en la parte inferior
- Rotación adicional para corrección

### 4. Displays Horizontales Invertidos
```python
MAX7219_DISPLAY_ROTATION = 180
MAX7219_DISPLAY_ORIENTATION = "horizontal"
```
- Módulos montados horizontalmente pero invertidos
- Cables de entrada en la parte inferior

## Ejemplos de Configuración

### Para Displays Verticales (Tu Caso)
```python
# Configuración para displays verticales, uno al lado del otro
MAX7219_DISPLAY_TYPE = "cascade"
MAX7219_NUM_MODULES = 2
MAX7219_DISPLAY_WIDTH = 16
MAX7219_DISPLAY_ROTATION = 90
MAX7219_DISPLAY_ORIENTATION = "vertical"
```

### Para Displays Horizontales Estándar
```python
# Configuración para displays horizontales estándar
MAX7219_DISPLAY_TYPE = "single"
MAX7219_DISPLAY_WIDTH = 8
MAX7219_DISPLAY_ROTATION = 0
MAX7219_DISPLAY_ORIENTATION = "horizontal"
```

## Algoritmos de Rotación

### Rotación de 90 Grados
```
Original:     Rotado 90°:
██████        █
█    █        ██
█    █   →    ██
█    █        ██
██████        █
```

### Rotación de 180 Grados
```
Original:     Rotado 180°:
██████        ██████
█    █   →    █    █
█    █        █    █
██████        ██████
```

### Rotación de 270 Grados
```
Original:     Rotado 270°:
██████        █
█    █        ██
█    █   →    ██
█    █        ██
██████        █
```

## Implementación Técnica

### Clase DisplayUtils

El sistema utiliza la clase `DisplayUtils` para manejar las transformaciones:

```python
from display_utils import DisplayUtils

# Rotar un patrón
rotated_pattern = DisplayUtils.rotate_pattern(pattern, 90)

# Transformar según orientación y rotación
transformed_pattern = DisplayUtils.transform_pattern_for_orientation(
    pattern, "vertical", 90
)
```

### Métodos Disponibles

1. **`rotate_pattern(pattern, rotation)`**: Rota un patrón según el ángulo
2. **`transform_pattern_for_orientation(pattern, orientation, rotation)`**: Aplica transformación completa
3. **`debug_pattern(pattern, label)`**: Imprime patrón en formato visual para debugging

## Verificación de Configuración

### Al Iniciar el Sistema
El sistema mostrará información sobre la configuración:

```
Usando controlador MAX7219 Cascade (16x8)
Rotación configurada: 90 grados
Orientación: vertical
```

### Testing de Rotación
Para verificar que la rotación funciona correctamente:

1. **Patrón de Test**: Usar un patrón asimétrico como "L" o "7"
2. **Verificación Visual**: Confirmar que el patrón aparece correctamente orientado
3. **Debug**: Usar `DisplayUtils.debug_pattern()` para ver el patrón en consola

## Solución de Problemas

### Problemas Comunes

1. **Texto Aparece Invertido**
   - Cambiar `MAX7219_DISPLAY_ROTATION` a 180
   - O cambiar `MAX7219_DISPLAY_ORIENTATION`

2. **Texto Aparece de Lado**
   - Cambiar `MAX7219_DISPLAY_ROTATION` a 90 o 270
   - Ajustar `MAX7219_DISPLAY_ORIENTATION`

3. **Patrones Mal Alineados**
   - Verificar configuración de `MAX7219_DISPLAY_WIDTH`
   - Confirmar número correcto de módulos

### Debugging

```python
# Para debugging de patrones
from display_utils import DisplayUtils

pattern = [0b11111111, 0b10000001, 0b10000001, 0b11111111,
           0b10001000, 0b10000100, 0b10000010, 0b10000001]

DisplayUtils.debug_pattern(pattern, "Original")
rotated = DisplayUtils.rotate_pattern(pattern, 90)
DisplayUtils.debug_pattern(rotated, "Rotado 90°")
```

## Configuraciones Recomendadas

### Para Diferentes Montajes

1. **Montaje Horizontal Estándar**
   ```python
   MAX7219_DISPLAY_ROTATION = 0
   MAX7219_DISPLAY_ORIENTATION = "horizontal"
   ```

2. **Montaje Vertical (Cables Arriba)**
   ```python
   MAX7219_DISPLAY_ROTATION = 90
   MAX7219_DISPLAY_ORIENTATION = "vertical"
   ```

3. **Montaje Vertical (Cables Abajo)**
   ```python
   MAX7219_DISPLAY_ROTATION = 270
   MAX7219_DISPLAY_ORIENTATION = "vertical"
   ```

4. **Montaje Horizontal Invertido**
   ```python
   MAX7219_DISPLAY_ROTATION = 180
   MAX7219_DISPLAY_ORIENTATION = "horizontal"
   ```

## Notas Importantes

1. **Performance**: Las rotaciones se calculan en tiempo real
2. **Memoria**: Cada transformación crea una copia del patrón
3. **Compatibilidad**: Funciona con ambos tipos de display (single y cascade)
4. **Flexibilidad**: Fácil ajuste sin cambiar código
5. **Debugging**: Herramientas incluidas para verificar configuraciones

## Expansión Futura

Para agregar más opciones de transformación:

1. Agregar nuevos métodos en `DisplayUtils`
2. Actualizar `transform_pattern_for_orientation()`
3. Documentar nuevas opciones
4. Agregar casos de prueba 