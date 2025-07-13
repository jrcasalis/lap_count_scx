# Configuración del Sensor IR TCRT5000

## 📋 Descripción

El sensor TCRT5000 es un sensor infrarrojo reflectivo que detecta objetos cuando el haz IR se refleja de vuelta al sensor. Es ideal para detectar el paso de coches en una pista de Scalextric.

## 🔌 Conexiones

### Diagrama de Conexión
```
TCRT5000 Sensor
┌─────────────┐
│    VCC ─────┼── 3.3V
│    GND ─────┼── GND  
│    OUT ─────┼── GP16
└─────────────┘
```

### Pines del Sensor
- **VCC**: Alimentación 3.3V
- **GND**: Tierra (GND)
- **OUT**: Señal digital (conectado a GP16)

### Pines de la Raspberry Pi Pico 2W
- **GP16**: Entrada digital para la señal del sensor
- **3.3V**: Alimentación
- **GND**: Tierra

## ⚙️ Configuración

### En `src/config.py`
```python
# Sensor TCRT5000
SENSOR_TCRT5000_PIN = 16  # Pin GP16
```

### Características del Sensor
- **Voltaje de operación**: 3.3V
- **Corriente de operación**: 20mA
- **Distancia de detección**: 2-15mm
- **Tiempo de respuesta**: <1ms
- **Lógica**: LOW cuando detecta objeto, HIGH cuando no detecta

## 🔧 Funcionamiento

### Principio de Operación
1. El sensor emite luz infrarroja
2. Cuando un objeto está cerca, la luz se refleja
3. El sensor detecta la luz reflejada
4. La salida cambia de HIGH a LOW

### Lógica de Detección
```python
# TCRT5000: LOW (0) cuando detecta objeto (reflejo)
# HIGH (1) cuando no detecta objeto
detected = sensor.value() == 0
```

### Detección de Flanco
Para contar vueltas, detectamos el flanco descendente (HIGH → LOW):
```python
if last_state == 1 and current_state == 0:
    # Nueva detección de vuelta
    increment_lap()
```

## 🧪 Pruebas

### Test Básico
```python
from machine import Pin
import time

# Configurar sensor
sensor = Pin(16, Pin.IN, Pin.PULL_UP)

# Leer estado
while True:
    detected = sensor.value() == 0
    print("Detectado" if detected else "Libre")
    time.sleep(0.1)
```

### Test Completo
Ejecuta el archivo `test_tcrt5000_sensor.py` para una prueba completa:
```bash
# En la Raspberry Pi Pico
python test_tcrt5000_sensor.py
```

## 📏 Ajuste de Distancia

### Posicionamiento Óptimo
1. **Distancia**: 5-10mm entre el sensor y la pista
2. **Altura**: Centrado sobre la pista
3. **Ángulo**: Perpendicular a la superficie

### Ajuste de Sensibilidad
- **Muy cerca**: Puede detectar falsos positivos
- **Muy lejos**: Puede no detectar objetos
- **Distancia óptima**: 5-10mm

## 🔍 Solución de Problemas

### El sensor no detecta objetos
1. **Verificar conexiones**
   - VCC conectado a 3.3V
   - GND conectado a GND
   - OUT conectado a GP16

2. **Verificar distancia**
   - Ajustar a 5-10mm de la pista
   - Asegurar que esté centrado

3. **Verificar superficie**
   - La superficie debe reflejar luz IR
   - Coches de Scalextric suelen funcionar bien

### Detecciones falsas
1. **Ajustar distancia**
   - Aumentar distancia si hay falsos positivos
   - Reducir distancia si no detecta

2. **Verificar interferencias**
   - Evitar luz solar directa
   - Verificar que no haya otros sensores IR cerca

3. **Ajustar debounce**
   - Aumentar tiempo de debounce si hay múltiples detecciones

### El sensor siempre detecta
1. **Verificar conexión GND**
   - Asegurar que GND esté bien conectado

2. **Verificar pull-up**
   - El pin debe tener pull-up interno
   - Verificar en el código: `Pin(16, Pin.IN, Pin.PULL_UP)`

## 🎯 Optimización

### Para Scalextric
1. **Posicionamiento**: Centrado sobre la pista
2. **Distancia**: 8-10mm de la superficie
3. **Velocidad**: Funciona bien con coches a alta velocidad
4. **Material**: Los coches de plástico reflejan bien la luz IR

### Ajustes de Software
```python
# Tiempo de debounce (ms)
debounce_time = 100

# Detección de flanco
if last_state == 1 and current_state == 0:
    # Verificar debounce
    if time_since_last > debounce_time:
        # Registrar vuelta
        increment_lap()
```

## 📊 Monitoreo

### Estado del Sensor
```python
# Leer estado actual
detected = sensor.value() == 0
status = "🔴 Detectado" if detected else "⚪ Libre"
print(f"Estado: {status}")
```

### Estadísticas
- **Vueltas detectadas**: Contador total
- **Tiempo entre detecciones**: Para verificar consistencia
- **Falsos positivos**: Detecciones no esperadas

## 🔄 Integración con el Sistema

### En `src/main.py`
```python
# Inicializar sensor
sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
last_sensor_state = sensor.value()

# En el bucle principal
current_sensor_state = sensor.value()
if last_sensor_state == 1 and current_sensor_state == 0:
    print("[TCRT5000] Detección de objeto - Incrementando vuelta")
    race_controller.increment_lap()
last_sensor_state = current_sensor_state
```

### API Web
El sensor se integra automáticamente con el sistema web:
- Las detecciones incrementan el contador de vueltas
- El estado se muestra en la interfaz web
- Los logs aparecen en la consola

## 📝 Notas Importantes

1. **Alimentación**: Usar solo 3.3V, no 5V
2. **Pull-up**: Siempre usar pull-up interno
3. **Debounce**: Implementar debounce para evitar múltiples detecciones
4. **Distancia**: Ajustar según el tipo de objeto a detectar
5. **Limpieza**: Mantener el sensor limpio para mejor detección

## 🚀 Próximos Pasos

1. **Instalar el sensor** según el diagrama de conexión
2. **Ejecutar el test básico** para verificar funcionamiento
3. **Ajustar la distancia** para optimizar detección
4. **Integrar con el sistema** de conteo de vueltas
5. **Probar con coches reales** en la pista 