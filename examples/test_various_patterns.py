"""
Ejemplo: Prueba de patrones varios
Demuestra todos los dibujos e iconos disponibles en various.py
"""

import time
from race_controller import RaceController
from patterns.various import *

def test_all_patterns():
    """Prueba todos los patrones disponibles"""
    print("=== PRUEBA: TODOS LOS PATRONES VARIOS ===")
    
    controller = RaceController(max_laps=5)
    
    # Lista de todos los patrones disponibles
    patterns = [
        # Cascos
        ("helmet", "Casco principal"),
        ("helmet_simple", "Casco simple"),
        ("helmet_empty", "Casco vacío"),
        
        # Símbolos
        ("heart", "Corazón"),
        ("star", "Estrella"),
        ("check", "Check (✓)"),
        ("x_mark", "X"),
        
        # Flechas
        ("arrow_up", "Flecha arriba"),
        ("arrow_down", "Flecha abajo"),
        ("arrow_right", "Flecha derecha"),
        ("arrow_left", "Flecha izquierda"),
        
        # Formas geométricas
        ("circle", "Círculo"),
        ("square", "Cuadrado"),
        ("triangle", "Triángulo"),
    ]
    
    print("🎨 Probando todos los patrones disponibles:")
    print("   Cada patrón se mostrará en ambos módulos")
    print()
    
    for i, (pattern_name, description) in enumerate(patterns, 1):
        print(f"{i:2d}. {description} ({pattern_name})")
        
        # Obtener el patrón
        pattern = get_various_pattern(pattern_name)
        
        # Mostrar en ambos módulos
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        
        # Esperar para ver el resultado
        time.sleep(2)
    
    controller.cleanup()
    print("\n✅ Prueba de todos los patrones completada!")

def test_pattern_functions():
    """Prueba las funciones de patrones"""
    print("\n=== PRUEBA: FUNCIONES DE PATRONES ===")
    
    print("🔧 Probando funciones:")
    
    # Probar función get_various_pattern
    print("- Función get_various_pattern:")
    heart = get_various_pattern('heart')
    star = get_various_pattern('star')
    arrow = get_various_pattern('arrow_up')
    
    print(f"  ✅ Corazón: {heart[:2]}...")
    print(f"  ✅ Estrella: {star[:2]}...")
    print(f"  ✅ Flecha arriba: {arrow[:2]}...")
    
    # Probar función get_available_patterns
    print("\n- Función get_available_patterns:")
    available = get_available_patterns()
    print(f"  ✅ Patrones disponibles: {len(available)}")
    print(f"  ✅ Lista: {', '.join(available)}")
    
    # Probar función get_helmet_pattern
    print("\n- Función get_helmet_pattern:")
    helmet_default = get_helmet_pattern('default')
    helmet_simple = get_helmet_pattern('simple')
    helmet_empty = get_helmet_pattern('empty')
    
    print(f"  ✅ Casco default: {helmet_default[:2]}...")
    print(f"  ✅ Casco simple: {helmet_simple[:2]}...")
    print(f"  ✅ Casco vacío: {helmet_empty[:2]}...")
    
    print("\n✅ Funciones de patrones funcionando correctamente!")

def test_pattern_categories():
    """Prueba patrones por categorías"""
    print("\n=== PRUEBA: PATRONES POR CATEGORÍAS ===")
    
    controller = RaceController(max_laps=5)
    
    # Probar cascos
    print("🏁 Probando cascos:")
    helmets = ['helmet', 'helmet_simple', 'helmet_empty']
    for helmet in helmets:
        pattern = get_various_pattern(helmet)
        print(f"  - {helmet}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(1.5)
    
    # Probar símbolos
    print("\n💝 Probando símbolos:")
    symbols = ['heart', 'star', 'check', 'x_mark']
    for symbol in symbols:
        pattern = get_various_pattern(symbol)
        print(f"  - {symbol}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(1.5)
    
    # Probar flechas
    print("\n➡️ Probando flechas:")
    arrows = ['arrow_up', 'arrow_down', 'arrow_right', 'arrow_left']
    for arrow in arrows:
        pattern = get_various_pattern(arrow)
        print(f"  - {arrow}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(1.5)
    
    # Probar formas geométricas
    print("\n🔷 Probando formas geométricas:")
    shapes = ['circle', 'square', 'triangle']
    for shape in shapes:
        pattern = get_various_pattern(shape)
        print(f"  - {shape}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(1.5)
    
    controller.cleanup()
    print("\n✅ Prueba por categorías completada!")

def main():
    """Función principal"""
    print("Prueba de Patrones Varios")
    print("=" * 40)
    
    # Probar funciones
    test_pattern_functions()
    
    # Probar por categorías
    test_pattern_categories()
    
    # Probar todos los patrones
    test_all_patterns()
    
    print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    print("\n💡 Patrones disponibles:")
    print("   🏁 Cascos: helmet, helmet_simple, helmet_empty")
    print("   💝 Símbolos: heart, star, check, x_mark")
    print("   ➡️ Flechas: arrow_up, arrow_down, arrow_right, arrow_left")
    print("   🔷 Formas: circle, square, triangle")

if __name__ == "__main__":
    main() 