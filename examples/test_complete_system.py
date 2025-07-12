"""
Prueba del Sistema Completo de Contador de Vueltas
Incluye display configurable, animaciones y lógica de carrera
"""

from race_controller import RaceController
import time

def main():
    print("=== PRUEBA DEL SISTEMA COMPLETO ===")
    print("Contador de vueltas con display configurable")
    print("=" * 50)
    
    # Inicializar controlador de carrera
    race = RaceController(max_laps=15)
    
    print("1. Estado inicial")
    status = race.get_race_status()
    print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
    print(f"   Completada: {status['is_completed']}")
    
    # Prueba 1: Incrementar vueltas
    print("\n2. Incrementando vueltas...")
    for i in range(5):
        race.increment_lap()
        status = race.get_race_status()
        print(f"   Vuelta {status['current_laps']}/{status['max_laps']}")
        time.sleep(0.5)
    
    # Prueba 2: Control de LED
    print("\n3. Probando control de LED...")
    print("   Encendiendo LED...")
    race.turn_on_led()
    time.sleep(1)
    
    print("   Apagando LED...")
    race.turn_off_led()
    time.sleep(1)
    
    print("   Alternando LED...")
    race.toggle_led()
    time.sleep(1)
    
    # Prueba 3: Configuración del display
    print("\n4. Probando configuración del display...")
    print("   Cambiando brillo...")
    for brightness in [5, 10, 15]:
        race.set_brightness(brightness)
        print(f"      Brillo: {brightness}")
        time.sleep(1)
    
    # Prueba 4: Completar carrera
    print("\n5. Completando carrera...")
    for i in range(10):
        race.increment_lap()
        status = race.get_race_status()
        print(f"   Vuelta {status['current_laps']}/{status['max_laps']}")
        time.sleep(0.3)
    
    # La carrera debería completarse y mostrar animación
    print("\n6. Carrera completada - mostrando animación de bandera")
    time.sleep(2)
    
    # Prueba 5: Reiniciar
    print("\n7. Reiniciando carrera...")
    race.reset_race()
    status = race.get_race_status()
    print(f"   Vueltas: {status['current_laps']}/{status['max_laps']}")
    
    print("\n=== PRUEBA COMPLETADA ===")
    print("Sistema funcionando correctamente!")

if __name__ == "__main__":
    main() 