"""
Prueba específica del patrón de bandera a cuadros 2x2
Demuestra el nuevo patrón clásico con cuadros de 2x2 píxeles
"""

from race_controller import RaceController
import time

def test_checkered_flag_2x2():
    """Prueba el nuevo patrón de bandera a cuadros 2x2"""
    print("=== PRUEBA: BANDERA A CUADROS 2x2 ===")
    
    # Inicializar controlador
    race = RaceController(max_laps=15)
    
    print("Patrón de bandera a cuadros 2x2:")
    print("Cada cuadro es de 2x2 LEDs (4 LEDs por cuadro)")
    print("Patrones:")
    print("  1. Cuadros 2x2 básicos")
    print("  2. Cuadros 2x2 invertidos") 
    print("  3. Cuadros 2x2 alternados horizontalmente")
    print("  4. Cuadros 2x2 alternados verticalmente")
    print()
    
    # Mostrar cada patrón individualmente para explicar
    patterns = [
        ("Cuadros 2x2 básicos", [0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33]),
        ("Cuadros 2x2 invertidos", [0x33, 0x33, 0xCC, 0xCC, 0x33, 0x33, 0xCC, 0xCC]),
        ("Cuadros 2x2 alternados horizontalmente", [0xCC, 0x33, 0xCC, 0x33, 0xCC, 0x33, 0xCC, 0x33]),
        ("Cuadros 2x2 alternados verticalmente", [0x33, 0xCC, 0x33, 0xCC, 0x33, 0xCC, 0x33, 0xCC])
    ]
    
    for i, (name, pattern) in enumerate(patterns, 1):
        print(f"Patrón {i}: {name}")
        print(f"  Bytes: {[hex(x) for x in pattern]}")
        print(f"  Binario:")
        for row in pattern:
            binary = format(row, '08b')
            print(f"    {binary}")
        print()
        
        # Mostrar patrón en el display
        print(f"Mostrando patrón {i}...")
        for row in range(8):
            race.display.write_register_all(row + 1, pattern[row])
        time.sleep(2)
    
    # Ahora mostrar la animación completa
    print("Mostrando animación completa de bandera a cuadros 2x2...")
    race.test_animation("checkered_flag")
    
    print("✅ Prueba de bandera a cuadros 2x2 completada!")

def explain_pattern():
    """Explica cómo funciona el patrón 2x2"""
    print("\n=== EXPLICACIÓN DEL PATRÓN 2x2 ===")
    print("En un display de 8x8 LEDs:")
    print("  - Cada fila tiene 8 LEDs")
    print("  - Cada cuadro 2x2 ocupa 4 LEDs")
    print("  - 0xCC = 11001100 (2 LEDs encendidos, 2 apagados)")
    print("  - 0x33 = 00110011 (2 LEDs apagados, 2 encendidos)")
    print()
    print("Patrón básico (0xCC, 0xCC, 0x33, 0x33):")
    print("  Fila 1: 11001100 (cuadro blanco)")
    print("  Fila 2: 11001100 (cuadro blanco)")
    print("  Fila 3: 00110011 (cuadro negro)")
    print("  Fila 4: 00110011 (cuadro negro)")
    print("  ... y así sucesivamente")
    print()
    print("Esto crea cuadros perfectos de 2x2 LEDs!")

def main():
    """Función principal"""
    print("Bandera a Cuadros 2x2 - Patrón Clásico")
    print("=" * 50)
    
    # Explicar el patrón
    explain_pattern()
    
    # Probar el patrón
    test_checkered_flag_2x2()
    
    print("\n🎉 Prueba completada exitosamente!")

if __name__ == "__main__":
    main() 