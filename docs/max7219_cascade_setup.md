# Configuración de Módulos MAX7219 en Cascada

## Descripción

Este proyecto ahora soporta múltiples módulos MAX7219 conectados en cascada para crear displays más grandes. La configuración actual utiliza **2 módulos** para crear un display de **16x8 LEDs**.

## Conexión Física

### Pines de Conexión

Conecta los módulos MAX7219 de la siguiente manera:

#### Módulo 1 (Primer módulo)
- **DIN** → GP2 (Pin de datos)
- **CS** → GP3 (Chip Select)
- **CLK** → GP4 (Reloj)
- **VCC** → 3.3V
- **GND** → GND

#### Módulo 2 (Segundo módulo)
- **DIN** → DOUT del Módulo 1 (Conexión en cascada)
- **CS** → GP3 (Mismo pin CS que el Módulo 1)
- **CLK** → GP4 (Mismo pin CLK que el Módulo 1)
- **VCC** → 3.3V
- **GND** → GND

### Diagrama de Conexión

```
Raspberry Pi Pico 2W
├── GP2 ──→ Módulo 1 DIN
├── GP3 ──→ Módulo 1 CS ──→ Módulo 2 CS
├── GP4 ──→ Módulo 1 CLK ──→ Módulo 2 CLK
└── 3.3V ──→ Módulo 1 VCC ──→ Módulo 2 VCC
    GND ──→ Módulo 1 GND ──→ Módulo 2 GND

Módulo 1 DOUT ──→ Módulo 2 DIN
```

## Configuración del Software

### Archivo config.py

El archivo `config.py` incluye las siguientes configuraciones para múltiples módulos:

```python
# Configuración para múltiples módulos MAX7219 en cascada
MAX7219_NUM_MODULES = 2  # Número de módulos conectados en serie
MAX7219_DISPLAY_WIDTH = 16  # Ancho total del display (8 * num_modules)
MAX7219_DISPLAY_HEIGHT = 8   # Alto del display
```

### Funcionalidades Soportadas

1. **Display de 16x8 LEDs**: Los dos módulos trabajan como un solo display de 16 columnas por 8 filas.

2. **Centrado Automático**: Todos los patrones (letras, números, banderas) se centran automáticamente en el display de 16 columnas.

3. **Comunicación SPI**: Los módulos se comunican a través del protocolo SPI en cascada, donde el primer módulo recibe los comandos y los pasa al segundo.

## Características Técnicas

### Protocolo de Comunicación

- **Velocidad SPI**: 1 MHz
- **Polaridad**: 0
- **Fase**: 0
- **Modo de cascada**: Los comandos se envían secuencialmente a todos los módulos

### Funciones Actualizadas

1. **write_register_all()**: Envía el mismo comando a todos los módulos
2. **write_register_module()**: Envía un comando específico a un módulo particular
3. **Centrado automático**: Todos los patrones se desplazan 4 bits a la izquierda para centrarlos

### Patrones Centrados

Los patrones de 8x8 se centran automáticamente en el display de 16x8:

```python
# Ejemplo de centrado
original_pattern = 0b00111100  # 8 bits
centered_pattern = original_pattern << 4  # 16 bits centrados
```

## Ventajas del Display de 16x8

1. **Mayor área de visualización**: Doble ancho para mostrar más información
2. **Mejor legibilidad**: Los números y letras se ven más grandes y claros
3. **Animaciones mejoradas**: Más espacio para efectos visuales
4. **Flexibilidad**: Fácil expansión a más módulos si es necesario

## Solución de Problemas

### Problemas Comunes

1. **Display no funciona**: Verificar conexiones SPI y alimentación
2. **Solo funciona un módulo**: Verificar conexión DOUT → DIN entre módulos
3. **Patrones mal centrados**: Verificar configuración de centrado en el código

### Verificación de Conexión

1. Verificar que todos los pines estén correctamente conectados
2. Confirmar que el DOUT del primer módulo esté conectado al DIN del segundo
3. Verificar que ambos módulos reciban alimentación de 3.3V
4. Comprobar que el CS y CLK sean compartidos entre ambos módulos

## Expansión Futura

Para agregar más módulos:

1. Conectar el DOUT del último módulo al DIN del nuevo módulo
2. Actualizar `MAX7219_NUM_MODULES` en `config.py`
3. Actualizar `MAX7219_DISPLAY_WIDTH` según corresponda
4. Ajustar el factor de centrado si es necesario

## Notas Importantes

- Los módulos MAX7219 deben ser del mismo modelo para compatibilidad
- La alimentación debe ser estable a 3.3V
- Las conexiones SPI deben ser cortas para evitar interferencias
- El pin CS debe ser compartido entre todos los módulos en cascada 