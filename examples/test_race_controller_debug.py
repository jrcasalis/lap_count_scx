"""
Test de Debug del RaceController
Simula el comportamiento sin dependencias de MicroPython
"""

import sys
import os
import time

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
        self._value = 1  # Por defecto HIGH
    
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

# Mock de _thread
class MockThread:
    @staticmethod
    def start_new_thread(func, args):
        print(f"[MOCK_THREAD] Iniciando hilo: {func.__name__}")
        # Simular ejecución en hilo separado
        import threading
        thread = threading.Thread(target=func, args=args)
        thread.daemon = True
        thread.start()
        return thread

# Crear módulo mock para machine
class MockMachine:
    Pin = MockPin
    PWM = MockPWM
    SPI = MockSPI

# Crear módulo mock para _thread
class MockThreadModule:
    start_new_thread = MockThread.start_new_thread

# Reemplazar módulos de MicroPython
sys.modules['machine'] = MockMachine()
sys.modules['_thread'] = MockThreadModule()

# Importar después de los mocks
from race_controller import RaceController
from traffic_light_controller import TrafficLightController
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable

def test_race_controller():
    """Test completo del RaceController (usando métodos de clase)"""
    print("🏁 Test de Debug del RaceController")
    print("=" * 50)
    
    try:
        # Inicializar parámetros de carrera
        print("1. Inicializando RaceController...")
        RaceController.__init__(max_laps=5, num_racers=2, racer_names=["Piloto A", "Piloto B"])
        print("✅ RaceController inicializado")
        
        # Mostrar parámetros iniciales
        print("\n2. Parámetros iniciales:")
        params = RaceController.get_race_params()
        for key, value in params.items():
            print(f"   {key}: {value}")
        
        # Test 1: Iniciar previa
        print("\n3. Test: Iniciar previa...")
        result = RaceController.start_race_previous()
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Previa iniciada correctamente")
            time.sleep(2)  # Esperar 2 segundos
            
            # Test 2: Detener previa
            print("\n4. Test: Detener previa...")
            result = RaceController.stop_race_previous()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Previa detenida correctamente")
        
        # Test 3: Iniciar carrera
        print("\n5. Test: Iniciar carrera...")
        result = RaceController.start_race()
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Carrera iniciada correctamente")
            time.sleep(5)  # Esperar 5 segundos para ver la secuencia
            
            # Test 4: Detener carrera
            print("\n6. Test: Detener carrera...")
            result = RaceController.stop_race()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Carrera detenida correctamente")
        
        # Test 5: Cambiar estado manualmente
        print("\n7. Test: Cambiar estado a FINISHED...")
        result = RaceController.set_race_state("FINISHED")
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Estado cambiado a FINISHED")
        
        # Test 6: Control de titileo
        print("\n8. Test: Control de titileo...")
        print(f"   Titileo actual: {RaceController.get_stopped_blink_status()}")
        
        RaceController.set_stopped_blink(False)
        print(f"   Titileo después de deshabilitar: {RaceController.get_stopped_blink_status()}")
        
        RaceController.set_stopped_blink(True)
        print(f"   Titileo después de habilitar: {RaceController.get_stopped_blink_status()}")
        
        print("\n✅ Todos los tests completados")
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        # No usar traceback para evitar problemas con _thread

def test_traffic_light_only():
    """Test solo del controlador del semáforo"""
    print("🚦 Test de Debug del TrafficLightController")
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
            time.sleep(3)  # Esperar 3 segundos
            
            # Test 2: Detener previa
            print("\n3. Test: Detener previa...")
            result = traffic_light.race_previous_stop()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Previa detenida correctamente")
        
        # Test 3: Iniciar secuencia de largada
        print("\n4. Test: Iniciar secuencia de largada...")
        result = traffic_light.race_start()
        print(f"   Resultado: {result}")
        
        if result:
            print("   ✅ Secuencia de largada iniciada correctamente")
            time.sleep(10)  # Esperar 10 segundos para ver toda la secuencia
            
            # Test 4: Detener carrera
            print("\n5. Test: Detener carrera...")
            result = traffic_light.race_stop()
            print(f"   Resultado: {result}")
            
            if result:
                print("   ✅ Carrera detenida correctamente")
        
        # Test 5: Obtener estado
        print("\n6. Test: Obtener estado...")
        status = traffic_light.get_status()
        print(f"   Estado: {status}")
        
        print("\n✅ Test del semáforo completado")
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        # No usar traceback para evitar problemas con _thread

def main():
    """Función principal"""
    print("🔧 Test de Debug del Sistema de Carrera")
    print("=" * 50)
    
    print("Elige el test:")
    print("1. Test completo del RaceController")
    print("2. Test solo del TrafficLightController")
    print("3. Ambos tests")
    print()
    
    try:
        choice = input("Ingresa tu elección (1, 2 o 3): ").strip()
        
        if choice == "1":
            test_race_controller()
        elif choice == "2":
            test_traffic_light_only()
        elif choice == "3":
            test_traffic_light_only()
            print("\n" + "="*50)
            test_race_controller()
        else:
            print("Opción no válida. Ejecutando test completo...")
            test_race_controller()
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrumpido")
    except Exception as e:
        print(f"❌ Error: {e}")
        # No usar traceback para evitar problemas con _thread

if __name__ == "__main__":
    main() 