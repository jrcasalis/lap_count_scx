"""
Prueba del efecto de alternancia de bandera a cuadros 2x2
Demuestra el patrón que alterna entre dos patrones complementarios
en lugar de encender y apagar completamente el display
"""

from race_controller import RaceController
import time

def test_checkered_flag_blink():
    """Prueba el efecto de alternancia de bandera a cuadros"""
    print("=== PRUEBA: BANDERA A CUADROS CON ALTERNANCIA ===")
    
    # Inicializar controlador
    race = RaceController(max_laps=15)
    
    print("Efecto de bandera a cuadros 2x2 con alternancia:")
    print("- Dos patrones complementarios de cuadros 2x2")
    print("- Alterna entre patrones en lugar de encender/apagar")
    print("- Intervalo de 0.5 segundos")
    print("- Display siempre activo durante la animación")
    print()
    
    # Mostrar los dos patrones estáticos primero
    print("Mostrando patrón 1 de bandera a cuadros...")
    pattern1 = [0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33]
    
    for row in range(8):
        race.display.write_register_all(row + 1, pattern1[row])
    
    print("Patrón 1 mostrado. Esperando 2 segundos...")
    time.sleep(2)
    
    print("Mostrando patrón 2 (complementario)...")
    pattern2 = [0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC]
    
    for row in range(8):
        race.display.write_register_all(row + 1, pattern2[row])
    
    print("Patrón 2 mostrado. Esperando 2 segundos...")
    time.sleep(2)
    
    # Ahora mostrar el efecto de alternancia
    print("Iniciando efecto de alternancia...")
    race.test_animation("checkered_flag")
    
    print("✅ Efecto de alternancia completado!")

def explain_blink_effect():
    """Explica cómo funciona el efecto de alternancia"""
    print("\n=== EXPLICACIÓN DEL EFECTO DE ALTERNANCIA ===")
    print("Patrón 1 de bandera a cuadros 2x2:")
    print("  Fila 1: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 2: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 3: 00110011 (0x33) - Cuadro negro")
    print("  Fila 4: 00110011 (0x33) - Cuadro negro")
    print("  Fila 5: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 6: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 7: 00110011 (0x33) - Cuadro negro")
    print("  Fila 8: 00110011 (0x33) - Cuadro negro")
    print()
    print("Patrón 2 (complementario):")
    print("  Fila 1: 00110011 (0x33) - Cuadro negro")
    print("  Fila 2: 00110011 (0x33) - Cuadro negro")
    print("  Fila 3: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 4: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 5: 00110011 (0x33) - Cuadro negro")
    print("  Fila 6: 00110011 (0x33) - Cuadro negro")
    print("  Fila 7: 11001100 (0xCC) - Cuadro blanco")
    print("  Fila 8: 11001100 (0xCC) - Cuadro blanco")
    print()
    print("Efecto de alternancia:")
    print("  - 0.5s: Patrón 1 (cuadros principales)")
    print("  - 0.5s: Patrón 2 (cuadros complementarios)")
    print("  - 0.5s: Patrón 1 (cuadros principales)")
    print("  - 0.5s: Patrón 2 (cuadros complementarios)")
    print("  - ... y así sucesivamente")
    print()
    print("¡Esto crea un efecto de bandera a cuadros que alterna patrones!")
    print("El display nunca se apaga completamente durante la animación.")

def test_custom_blink_duration():
    """Prueba con diferentes duraciones de alternancia"""
    print("\n=== PRUEBA CON DIFERENTES DURACIONES ===")
    
    race = RaceController(max_laps=15)
    
    durations = [0.2, 0.5, 1.0]
    
    for duration in durations:
        print(f"Probando alternancia con {duration}s de intervalo...")
        
        # Simular el efecto manualmente con dos patrones
        pattern1 = [0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33]
        pattern2 = [0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC]
        
        for i in range(6):  # 3 ciclos completos
            # Patrón 1
            for row in range(8):
                race.display.write_register_all(row + 1, pattern1[row])
            time.sleep(duration)
            
            # Patrón 2
            for row in range(8):
                race.display.write_register_all(row + 1, pattern2[row])
            time.sleep(duration)
        
        print(f"✅ Alternancia de {duration}s completada")
        time.sleep(1)
    
    # Limpiar display
    race.display.clear()

def main():
    """Función principal"""
    print("Bandera a Cuadros con Alternancia")
    print("=" * 40)
    
    # Explicar el efecto
    explain_blink_effect()
    
    # Probar el efecto
    test_checkered_flag_blink()
    
    # Probar diferentes duraciones
    test_custom_blink_duration()
    
    print("\n🎉 Todas las pruebas completadas exitosamente!")

if __name__ == "__main__":
    main() 