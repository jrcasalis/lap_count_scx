"""
Test de Debug del Sensor IR TCRT5000
Raspberry Pi Pico 2W - MicroPython

Test detallado para diagnosticar problemas con el sensor.
"""

import time
from machine import Pin

# Configurar sensor en pin 16
SENSOR_PIN = 16
sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)

print("🔍 Test de Debug del Sensor IR TCRT5000")
print("=" * 50)
print(f"✅ Sensor configurado en pin {SENSOR_PIN}")

# Leer estado inicial
initial_state = sensor.value()
print(f"📊 Estado inicial: {initial_state}")

print("\n📋 Información del Sensor:")
print(f"  - Pin: GP{SENSOR_PIN}")
print(f"  - Tipo: TCRT5000 (3 pines: VCC, GND, OUT)")
print(f"  - Lógica: LOW (0) cuando detecta, HIGH (1) cuando no detecta")
print(f"  - Pull-up: Habilitado")
print()

print("🔧 Diagnóstico:")
print("1. Verificando conexiones...")
print("   - VCC debe estar conectado a 3.3V")
print("   - GND debe estar conectado a GND")
print("   - OUT debe estar conectado a GP16")
print()

print("2. Verificando funcionamiento...")
print("   - Estado inicial debe ser 1 (libre)")
print("   - Con objeto cerca debe cambiar a 0 (detectado)")
print("   - Sin objeto debe volver a 1 (libre)")
print()

print("3. Test de lectura continua:")
print("   - Acerca y aleja objetos frente al sensor")
print("   - Observa los cambios en tiempo real")
print("   - Presiona Ctrl+C para detener")
print()

try:
    while True:
        # Leer sensor
        current_state = sensor.value()
        
        # Mostrar valor con más información
        status = "🔴 DETECTADO" if current_state == 0 else "⚪ LIBRE"
        print(f"\r📊 Valor: {current_state} | Estado: {status}", end="")
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n⏹️ Test terminado")
    print("\n📋 Resumen:")
    print("  - Si siempre muestra 1: Verificar conexiones o sensor")
    print("  - Si siempre muestra 0: Verificar GND o sensor")
    print("  - Si cambia correctamente: Sensor funciona bien") 