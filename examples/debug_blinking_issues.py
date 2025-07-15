"""
Debug de problemas de titileo - Test paso a paso
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock de MicroPython para testing
class MockPin:
    def __init__(self, pin_id, mode=None, pull=None):
        self.pin_id = pin_id
        self.mode = mode
        self.pull = pull
        self.value_state = 1
    
    def value(self, val=None):
        if val is not None:
            self.value_state = val
        return self.value_state

class MockPWM:
    def __init__(self, pin, freq=None):
        self.pin = pin
        self.freq = freq
        self.duty_u16_val = 0
    
    def duty_u16(self, value=None):
        if value is not None:
            self.duty_u16_val = value
        return self.duty_u16_val

class MockSPI:
    def __init__(self, id, baudrate=None, polarity=None, phase=None, sck=None, mosi=None):
        self.id = id
        self.baudrate = baudrate
        self.polarity = polarity
        self.phase = phase
        self.sck = sck
        self.mosi = mosi
        self.written_data = []
    
    def write(self, data):
        self.written_data.append(data)

# Mock de módulos de MicroPython
import builtins
builtins.Pin = MockPin
builtins.PWM = MockPWM
builtins.SPI = MockSPI

# Mock de _thread para evitar errores
class MockThread:
    @staticmethod
    def start_new_thread(func, args):
        print(f"[MOCK] Hilo iniciado: {func.__name__}")
        return True

builtins._thread = MockThread

# Mock de time para testing
import time
original_time = time.time
original_sleep = time.sleep

def mock_time():
    if not hasattr(mock_time, 'counter'):
        mock_time.counter = 0
    mock_time.counter += 0.1
    return mock_time.counter

def mock_sleep(seconds):
    print(f"[MOCK] Sleep: {seconds}s")

time.time = mock_time
time.sleep = mock_sleep

# Ahora importar los módulos
from race_controller import RaceController
from patterns.various import FULL_CIRCLE
import time

def test_step_by_step():
    """Test paso a paso para identificar problemas"""
    print("🔍 DEBUG: Problemas de titileo - Test paso a paso")
    print("=" * 70)
    
    # Paso 1: Inicializar controlador
    print("\n1️⃣ PASO 1: Inicializando RaceController")
    try:
        RaceController.__init__(max_laps=15, num_racers=2, racer_names=["Piloto 1", "Piloto 2"])
        print("   ✅ RaceController inicializado")
        
        # Verificar estado inicial
        params = RaceController.get_race_params()
        print(f"   📊 Estado: {params['race_state']}")
        print(f"   💡 Titileo habilitado: {RaceController.get_stopped_blink_status()}")
        
        # Verificar que display y traffic_light existen
        print(f"   📺 Display existe: {RaceController.display is not None}")
        print(f"   🚦 Traffic light existe: {RaceController.traffic_light is not None}")
        
    except Exception as e:
        print(f"   ❌ Error inicializando: {e}")
        return
    
    # Paso 2: Verificar patrón FULL_CIRCLE
    print("\n2️⃣ PASO 2: Verificando patrón FULL_CIRCLE")
    try:
        print(f"   📋 Patrón FULL_CIRCLE: {FULL_CIRCLE}")
        print(f"   📏 Longitud: {len(FULL_CIRCLE)} filas")
        print("   ✅ Patrón válido")
    except Exception as e:
        print(f"   ❌ Error con patrón: {e}")
        return
    
    # Paso 3: Test titileo en estado STOPPED
    print("\n3️⃣ PASO 3: Test titileo en estado STOPPED")
    try:
        print("   🔄 Ejecutando update() 10 veces...")
        for i in range(10):
            RaceController.update()
            time.sleep(0.1)
            if i % 2 == 0:
                print(f"      Update {i+1}: ejecutado")
        
        # Verificar si el display está titilando
        if RaceController.display:
            is_blinking = RaceController.display.is_blinking()
            print(f"   💡 Display titilando: {is_blinking}")
        else:
            print("   ❌ Display es None")
            
    except Exception as e:
        print(f"   ❌ Error en titileo STOPPED: {e}")
    
    # Paso 4: Test previa
    print("\n4️⃣ PASO 4: Test previa (start_race_previous)")
    try:
        print("   🚦 Iniciando previa...")
        success = RaceController.start_race_previous()
        print(f"   📊 Resultado: {'✅ Éxito' if success else '❌ Fallo'}")
        
        if success:
            print("   🔄 Ejecutando update() 10 veces...")
            for i in range(10):
                RaceController.update()
                time.sleep(0.1)
                if i % 2 == 0:
                    print(f"      Update {i+1}: ejecutado")
            
            # Verificar estado del semáforo
            if RaceController.traffic_light:
                status = RaceController.traffic_light.get_status()
                print(f"   🚦 Estado semáforo: {status}")
            else:
                print("   ❌ Traffic light es None")
                
    except Exception as e:
        print(f"   ❌ Error en previa: {e}")
    
    # Paso 5: Detener previa
    print("\n5️⃣ PASO 5: Deteniendo previa")
    try:
        success = RaceController.stop_race_previous()
        print(f"   📊 Resultado: {'✅ Éxito' if success else '❌ Fallo'}")
    except Exception as e:
        print(f"   ❌ Error deteniendo previa: {e}")
    
    print("\n✅ Debug completado!")
    print("=" * 70)

if __name__ == "__main__":
    test_step_by_step() 