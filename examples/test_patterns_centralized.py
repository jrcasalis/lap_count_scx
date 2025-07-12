"""
Ejemplo: Prueba de patrones centralizados
Demuestra cómo usar la nueva estructura de patrones organizados
"""

import time
from race_controller import RaceController
from patterns.index import *
from patterns.index import get_pattern

def test_patterns_import():
    """Prueba la importación de patrones centralizados"""
    print("=== PRUEBA: IMPORTACIÓN DE PATRONES ===")
    
    print("✅ Patrones disponibles:")
    print(f"- Dígitos: {len(DIGITS)} patrones (0-9)")
    print(f"- Varios: 13 patrones (cascos, símbolos, flechas, formas)")
    print(f"- Animaciones: 4 tipos (checkered, pulse, wave, spinning)")
    
    # Probar acceso a patrones
    print("\n📊 Probando acceso a patrones:")
    print(f"- Dígito '5': {get_digit_pattern('5')[:2]}...")  # Solo primeros 2 elementos
    print(f"- Casco default: {HELMET[:2]}...")
    print(f"- Animación checkered: {len(CHECKERED_FLAG_PATTERNS)} variaciones")
    
    print("\n✅ Importación de patrones exitosa!")

def test_helmet_display():
    """Prueba el display con casco usando patrones centralizados"""
    print("\n=== PRUEBA: DISPLAY CON CASCO (PATRONES CENTRALIZADOS) ===")
    
    controller = RaceController(max_laps=5)
    
    # Probar diferentes nombres
    test_names = [
        ("Jose", "J = 10"),
        ("Ana", "A = 01"), 
        ("Bob", "B = 02"),
        ("Carlos", "C = 03"),
        ("David", "D = 04"),
        ("Elena", "E = 05"),
    ]
    
    print("🏁 Probando display con casco centralizado:")
    print("   Módulo 1: Casco (patrón centralizado)")
    print("   Módulo 2: Código de letra")
    print("   📁 Patrones desde patterns/various.py")
    print()
    
    for i, (name, description) in enumerate(test_names, 1):
        print(f"{i}. Probando: '{name}' ({description})")
        
        controller.set_racer_name(name)
        controller.display_racer_name()
        time.sleep(2)
    
    controller.cleanup()
    print("\n✅ Prueba de display con patrones centralizados completada!")

def test_animations_centralized():
    """Prueba las animaciones usando patrones centralizados"""
    print("\n=== PRUEBA: ANIMACIONES CON PATRONES CENTRALIZADOS ===")
    
    controller = RaceController(max_laps=5)
    
    # Lista de animaciones disponibles
    animations = [
        ("checkered_flag", "Bandera a cuadros"),
        ("pulse_flag", "Bandera pulsante"),
        ("wave_flag", "Bandera ondulante"),
        ("spinning_flag", "Bandera giratoria"),
    ]
    
    print("🎬 Probando animaciones con patrones centralizados:")
    
    for i, (anim_type, description) in enumerate(animations, 1):
        print(f"\n{i}. {description} ({anim_type})")
        controller.test_animation(anim_type)
        time.sleep(1)
    
    controller.cleanup()
    print("\n✅ Prueba de animaciones centralizadas completada!")

def test_pattern_functions():
    """Prueba las funciones de patrones"""
    print("\n=== PRUEBA: FUNCIONES DE PATRONES ===")
    
    print("🔧 Probando funciones de patrones:")
    
    # Probar función centralizada
    print("- Función get_pattern:")
    digit_pattern = get_pattern('digit', digit='7')
    helmet_pattern = get_pattern('helmet', helmet_type='simple')
    animation_patterns = get_pattern('animation', animation_type='pulse')
    
    print(f"  ✅ Dígito 7: {digit_pattern[:2]}...")
    print(f"  ✅ Casco simple: {helmet_pattern[:2]}...")
    print(f"  ✅ Animación pulse: {len(animation_patterns)} patrones")
    
    # Probar funciones específicas
    print("\n- Funciones específicas:")
    left, right = get_two_digits_pattern(42)
    print(f"  ✅ Dos dígitos 42: {left[:2]}... | {right[:2]}...")
    
    helmet = get_helmet_pattern('default')
    print(f"  ✅ Casco default: {helmet[:2]}...")
    
    checkered = get_checkered_flag_pattern(1)
    print(f"  ✅ Bandera variación 1: {checkered[:2]}...")
    
    print("\n✅ Funciones de patrones funcionando correctamente!")

def main():
    """Función principal"""
    print("Prueba de Patrones Centralizados")
    print("=" * 50)
    
    # Probar importación
    test_patterns_import()
    
    # Probar funciones de patrones
    test_pattern_functions()
    
    # Probar display con casco
    test_helmet_display()
    
    # Probar animaciones
    test_animations_centralized()
    
    print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    print("\n💡 Beneficios de la centralización:")
    print("   📁 Patrones organizados en carpetas")
    print("   🔧 Fácil mantenimiento y modificación")
    print("   📦 Reutilización en múltiples controladores")
    print("   🎨 Separación clara de responsabilidades")
    print("   🎨 13 patrones varios disponibles en patterns/various.py")

if __name__ == "__main__":
    main() 