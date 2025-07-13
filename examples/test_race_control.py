"""
Test de Control de Carrera con Sensor IR
Raspberry Pi Pico 2W - MicroPython

Este test verifica que el sensor solo cuente vueltas cuando la carrera esté iniciada.
"""

import time
from machine import Pin
from config import SENSOR_TCRT5000_PIN

def test_race_control():
    """Test del control de carrera con sensor"""
    print("🏁 Test de Control de Carrera con Sensor IR")
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
    print("  1. La carrera inicia en estado 'No iniciada'")
    print("  2. El sensor NO debe contar vueltas hasta que inicies la carrera")
    print("  3. Simula iniciar la carrera (cambia race_started = True)")
    print("  4. Ahora el sensor debe contar vueltas")
    print("  5. Simula detener la carrera (cambia race_started = False)")
    print("  6. El sensor NO debe contar vueltas")
    print("  7. Presiona Ctrl+C para detener")
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
            
            # Mostrar estado cada segundo
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Test terminado")
        print(f"📈 Vueltas detectadas: {lap_count}")

def test_manual_race_control():
    """Test manual del control de carrera"""
    print("\n🎮 Test Manual de Control de Carrera")
    print("=" * 50)
    
    # Configurar sensor
    sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
    
    # Variables de control
    lap_count = 0
    last_sensor_state = sensor.value()
    last_detection_time = 0
    debounce_time = 100  # ms
    race_started = False  # Estado de la carrera
    
    print("📋 Instrucciones:")
    print("  - Escribe 'start' para iniciar la carrera")
    print("  - Escribe 'stop' para detener la carrera")
    print("  - Escribe 'status' para ver el estado")
    print("  - Escribe 'quit' para salir")
    print("  - Pasa objetos frente al sensor para probar")
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
            
            # Pequeña pausa
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Test terminado")
        print(f"📈 Vueltas detectadas: {lap_count}")

def main():
    """Función principal"""
    print("🏁 Test de Control de Carrera con Sensor IR")
    print("=" * 50)
    
    print("Elige el test:")
    print("1. Test automático")
    print("2. Test manual")
    print()
    
    try:
        choice = input("Ingresa tu elección (1 o 2): ")
        
        if choice == "1":
            test_race_control()
        elif choice == "2":
            test_manual_race_control()
        else:
            print("Opción no válida. Ejecutando test automático...")
            test_race_control()
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrumpido")

if __name__ == "__main__":
    main() 