"""
Test del RaceController con sistema de polling (sin hilos)
Raspberry Pi Pico 2W - MicroPython

Este test demuestra cómo usar el nuevo sistema de polling para evitar conflictos de hilos.
"""

import time
import sys
import os

# Agregar la raíz del proyecto y src al path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
PATTERNS_DIR = os.path.join(ROOT_DIR, 'patterns')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if PATTERNS_DIR not in sys.path:
    sys.path.insert(0, PATTERNS_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Mock de las dependencias de MicroPython
class MockPin:
    def __init__(self, pin_id, mode=None, pull=None):
        self.pin_id = pin_id
        self.mode = mode
        self.pull = pull
        self._value = 1
    
    def value(self, val=None):
        if val is not None:
            self._value = val
        return self._value

class MockPWM:
    def __init__(self, pin, freq=1000):
        self.pin = pin
        self.freq = freq
        self._duty = 0
    
    def duty_u16(self, duty=None):
        if duty is not None:
            self._duty = duty
        return self._duty
    
    def deinit(self):
        pass

class MockSPI:
    def __init__(self, id, baudrate=10000000, polarity=0, phase=0, sck=None, mosi=None):
        self.id = id
        self.baudrate = baudrate
        self.polarity = polarity
        self.phase = phase
        self.sck = sck
        self.mosi = mosi
    
    def write(self, data):
        print(f"[MOCK_SPI] Escribiendo: {data}")

# Crear módulo mock para machine
class MockMachine:
    Pin = MockPin
    PWM = MockPWM
    SPI = MockSPI

# Reemplazar módulos de MicroPython
sys.modules['machine'] = MockMachine()

# Importar después de los mocks
from race_controller import RaceController
from traffic_light_controller import TrafficLightController
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable

def test_polling_system():
    """Test del sistema de polling"""
    print("🔄 Test del Sistema de Polling")
    print("=" * 50)
    
    try:
        # Inicializar controlador
        print("1. Inicializando RaceController...")
        RaceController.__init__(max_laps=5, num_racers=2, racer_names=["Piloto A", "Piloto B"])
        print("✅ RaceController inicializado")
        
        # Mostrar parámetros iniciales
        print("\n2. Parámetros iniciales:")
        params = RaceController.get_race_params()
        for key, value in params.items():
            print(f"   {key}: {value}")
        
        # Test 1: Iniciar previa con polling
        print("\n3. Test: Iniciar previa (modo polling)...")
        result = RaceController.start_race_previous()
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Previa iniciada correctamente")
            
            # Simular bucle principal con polling
            print("\n4. Simulando bucle principal con polling...")
            print("   (El titileo del semáforo se actualiza en cada iteración)")
            
            for i in range(10):  # 10 iteraciones = 5 segundos
                print(f"   Iteración {i+1}/10...")
                RaceController.update()  # Actualizar titileo del semáforo
                time.sleep(0.5)  # Simular 0.5 segundos
            
            # Test 2: Detener previa
            print("\n5. Test: Detener previa...")
            result = RaceController.stop_race_previous()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Previa detenida correctamente")
        
        # Test 3: Iniciar carrera
        print("\n6. Test: Iniciar carrera...")
        result = RaceController.start_race()
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Carrera iniciada correctamente")
            
            # Simular bucle principal durante la carrera
            print("\n7. Simulando bucle principal durante la carrera...")
            for i in range(15):  # 15 iteraciones = 7.5 segundos
                print(f"   Iteración {i+1}/15...")
                RaceController.update()  # Actualizar titileo del semáforo
                time.sleep(0.5)
            
            # Test 4: Detener carrera
            print("\n8. Test: Detener carrera...")
            result = RaceController.stop_race()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Carrera detenida correctamente")
        
        print("\n✅ Test del sistema de polling completado")
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")

def test_traffic_light_polling():
    """Test específico del semáforo con polling"""
    print("🚦 Test del Semáforo con Polling")
    print("=" * 50)
    
    try:
        # Crear instancia del semáforo
        print("1. Creando TrafficLightController...")
        traffic_light = TrafficLightController()
        print("✅ TrafficLightController creado")
        
        # Test 1: Iniciar previa
        print("\n2. Test: Iniciar previa...")
        result = traffic_light.race_previous()
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Previa iniciada correctamente")
            
            # Simular bucle principal
            print("\n3. Simulando bucle principal...")
            for i in range(10):
                print(f"   Iteración {i+1}/10...")
                traffic_light.update_blinking()
                time.sleep(0.5)
            
            # Test 2: Detener previa
            print("\n4. Test: Detener previa...")
            result = traffic_light.race_previous_stop()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Previa detenida correctamente")
        
        # Test 3: Obtener estado
        print("\n5. Test: Obtener estado...")
        status = traffic_light.get_thread_status()
        print(f"   Estado: {status}")
        
        print("\n✅ Test del semáforo con polling completado")
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")

def main():
    """Función principal"""
    print("🔄 Test del Sistema de Polling")
    print("=" * 50)
    
    print("Elige el test:")
    print("1. Test completo del sistema de polling")
    print("2. Test solo del semáforo con polling")
    print("3. Ambos tests")
    print()
    
    try:
        choice = input("Ingresa tu elección (1, 2 o 3): ").strip()
        
        if choice == "1":
            test_polling_system()
        elif choice == "2":
            test_traffic_light_polling()
        elif choice == "3":
            test_traffic_light_polling()
            print("\n" + "="*50)
            test_polling_system()
        else:
            print("Opción no válida. Ejecutando test completo...")
            test_polling_system()
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrumpido")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 