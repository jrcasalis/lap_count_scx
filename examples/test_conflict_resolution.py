"""
Test para verificar la resolución del conflicto previa -> carrera
Verifica que cuando se inicia una carrera durante una previa activa:
1. La previa se termina automáticamente
2. La carrera se inicia correctamente
3. No hay errores en el proceso
"""

import time
import requests
import json

def test_conflict_resolution():
    """Test para verificar la resolución correcta del conflicto"""
    
    print("🧪 Test: Resolución de Conflicto Previa -> Carrera")
    print("=" * 60)
    
    # URL base del servidor
    base_url = "http://192.168.1.100:8080"
    
    try:
        # Paso 1: Verificar estado inicial
        print("1️⃣ Verificando estado inicial...")
        response = requests.get(f"{base_url}/api/traffic-light/status", timeout=5)
        initial_status = response.json()
        print(f"   Estado inicial: {initial_status['traffic_light_status']['state']}")
        
        # Paso 2: Iniciar previa
        print("2️⃣ Iniciando previa...")
        response = requests.get(f"{base_url}/api/traffic-light/previous", timeout=5)
        previous_result = response.json()
        
        if not previous_result['success']:
            print(f"   ❌ Error iniciando previa: {previous_result['message']}")
            return False
        
        print("   ✅ Previa iniciada correctamente")
        print(f"   Estado: {previous_result['traffic_light_status']['state']}")
        
        # Esperar un momento para que la previa esté activa
        time.sleep(1)
        
        # Paso 3: Verificar que la previa está activa
        print("3️⃣ Verificando que previa está activa...")
        response = requests.get(f"{base_url}/api/traffic-light/status", timeout=5)
        status_during_previous = response.json()
        
        if status_during_previous['traffic_light_status']['state'] != 'blinking':
            print(f"   ⚠️ Estado inesperado durante previa: {status_during_previous['traffic_light_status']['state']}")
            return False
        
        print("   ✅ Previa está activa (blinking)")
        
        # Paso 4: Iniciar carrera durante previa (CONFLICTO)
        print("4️⃣ Iniciando carrera durante previa (conflicto)...")
        response = requests.get(f"{base_url}/api/traffic-light/start", timeout=5)
        race_result = response.json()
        
        if not race_result['success']:
            print(f"   ❌ Error iniciando carrera: {race_result['message']}")
            return False
        
        print("   ✅ Carrera iniciada correctamente")
        print(f"   Estado del semáforo: {race_result['traffic_light_status']['state']}")
        print(f"   Estado de la carrera: {race_result['race_status']['is_race_started']}")
        
        # Paso 5: Verificar que la previa se terminó automáticamente
        print("5️⃣ Verificando que previa se terminó automáticamente...")
        response = requests.get(f"{base_url}/api/traffic-light/status", timeout=5)
        status_after_race = response.json()
        
        if status_after_race['traffic_light_status']['state'] == 'blinking':
            print("   ❌ Previa sigue activa después de iniciar carrera")
            return False
        
        print("   ✅ Previa se terminó automáticamente")
        
        # Paso 6: Esperar a que termine la secuencia de largada
        print("6️⃣ Esperando fin de secuencia de largada...")
        time.sleep(5)
        
        # Paso 7: Verificar estado final
        print("7️⃣ Verificando estado final...")
        response = requests.get(f"{base_url}/api/traffic-light/status", timeout=5)
        final_status = response.json()
        
        print(f"   Estado final del semáforo: {final_status['traffic_light_status']['state']}")
        print(f"   Estado final de la carrera: {final_status['race_status']['is_race_started']}")
        
        # Paso 8: Parar la carrera para limpiar
        print("8️⃣ Parando carrera para limpiar...")
        response = requests.get(f"{base_url}/api/traffic-light/stop", timeout=5)
        stop_result = response.json()
        
        if stop_result['success']:
            print("   ✅ Carrera parada correctamente")
        else:
            print(f"   ⚠️ Error parando carrera: {stop_result['message']}")
        
        print("\n" + "=" * 60)
        print("✅ Test de resolución de conflicto completado exitosamente")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_multiple_conflicts():
    """Test para verificar múltiples conflictos consecutivos"""
    
    print("\n🧪 Test: Múltiples Conflictos Consecutivos")
    print("=" * 60)
    
    base_url = "http://192.168.1.100:8080"
    
    try:
        for i in range(3):
            print(f"\n--- Iteración {i+1}/3 ---")
            
            # Iniciar previa
            print(f"   Iniciando previa {i+1}...")
            response = requests.get(f"{base_url}/api/traffic-light/previous", timeout=5)
            if not response.json()['success']:
                print(f"   ❌ Error en previa {i+1}")
                return False
            
            time.sleep(0.5)
            
            # Iniciar carrera durante previa
            print(f"   Iniciando carrera {i+1} durante previa...")
            response = requests.get(f"{base_url}/api/traffic-light/start", timeout=5)
            if not response.json()['success']:
                print(f"   ❌ Error en carrera {i+1}")
                return False
            
            time.sleep(2)
            
            # Parar carrera
            print(f"   Parando carrera {i+1}...")
            requests.get(f"{base_url}/api/traffic-light/stop", timeout=5)
            
            time.sleep(1)
        
        print("\n✅ Test de múltiples conflictos completado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de múltiples conflictos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando tests de resolución de conflictos")
    print("=" * 60)
    
    # Test 1: Resolución de conflicto básico
    success1 = test_conflict_resolution()
    
    # Test 2: Múltiples conflictos consecutivos
    success2 = test_multiple_conflicts()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✅ Todos los tests de resolución de conflictos pasaron")
        print("   El sistema maneja correctamente el escenario previa -> carrera")
    else:
        print("❌ Algunos tests fallaron")
        print("   Revisar logs para identificar el problema específico") 