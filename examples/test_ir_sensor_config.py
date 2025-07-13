"""
Test de Configuración del Sensor IR TCRT5000
Raspberry Pi Pico 2W - MicroPython

Prueba diferentes configuraciones del pin para diagnosticar problemas.
"""

import time
from machine import Pin

# Configurar sensor en pin 16
SENSOR_PIN = 16

print("🔍 Test de Configuración del Sensor IR TCRT5000")
print("=" * 50)
print(f"✅ Probando diferentes configuraciones en pin {SENSOR_PIN}")

def test_config_with_pull_up():
    """Test con pull-up interno"""
    print("\n1️⃣ Test con Pull-Up Interno:")
    sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
    
    try:
        for i in range(10):
            current_state = sensor.value()
            status = "🔴 DETECTADO" if current_state == 0 else "⚪ LIBRE"
            print(f"   Lectura {i+1}: {current_state} | {status}")
            time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_config_without_pull():
    """Test sin pull-up"""
    print("\n2️⃣ Test sin Pull-Up:")
    sensor = Pin(SENSOR_PIN, Pin.IN)
    
    try:
        for i in range(10):
            current_state = sensor.value()
            status = "🔴 DETECTADO" if current_state == 0 else "⚪ LIBRE"
            print(f"   Lectura {i+1}: {current_state} | {status}")
            time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_config_with_pull_down():
    """Test con pull-down"""
    print("\n3️⃣ Test con Pull-Down:")
    sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_DOWN)
    
    try:
        for i in range(10):
            current_state = sensor.value()
            status = "🔴 DETECTADO" if current_state == 0 else "⚪ LIBRE"
            print(f"   Lectura {i+1}: {current_state} | {status}")
            time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_continuous_reading():
    """Test de lectura continua"""
    print("\n4️⃣ Test de Lectura Continua:")
    sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
    
    print("   📋 Instrucciones:")
    print("   - Acerca un objeto frente al sensor")
    print("   - Observa los cambios en tiempo real")
    print("   - Presiona Ctrl+C para detener")
    print()
    
    try:
        while True:
            current_state = sensor.value()
            status = "🔴 DETECTADO" if current_state == 0 else "⚪ LIBRE"
            print(f"\r   📊 Valor: {current_state} | Estado: {status}", end="")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n   ⏹️ Test terminado")

def main():
    """Función principal"""
    print("🔧 Diagnóstico de Configuración del Sensor")
    print("=" * 50)
    
    # Test 1: Con pull-up
    test_config_with_pull_up()
    
    # Test 2: Sin pull
    test_config_without_pull()
    
    # Test 3: Con pull-down
    test_config_with_pull_down()
    
    # Test 4: Lectura continua
    test_continuous_reading()
    
    print("\n📋 Resumen de Diagnóstico:")
    print("  - Si todas las lecturas son 1: Verificar conexiones")
    print("  - Si todas las lecturas son 0: Verificar GND")
    print("  - Si hay cambios: Sensor funciona")
    print("  - Si hay errores: Verificar pin o sensor")

if __name__ == "__main__":
    main() 