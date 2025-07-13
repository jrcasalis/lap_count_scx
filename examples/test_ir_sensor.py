"""
Test Simple del Sensor IR TCRT5000
Raspberry Pi Pico 2W - MicroPython

Solo lee el sensor y muestra 0 o 1 por consola.
"""

import time
from machine import Pin

# Configurar sensor en pin 16
SENSOR_PIN = 16
sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)

print("🔍 Test Simple del Sensor IR TCRT5000")
print("=" * 40)
print(f"✅ Sensor configurado en pin {SENSOR_PIN}")

# Leer estado inicial
initial_state = sensor.value()
print(f"📊 Estado inicial: {initial_state}")

print("\n📋 Instrucciones:")
print("  - Acerca un objeto frente al sensor")
print("  - Observa cómo cambia el valor (0 o 1)")
print("  - Presiona Ctrl+C para detener")
print()

try:
    while True:
        # Leer sensor
        current_state = sensor.value()
        
        # Mostrar valor
        print(f"\r📊 Valor: {current_state}", end="")
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n⏹️ Test terminado") 