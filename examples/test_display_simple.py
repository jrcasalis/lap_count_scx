"""
Test simple para verificar que el display funcione
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
        print(f"[MOCK SPI] Escribiendo: {data}")

# Mock de módulos de MicroPython
import builtins
builtins.Pin = MockPin
builtins.SPI = MockSPI

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
from max7219_dual_display_configurable import MAX7219DualDisplayConfigurable
from patterns.various import FULL_CIRCLE
import time

def test_display_simple():
    """Test simple para verificar que el display funcione"""
    print("🧪 TEST: Display simple")
    print("=" * 40)
    
    # Crear display
    print("1. Creando display...")
    display = MAX7219DualDisplayConfigurable()
    print("   ✅ Display creado")
    
    # Verificar patrón FULL_CIRCLE
    print("\n2. Verificando patrón FULL_CIRCLE...")
    print(f"   📋 Patrón: {FULL_CIRCLE}")
    print(f"   📏 Longitud: {len(FULL_CIRCLE)}")
    print("   ✅ Patrón válido")
    
    # Test mostrar patrón fijo
    print("\n3. Test mostrar patrón fijo...")
    for row in range(8):
        display.write_register_all(row + 1, FULL_CIRCLE[row])
    print("   ✅ Patrón mostrado fijo")
    
    # Test titileo
    print("\n4. Test titileo...")
    display.start_pattern_blink(FULL_CIRCLE, interval=0.5)
    print("   ✅ Titileo iniciado")
    
    # Simular algunas actualizaciones
    print("\n5. Simulando actualizaciones...")
    for i in range(10):
        display.update_pattern_blink()
        time.sleep(0.1)
        if i % 2 == 0:
            print(f"      Update {i+1}: ejecutado")
    
    print("\n✅ Test completado!")
    print("=" * 40)

if __name__ == "__main__":
    test_display_simple() 