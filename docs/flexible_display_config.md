# Configuración Flexible del Display MAX7219

## Descripción

El proyecto ahora soporta una configuración flexible que permite elegir entre dos tipos de displays MAX7219:

1. **Single Module (8x8)**: Un solo módulo MAX7219 para display de 8x8 LEDs
2. **Cascade Module (16x8)**: Múltiples módulos MAX7219 en cascada para display de 16x8 LEDs

## Configuración

### Archivo config.py

Para cambiar entre los dos tipos de display, modifica la configuración en `src/config.py`:

```python
# Configuración para múltiples módulos MAX7219 en cascada
MAX7219_DISPLAY_TYPE = "cascade"  # "single" o "cascade"
MAX7219_NUM_MODULES = 2  # Número de módulos conectados en serie (solo para cascade)
MAX7219_DISPLAY_WIDTH = 16  # Ancho total del display (8 para single, 16 para cascade)
MAX7219_DISPLAY_HEIGHT = 8   # Alto del display
```

### Opciones de Configuración

#### Para Display Single (8x8)
```python
MAX7219_DISPLAY_TYPE = "single"
MAX7219_DISPLAY_WIDTH = 8
```

#### Para Display Cascade (16x8)
```python
MAX7219_DISPLAY_TYPE = "cascade"
MAX7219_NUM_MODULES = 2
MAX7219_DISPLAY_WIDTH = 16
```

## Conexiones por Tipo

### Single Module (8x8)
```
Raspberry Pi Pico 2W
├── GP2 ──→ Módulo MAX7219 DIN
├── GP3 ──→ Módulo MAX7219 CS
├── GP4 ──→ Módulo MAX7219 CLK
└── 3.3V ──→ Módulo MAX7219 VCC
    GND ──→ Módulo MAX7219 GND
```

### Cascade Module (16x8)
```
Raspberry Pi Pico 2W
├── GP2 ──→ Módulo 1 DIN
├── GP3 ──→ Módulo 1 CS ──→ Módulo 2 CS
├── GP4 ──→ Módulo 1 CLK ──→ Módulo 2 CLK
└── 3.3V ──→ Módulo 1 VCC ──→ Módulo 2 VCC
    GND ──→ Módulo 1 GND ──→ Módulo 2 GND

Módulo 1 DOUT ──→ Módulo 2 DIN
```

## Archivos del Sistema

### Controladores Disponibles

1. **`src/max7219_display.py`**: Controlador flexible que selecciona automáticamente
2. **`src/max7219_display_single.py`**: Controlador para un solo módulo (8x8)
3. **`src/max7219_display_cascade.py`**: Controlador para múltiples módulos (16x8)

### Selección Automática

El archivo `src/max7219_display.py` actúa como un selector que importa automáticamente la versión correcta según `MAX7219_DISPLAY_TYPE`:

```python
if MAX7219_DISPLAY_TYPE == "single":
    from max7219_display_single import MAX7219DisplaySingle as MAX7219Display
elif MAX7219_DISPLAY_TYPE == "cascade":
    from max7219_display_cascade import MAX7219Display as MAX7219Display
```

## Ventajas de la Configuración Flexible

### 1. **Compatibilidad**
- Mismo código funciona con ambos tipos de display
- No requiere cambios en el código principal
- Fácil migración entre configuraciones

### 2. **Escalabilidad**
- Fácil agregar más módulos en el futuro
- Configuración centralizada
- Reutilización de código

### 3. **Mantenimiento**
- Código organizado por funcionalidad
- Documentación específica para cada tipo
- Debugging simplificado

## Casos de Uso

### Para Proyectos Simples
```python
MAX7219_DISPLAY_TYPE = "single"
```
- Un solo módulo MAX7219
- Display de 8x8 LEDs
- Conexión simple
- Menor consumo de energía

### Para Proyectos Avanzados
```python
MAX7219_DISPLAY_TYPE = "cascade"
MAX7219_NUM_MODULES = 2
```
- Múltiples módulos MAX7219
- Display de 16x8 LEDs
- Mayor área de visualización
- Mejor legibilidad

## Migración entre Configuraciones

### De Single a Cascade
1. Cambiar `MAX7219_DISPLAY_TYPE` a `"cascade"`
2. Actualizar `MAX7219_DISPLAY_WIDTH` a `16`
3. Configurar `MAX7219_NUM_MODULES`
4. Conectar módulos adicionales según documentación

### De Cascade a Single
1. Cambiar `MAX7219_DISPLAY_TYPE` a `"single"`
2. Actualizar `MAX7219_DISPLAY_WIDTH` a `8`
3. Desconectar módulos adicionales
4. Mantener solo un módulo conectado

## Verificación de Configuración

### Al Iniciar el Sistema
El sistema mostrará un mensaje indicando qué controlador está usando:

```
Usando controlador MAX7219 Single Module (8x8)
```
o
```
Usando controlador MAX7219 Cascade (16x8)
```

### Verificación de Funcionalidad
- **Single**: Los patrones se muestran directamente en 8x8
- **Cascade**: Los patrones se centran automáticamente en 16x8

## Solución de Problemas

### Error de Configuración
```
ValueError: Tipo de display no válido: invalid_type. Use 'single' o 'cascade'
```
**Solución**: Verificar que `MAX7219_DISPLAY_TYPE` sea `"single"` o `"cascade"`

### Problemas de Conexión
- **Single**: Verificar conexión de un solo módulo
- **Cascade**: Verificar conexión en cascada y alimentación compartida

### Problemas de Visualización
- **Single**: Los patrones deben ocupar todo el display 8x8
- **Cascade**: Los patrones se centran automáticamente en 16x8

## Notas Importantes

1. **Compatibilidad**: Ambos controladores mantienen la misma interfaz
2. **Performance**: El controlador cascade puede ser ligeramente más lento
3. **Memoria**: El controlador cascade usa más memoria
4. **Energía**: Más módulos = mayor consumo de energía
5. **Costo**: Más módulos = mayor costo de hardware

## Expansión Futura

Para agregar soporte para más módulos:

1. Crear nuevo controlador (ej: `max7219_display_4modules.py`)
2. Agregar nueva opción en `config.py`
3. Actualizar selector en `max7219_display.py`
4. Documentar nueva configuración 