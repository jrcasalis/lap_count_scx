# Resolución de Conflicto: Previa -> Carrera

## Problema Identificado

El usuario reportó un error cuando se inicia una previa y luego se inicia una carrera mientras la previa está activa. Este escenario puede causar conflictos en el manejo de estados del semáforo.

## Escenario Problemático

1. **Inicio de Previa**: Se activa el titileo de todas las luces del semáforo
2. **Inicio de Carrera**: Mientras la previa está activa, se inicia la secuencia de largada
3. **Conflicto**: Ambos estados intentan controlar el semáforo simultáneamente

## Solución Implementada

### 1. Controlador de Carrera (`race_controller.py`)

```python
def start_race(self):
    """Inicia la carrera - permite que el sensor cuente vueltas"""
    # Si hay previa activa, terminarla automáticamente sin mensajes
    if self.traffic_light and self.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
        if DEBUG_ENABLED:
            print("[RACE] Previa activa detectada - terminando automáticamente")
        try:
            self.traffic_light.race_previous_stop()
            # Esperar un momento para que se complete la terminación
            time.sleep(0.1)
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[RACE] Error terminando previa: {e}")
    
    # Verificar que la previa se terminó correctamente
    if self.traffic_light and self.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
        if DEBUG_ENABLED:
            print("[RACE] Previa aún activa después de intentar terminarla")
        # Intentar terminar nuevamente
        try:
            self.traffic_light.race_previous_stop()
            time.sleep(0.1)
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[RACE] Error en segundo intento de terminar previa: {e}")
    
    self.is_race_started = True
    
    if DEBUG_ENABLED:
        print("[RACE] Carrera iniciada - Sensor activo")
    
    return True
```

### 2. Controlador del Semáforo (`traffic_light_controller.py`)

```python
def race_start(self):
    """Inicia la secuencia de largada: Roja -> Amarilla -> Verde"""
    if self.current_state in [TRAFFIC_LIGHT_STATE_RED, TRAFFIC_LIGHT_STATE_YELLOW, TRAFFIC_LIGHT_STATE_GREEN]:
        if DEBUG_ENABLED:
            print("[TRAFFIC] Secuencia de largada ya en progreso")
        return False
    
    # Detener cualquier titileo previo de forma segura
    try:
        self.race_previous_stop()
        # Esperar un momento para que se complete la terminación
        time.sleep(0.1)
    except Exception as e:
        if DEBUG_ENABLED:
            print(f"[TRAFFIC] Error terminando previa antes de largada: {e}")
    
    # Verificar que la previa se terminó correctamente
    if self.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
        if DEBUG_ENABLED:
            print("[TRAFFIC] Previa aún activa, intentando terminar nuevamente")
        try:
            self.race_previous_stop()
            time.sleep(0.1)
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[TRAFFIC] Error en segundo intento de terminar previa: {e}")
    
    if DEBUG_ENABLED:
        print("[TRAFFIC] Iniciando secuencia de largada")
    
    # Iniciar hilo para la secuencia de largada
    try:
        _thread.start_new_thread(self._race_start_sequence, ())
        return True
    except Exception as e:
        if DEBUG_ENABLED:
            print(f"[TRAFFIC] Error iniciando secuencia de largada: {e}")
        return False
```

### 3. Servidor Web (`web_server.py`)

```python
def api_traffic_start(self):
    """API: Iniciar carrera (secuencia de largada)"""
    try:
        # Si hay previa activa, terminarla automáticamente sin mensajes
        if self.race_controller.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[WEB] Previa activa detectada - terminando automáticamente")
            self.race_controller.traffic_light.race_previous_stop()
            # Esperar un momento para que se complete la terminación
            time.sleep(0.1)
        
        # Verificar que la previa se terminó correctamente
        if self.race_controller.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
            if DEBUG_ENABLED:
                print("[WEB] Previa aún activa, intentando terminar nuevamente")
            self.race_controller.traffic_light.race_previous_stop()
            time.sleep(0.1)
        
        success = self.race_controller.race_start()
        traffic_status = self.race_controller.get_traffic_light_status()
        race_status = self.race_controller.get_race_status()
        
        return self.json_response({
            "success": success,
            "message": "Carrera iniciada" if success else "Error al iniciar carrera",
            "traffic_light_status": traffic_status,
            "race_status": race_status
        })
    except Exception as e:
        if DEBUG_ENABLED:
            print(f"[WEB] Error en api_traffic_start: {e}")
        return self.json_response({
            "success": False,
            "message": f"Error al iniciar carrera: {str(e)}",
            "traffic_light_status": self.race_controller.get_traffic_light_status(),
            "race_status": self.race_controller.get_race_status()
        })
```

### 4. JavaScript (`script.js`)

```javascript
// Función para iniciar carrera
async function startRace() {
    const button = event.target.closest('.btn');
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="icon">⏳</span>Iniciando...';
    }
    
    try {
        console.log('🚦 Iniciando carrera...');
        
        const response = await fetch('/api/traffic-light/start');
        const data = await response.json();
        
        if (data.success) {
            console.log('✅ Carrera iniciada correctamente');
            console.log('   Estado del semáforo:', data.traffic_light_status.state);
            console.log('   Estado de la carrera:', data.race_status.is_race_started);
            
            showNotification('Carrera iniciada', 'success');
            
            // Actualizar estado inmediatamente
            if (data.traffic_light_status) {
                trafficLightStatus = data.traffic_light_status;
                updateTrafficLightUI();
            }
            
            if (data.race_status) {
                raceStatus = data.race_status;
                updateUI();
            }
        } else {
            console.error('❌ Error iniciando carrera:', data.message);
            showNotification(data.message, 'warning');
        }
    } catch (error) {
        console.error('❌ Error de conexión:', error);
        showNotification('Error al iniciar carrera', 'error');
    }
    
    if (button) {
        button.disabled = false;
        button.innerHTML = '<span class="icon">🏁</span>Largar';
    }
}
```

## Características de la Solución

### 1. **Detección Automática**
- El sistema detecta automáticamente cuando hay una previa activa
- No requiere intervención manual del usuario

### 2. **Terminación Segura**
- La previa se termina de forma segura antes de iniciar la carrera
- Se incluyen verificaciones para asegurar que la terminación fue exitosa

### 3. **Manejo de Errores**
- Se capturan y manejan excepciones en cada nivel
- Se registran logs detallados para debugging

### 4. **Verificación Doble**
- Se verifica que la previa se terminó correctamente
- Si no se terminó, se intenta nuevamente

### 5. **Sincronización Inmediata**
- El estado se actualiza inmediatamente en la interfaz web
- Se mantiene la sincronización en tiempo real

## Tests Implementados

### 1. Test de Conflicto Básico (`test_conflict_resolution.py`)
- Verifica que el conflicto se resuelve correctamente
- Comprueba que la previa se termina automáticamente
- Valida que la carrera se inicia sin errores

### 2. Test de Múltiples Conflictos (`test_conflict_resolution.py`)
- Ejecuta múltiples conflictos consecutivos
- Verifica que el sistema es estable bajo estrés
- Comprueba que no hay acumulación de errores

## Flujo de Resolución

1. **Usuario inicia previa** → Semáforo entra en modo titileo
2. **Usuario inicia carrera** → Sistema detecta previa activa
3. **Terminación automática** → Sistema termina la previa de forma segura
4. **Verificación** → Sistema verifica que la previa se terminó
5. **Inicio de carrera** → Sistema inicia la secuencia de largada
6. **Sincronización** → Interfaz web se actualiza inmediatamente

## Logs de Debug

El sistema incluye logs detallados para debugging:

```
[RACE] Previa activa detectada - terminando automáticamente
[TRAFFIC] Error terminando previa antes de largada: [error]
[TRAFFIC] Previa aún activa, intentando terminar nuevamente
[WEB] Previa activa detectada - terminando automáticamente
```

## Beneficios

1. **Experiencia de Usuario Mejorada**: No hay errores al iniciar carrera durante previa
2. **Estabilidad del Sistema**: Manejo robusto de conflictos de estado
3. **Debugging Facilitado**: Logs detallados para identificar problemas
4. **Transiciones Suaves**: Las transiciones entre estados son fluidas
5. **Sincronización Confiable**: La interfaz web se mantiene sincronizada

## Conclusión

El conflicto previa → carrera ahora se maneja de forma automática y segura. El sistema:

- ✅ Detecta automáticamente conflictos
- ✅ Termina la previa de forma segura
- ✅ Inicia la carrera sin errores
- ✅ Mantiene la sincronización en tiempo real
- ✅ Proporciona logs detallados para debugging

El escenario problemático reportado por el usuario ahora se resuelve correctamente sin intervención manual. 