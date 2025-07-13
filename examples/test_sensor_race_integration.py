"""
Test de Integración del Sensor con Sistema de Carrera
Raspberry Pi Pico 2W - MicroPython

Este test verifica que el sensor funcione correctamente con el control de carrera.
"""

import time
from machine import Pin
from config import SENSOR_TCRT5000_PIN

def test_sensor_race_integration():
    """Test de integración del sensor con el sistema de carrera"""
    print("🏁 Test de Integración Sensor + Carrera")
    print("=" * 50)
    
    # Configurar sensor
    sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
    
    # Variables de control
    lap_count = 0
    last_sensor_state = sensor.value()
    last_detection_time = 0
    debounce_time = 100  # ms
    race_started = False  # Estado de la carrera
    
    print(f"✅ Sensor configurado en pin {SENSOR_TCRT5000_PIN}")
    print(f"📊 Estado inicial: {'🔴 Detectado' if last_sensor_state == 0 else '⚪ Libre'}")
    print(f"🏁 Estado de carrera: {'🟢 Iniciada' if race_started else '🔴 No iniciada'}")
    
    print("\n📋 Instrucciones:")
    print("  1. Simula el semáforo iniciando la carrera (cambia race_started = True)")
    print("  2. Pasa objetos frente al sensor")
    print("  3. Verifica que solo cuente cuando la carrera esté iniciada")
    print("  4. Simula detener la carrera (cambia race_started = False)")
    print("  5. Verifica que no cuente cuando la carrera esté detenida")
    print("  6. Presiona Ctrl+C para detener")
    print()
    
    try:
        while True:
            # Leer sensor
            current_state = sensor.value()
            
            # Detectar flanco descendente (HIGH -> LOW)
            if last_sensor_state == 1 and current_state == 0:
                current_time = time.ticks_ms()
                time_since_last = time.ticks_diff(current_time, last_detection_time)
                
                if time_since_last > debounce_time:
                    last_detection_time = current_time
                    
                    # Solo contar si la carrera está iniciada
                    if race_started:
                        lap_count += 1
                        print(f"🏁 ¡Vuelta {lap_count} detectada! (Carrera iniciada)")
                    else:
                        print(f"⚠️ Detección ignorada (Carrera no iniciada)")
            
            last_sensor_state = current_state
            
            # Mostrar estado cada 2 segundos
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Test terminado")
        print(f"📈 Vueltas detectadas: {lap_count}")

def test_semaphore_race_start():
    """Test que simula el comportamiento del semáforo"""
    print("\n🚦 Test de Semáforo + Inicio de Carrera")
    print("=" * 50)
    
    # Configurar sensor
    sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
    
    # Variables de control
    lap_count = 0
    last_sensor_state = sensor.value()
    last_detection_time = 0
    debounce_time = 100  # ms
    race_started = False  # Estado de la carrera
    
    print("📋 Simulación de secuencia de semáforo:")
    print("  1. Semáforo en rojo (carrera no iniciada)")
    print("  2. Semáforo en amarillo (carrera no iniciada)")
    print("  3. Semáforo en verde (carrera iniciada automáticamente)")
    print("  4. Pasa objetos frente al sensor")
    print()
    
    # Simular secuencia del semáforo
    print("🔴 Semáforo en ROJO (carrera no iniciada)")
    time.sleep(2)
    
    print("🟡 Semáforo en AMARILLO (carrera no iniciada)")
    time.sleep(2)
    
    print("🟢 Semáforo en VERDE - ¡CARRERA INICIADA!")
    race_started = True
    time.sleep(1)
    
    print("\n📋 Ahora pasa objetos frente al sensor...")
    print("   - El sensor debe contar vueltas")
    print("   - Presiona Ctrl+C para detener")
    print()
    
    try:
        while True:
            # Leer sensor
            current_state = sensor.value()
            
            # Detectar flanco descendente (HIGH -> LOW)
            if last_sensor_state == 1 and current_state == 0:
                current_time = time.ticks_ms()
                time_since_last = time.ticks_diff(current_time, last_detection_time)
                
                if time_since_last > debounce_time:
                    last_detection_time = current_time
                    
                    # Solo contar si la carrera está iniciada
                    if race_started:
                        lap_count += 1
                        print(f"🏁 ¡Vuelta {lap_count} detectada!")
                    else:
                        print(f"⚠️ Detección ignorada (Carrera no iniciada)")
            
            last_sensor_state = current_state
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Test terminado")
        print(f"📈 Vueltas detectadas: {lap_count}")

def main():
    """Función principal"""
    print("🏁 Test de Integración Sensor + Sistema de Carrera")
    print("=" * 60)
    
    print("Elige el test:")
    print("1. Test básico de integración")
    print("2. Test de semáforo + inicio de carrera")
    print()
    
    try:
        choice = input("Ingresa tu elección (1 o 2): ")
        
        if choice == "1":
            test_sensor_race_integration()
        elif choice == "2":
            test_semaphore_race_start()
        else:
            print("Opción no válida. Ejecutando test básico...")
            test_sensor_race_integration()
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrumpido")

if __name__ == "__main__":
    main() 