"""
Test de Conteo del Sensor TCRT5000
Raspberry Pi Pico 2W - MicroPython

Ejecuta este script para probar el conteo de vueltas con el sensor.
"""

import time
from machine import Pin

# Configurar sensor en pin 16
SENSOR_PIN = 16
sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)

print("🏁 Test de Conteo del Sensor TCRT5000")
print("=" * 40)
print(f"✅ Sensor configurado en pin {SENSOR_PIN}")

# Variables de control
lap_count = 0
last_state = sensor.value()
last_detection_time = 0
debounce_time = 100  # ms

# Leer estado inicial
initial_state = sensor.value()
print(f"📊 Estado inicial: {'🔴 Detectado' if initial_state == 0 else '⚪ Libre'}")

print("\n📋 Instrucciones:")
print("  - Pasa un objeto frente al sensor para simular una vuelta")
print("  - El sensor debe contar cada detección")
print("  - Presiona Ctrl+C para detener")
print()

try:
    while True:
        # Leer sensor
        current_state = sensor.value()
        
        # Detectar flanco descendente (HIGH -> LOW)
        if last_state == 1 and current_state == 0:
            current_time = time.ticks_ms()
            time_since_last = time.ticks_diff(current_time, last_detection_time)
            
            if time_since_last > debounce_time:
                lap_count += 1
                last_detection_time = current_time
                print(f"🏁 ¡Vuelta {lap_count} detectada!")
        
        last_state = current_state
        
        # Mostrar estado cada segundo
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print(f"\n⏹️ Test terminado")
    print(f"📈 Vueltas detectadas: {lap_count}") 