"""
Test para verificar que los titileos funcionen correctamente
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from race_controller import RaceController
import time

def test_blinking_functionality():
    """Test para verificar que los titileos funcionen correctamente"""
    print("🧪 TEST: Verificando titileos del display y semáforo")
    print("=" * 60)
    
    # Inicializar controlador
    print("1. Inicializando RaceController...")
    RaceController.__init__(max_laps=15, num_racers=2, racer_names=["Piloto 1", "Piloto 2"])
    
    # Verificar estado inicial
    params = RaceController.get_race_params()
    print(f"   Estado inicial: {params['race_state']}")
    print(f"   Titileo habilitado: {RaceController.get_stopped_blink_status()}")
    
    # Test 1: Verificar titileo en estado STOPPED
    print("\n2. Test 1: Titileo en estado STOPPED")
    print("   - Debería mostrar patrón FULL_CIRCLE titilando")
    print("   - Ejecutando update() por 5 segundos...")
    
    start_time = time.time()
    while time.time() - start_time < 5:
        RaceController.update()
        time.sleep(0.1)
    
    # Test 2: Iniciar previa
    print("\n3. Test 2: Iniciando previa")
    print("   - Debería mostrar max_laps (15) en display")
    print("   - Semáforo debería titilar todas las luces")
    
    success = RaceController.start_race_previous()
    print(f"   Resultado: {'✅ Éxito' if success else '❌ Fallo'}")
    
    if success:
        print("   - Ejecutando update() por 5 segundos...")
        start_time = time.time()
        while time.time() - start_time < 5:
            RaceController.update()
            time.sleep(0.1)
    
    # Test 3: Detener previa
    print("\n4. Test 3: Deteniendo previa")
    success = RaceController.stop_race_previous()
    print(f"   Resultado: {'✅ Éxito' if success else '❌ Fallo'}")
    
    # Test 4: Verificar que vuelve al titileo STOPPED
    print("\n5. Test 4: Verificando vuelta a titileo STOPPED")
    print("   - Debería volver a mostrar patrón FULL_CIRCLE titilando")
    print("   - Ejecutando update() por 3 segundos...")
    
    start_time = time.time()
    while time.time() - start_time < 3:
        RaceController.update()
        time.sleep(0.1)
    
    print("\n✅ Test completado!")
    print("=" * 60)

if __name__ == "__main__":
    test_blinking_functionality() 