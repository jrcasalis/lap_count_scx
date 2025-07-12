# Análisis: Sistema Dual de Contador de Vueltas para Scalextric

## 🎯 Objetivo

Convertir el sistema actual de contador de vueltas en un sistema dual para pistas Scalextric con dos carriles independientes, cada uno con su propio sensor IR y display MAX7219 doble.

## 🚀 Características Objetivo

- **2 carriles independientes** con contadores separados
- **2 sensores TCRT5000** (uno por carril)
- **2 displays MAX7219 dobles** (uno por carril)
- **Interfaz web unificada** para controlar ambos carriles
- **API REST dual** con endpoints separados por carril
- **Misma configuración** de displays (rotación, brillo, orientación)
- **Límite de vueltas compartido** pero contadores independientes

## 🔧 Cambios Necesarios

### 1. Hardware Adicional

#### Sensores
- **Sensor actual**: TCRT5000 en GP16 (Carril 1)
- **Sensor nuevo**: TCRT5000 en GP17 (Carril 2)

#### Displays
- **Display actual**: MAX7219 doble en GP2/3/5 (Carril 1)
- **Display nuevo**: MAX7219 doble en GP6/7/8 (Carril 2)

### 2. Configuración de Pines

```python
# =============================================================================
# CONFIGURACIÓN DE PINES DUAL
# =============================================================================

# Carril 1 (actual)
SENSOR_TCRT5000_PIN_1 = 16  # Sensor carril 1
MAX7219_DIN_PIN_1 = 3       # Display carril 1
MAX7219_CS_PIN_1 = 5
MAX7219_CLK_PIN_1 = 2

# Carril 2 (nuevo)
SENSOR_TCRT5000_PIN_2 = 17  # Sensor carril 2
MAX7219_DIN_PIN_2 = 6       # Display carril 2
MAX7219_CS_PIN_2 = 7
MAX7219_CLK_PIN_2 = 8

# Configuración compartida
LED_PIN_RED = 0              # LED indicador (compartido)
RACE_MAX_LAPS = 15           # Límite compartido para ambos carriles
```

### 3. Estructura de Archivos Propuesta

```
src/
├── main_dual.py                    # Arranque principal dual
├── dual_race_controller.py         # Controlador dual principal
├── lane_controller.py              # Controlador individual por carril
├── dual_display_manager.py         # Gestor de displays duales
├── web_server_dual.py              # Servidor web con APIs duales
├── config_dual.py                  # Configuración dual
└── [archivos actuales]             # Mantener compatibilidad

examples/
├── test_dual_race.py               # Prueba sistema dual completo
├── test_dual_displays.py           # Prueba displays duales
├── test_scalextric_setup.py        # Prueba setup Scalextric
└── test_dual_web_integration.py    # Prueba integración web dual

web/
├── index_dual.html                 # Interfaz web dual
├── style_dual.css                  # Estilos para interfaz dual
└── script_dual.js                  # JavaScript dual
```

## 📋 Plan de Implementación

### **Fase 1: Preparación y Configuración**
1. **Crear `config_dual.py`**
   - Configuración de pines duales
   - Parámetros compartidos
   - Configuración de displays duales

2. **Crear `lane_controller.py`**
   - Versión simplificada del `race_controller.py` actual
   - Control individual por carril
   - Gestión de sensor y display individual

3. **Crear `dual_race_controller.py`**
   - Coordinación de dos carriles
   - Gestión de estado dual
   - APIs para control dual

### **Fase 2: Gestión de Displays Duales**
1. **Crear `dual_display_manager.py`**
   - Inicialización de dos displays MAX7219
   - Sincronización de configuraciones
   - Métodos para actualizar ambos displays

2. **Configuración de Displays**
   - Misma rotación, brillo y orientación
   - Centrado automático en ambos displays
   - Animaciones sincronizadas

### **Fase 3: API y Servidor Web Dual**
1. **Crear `web_server_dual.py`**
   - Endpoints para carril 1: `/api/lane1/*`
   - Endpoints para carril 2: `/api/lane2/*`
   - Endpoints duales: `/api/dual/*`

2. **Nuevos Endpoints de API**
   ```
   # Carril 1
   GET /api/lane1/increment
   GET /api/lane1/reset
   GET /api/lane1/status
   
   # Carril 2
   GET /api/lane2/increment
   GET /api/lane2/reset
   GET /api/lane2/status
   
   # Control dual
   GET /api/dual/status
   GET /api/dual/reset
   GET /api/dual/start
   ```

### **Fase 4: Interfaz Web Dual**
1. **Crear `index_dual.html`**
   - Dos secciones independientes
   - Contadores separados por carril
   - Botones de control individuales

2. **Crear `script_dual.js`**
   - Manejo de APIs duales
   - Actualización en tiempo real
   - Control de estado dual

### **Fase 5: Integración y Pruebas**
1. **Crear `main_dual.py`**
   - Inicialización del sistema dual
   - Gestión de sensores duales
   - Servidor web dual

2. **Crear ejemplos de prueba**
   - Pruebas de displays duales
   - Pruebas de sensores duales
   - Pruebas de integración web

## 🔌 Conexiones de Hardware Detalladas

### **Carril 1 (actual)**
```
Sensor TCRT5000:
  VCC → 3.3V
  GND → GND
  OUT → GP16

Display MAX7219 Doble:
  DIN → GP3
  CS → GP5
  CLK → GP2
  VCC → 3.3V
  GND → GND
```

### **Carril 2 (nuevo)**
```
Sensor TCRT5000:
  VCC → 3.3V
  GND → GND
  OUT → GP17

Display MAX7219 Doble:
  DIN → GP6
  CS → GP7
  CLK → GP8
  VCC → 3.3V
  GND → GND
```

### **LED Indicador (compartido)**
```
LED Rojo:
  + → GP0 (con resistencia 220Ω)
  - → GND
```

## 📊 Estructura de Datos

### **Estado Dual**
```python
dual_status = {
    "lane1": {
        "current_laps": 7,
        "max_laps": 15,
        "remaining_laps": 8,
        "is_completed": False,
        "progress_percentage": 46.7,
        "display_status": "active"
    },
    "lane2": {
        "current_laps": 12,
        "max_laps": 15,
        "remaining_laps": 3,
        "is_completed": False,
        "progress_percentage": 80.0,
        "display_status": "active"
    },
    "race_status": "active",  # "active", "completed", "paused"
    "winner": None  # "lane1", "lane2", None
}
```

### **Configuración Dual**
```python
dual_config = {
    "max_laps": 15,
    "auto_reset": True,
    "show_animations": True,
    "displays": {
        "brightness": 8,
        "rotation": 90,
        "orientation": "horizontal"
    },
    "sensors": {
        "debounce_time": 0.1,
        "auto_increment": True
    }
}
```

## 🎮 Funcionalidades Específicas

### **Control Individual**
- Incrementar vueltas por carril independiente
- Reiniciar carrera por carril
- Ver estado individual de cada carril

### **Control Dual**
- Reiniciar ambas carreras simultáneamente
- Iniciar carrera dual (ambos en 0)
- Detectar ganador automáticamente

### **Animaciones Duales**
- Animación de bandera a cuadros en ambos displays
- Animación de victoria en el carril ganador
- Animación de empate si ambos completan simultáneamente

### **Interfaz Web**
- Dos paneles independientes (Carril 1 y Carril 2)
- Contadores en tiempo real
- Botones de control individuales
- Vista de estado dual
- Notificaciones de eventos

## 🔍 Consideraciones Técnicas

### **Memoria y Performance**
- Dos displays MAX7219 = mayor uso de memoria
- Dos sensores = mayor procesamiento
- Optimización necesaria para MicroPython

### **Sincronización**
- Ambos displays deben mantener configuración idéntica
- Sensores deben tener debounce independiente
- APIs deben ser thread-safe

### **Escalabilidad**
- Estructura preparada para más carriles
- Configuración centralizada
- APIs extensibles

### **Compatibilidad**
- Mantener compatibilidad con sistema actual
- Archivos duales separados del sistema actual
- Posibilidad de migración gradual

## 📝 Próximos Pasos

1. **Crear configuración dual** (`config_dual.py`)
2. **Implementar controlador de carril individual** (`lane_controller.py`)
3. **Desarrollar gestor de displays duales** (`dual_display_manager.py`)
4. **Crear controlador dual** (`dual_race_controller.py`)
5. **Implementar servidor web dual** (`web_server_dual.py`)
6. **Desarrollar interfaz web dual**
7. **Crear ejemplos de prueba**
8. **Documentar sistema dual**

## 🎯 Beneficios del Sistema Dual

1. **Independencia total**: Cada carril funciona por separado
2. **Misma configuración**: Ambos displays con misma rotación/brillo
3. **API separada**: Control individual de cada carril
4. **Interfaz unificada**: Una sola web para controlar ambos
5. **Escalabilidad**: Fácil agregar más carriles en el futuro
6. **Compatibilidad**: Mantiene funcionalidad del sistema actual
7. **Flexibilidad**: Configuración independiente por carril
8. **Robustez**: Sistema tolerante a fallos individuales

---

**Nota**: Este análisis sirve como guía para la implementación del sistema dual de Scalextric. Se puede implementar por fases manteniendo la funcionalidad actual intacta. 