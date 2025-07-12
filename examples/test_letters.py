"""
Ejemplo: Prueba de patrones de letras
Demuestra todos los patrones de letras mayúsculas A-Z disponibles
"""

import time
from race_controller import RaceController
from patterns.letters import *

def test_all_letters():
    """Prueba todas las letras disponibles"""
    print("=== PRUEBA: TODAS LAS LETRAS A-Z ===")
    
    controller = RaceController(max_laps=5)
    
    # Obtener todas las letras disponibles
    letters = get_available_letters()
    
    print(f"🎯 Probando {len(letters)} letras disponibles:")
    print("   Cada letra se mostrará en ambos módulos")
    print()
    
    for i, letter in enumerate(letters, 1):
        print(f"{i:2d}. Letra '{letter}'")
        
        # Obtener el patrón de la letra
        pattern = get_letter_pattern(letter)
        
        # Mostrar en ambos módulos
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        
        # Esperar para ver el resultado
        time.sleep(1.5)
    
    controller.cleanup()
    print("\n✅ Prueba de todas las letras completada!")

def test_letter_functions():
    """Prueba las funciones de letras"""
    print("\n=== PRUEBA: FUNCIONES DE LETRAS ===")
    
    print("🔧 Probando funciones:")
    
    # Probar función get_letter_pattern
    print("- Función get_letter_pattern:")
    a_pattern = get_letter_pattern('A')
    z_pattern = get_letter_pattern('Z')
    invalid_pattern = get_letter_pattern('@')
    
    print(f"  ✅ Letra A: {a_pattern[:2]}...")
    print(f"  ✅ Letra Z: {z_pattern[:2]}...")
    print(f"  ✅ Letra inválida @: {invalid_pattern[:2]}...")
    
    # Probar función get_word_pattern
    print("\n- Función get_word_pattern:")
    word_patterns = get_word_pattern('HELLO', 2)
    print(f"  ✅ Palabra 'HELLO' (máx 2): {len(word_patterns)} patrones")
    for i, pattern in enumerate(word_patterns):
        print(f"    Patrón {i+1}: {pattern[:2]}...")
    
    # Probar función get_available_letters
    print("\n- Función get_available_letters:")
    available = get_available_letters()
    print(f"  ✅ Letras disponibles: {len(available)}")
    print(f"  ✅ Primera letra: {available[0]}")
    print(f"  ✅ Última letra: {available[-1]}")
    
    # Probar función get_letter_info
    print("\n- Función get_letter_info:")
    info_a = get_letter_info('A')
    info_invalid = get_letter_info('@')
    
    print(f"  ✅ Info letra A: {info_a['letter']} - Existe: {info_a['exists']}")
    print(f"  ✅ Info letra @: {info_invalid['letter']} - Existe: {info_invalid['exists']}")
    
    print("\n✅ Funciones de letras funcionando correctamente!")

def test_letter_categories():
    """Prueba letras por categorías"""
    print("\n=== PRUEBA: LETRAS POR CATEGORÍAS ===")
    
    controller = RaceController(max_laps=5)
    
    # Probar vocales
    print("🔤 Probando vocales:")
    vowels = ['A', 'E', 'I', 'O', 'U']
    for vowel in vowels:
        pattern = get_letter_pattern(vowel)
        print(f"  - {vowel}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(1)
    
    # Probar consonantes comunes
    print("\n🔤 Probando consonantes comunes:")
    common_consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M']
    for consonant in common_consonants:
        pattern = get_letter_pattern(consonant)
        print(f"  - {consonant}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(0.8)
    
    # Probar consonantes restantes
    print("\n🔤 Probando consonantes restantes:")
    remaining_consonants = ['N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    for consonant in remaining_consonants:
        pattern = get_letter_pattern(consonant)
        print(f"  - {consonant}")
        for row in range(8):
            controller.display.write_register_all(row + 1, pattern[row])
        time.sleep(0.8)
    
    controller.cleanup()
    print("\n✅ Prueba por categorías completada!")

def test_word_display():
    """Prueba mostrar palabras en el display"""
    print("\n=== PRUEBA: MOSTRAR PALABRAS ===")
    
    controller = RaceController(max_laps=5)
    
    # Lista de palabras para probar
    test_words = [
        "HI",
        "OK", 
        "GO",
        "NO",
        "YES",
        "HELLO",  # Solo mostrará HE
        "WORLD",  # Solo mostrará WO
        "TEST",   # Solo mostrará TE
    ]
    
    print("📝 Probando palabras (máximo 2 letras):")
    
    for word in test_words:
        print(f"\n🏷️ Palabra: '{word}'")
        
        # Obtener patrones de la palabra
        patterns = get_word_pattern(word, 2)
        
        # Mostrar cada letra en un módulo diferente
        for i, pattern in enumerate(patterns):
            print(f"  Letra {i+1}: '{word[i]}' en módulo {i+1}")
            
            # Mostrar en el módulo correspondiente
            for row in range(8):
                controller.display.write_register_module(i, row + 1, pattern[row])
        
        time.sleep(2)
    
    controller.cleanup()
    print("\n✅ Prueba de palabras completada!")

def main():
    """Función principal"""
    print("Prueba de Patrones de Letras")
    print("=" * 40)
    
    # Probar funciones
    test_letter_functions()
    
    # Probar por categorías
    test_letter_categories()
    
    # Probar palabras
    test_word_display()
    
    # Probar todas las letras
    test_all_letters()
    
    print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    print("\n💡 Letras disponibles:")
    print("   🔤 26 letras mayúsculas A-Z")
    print("   📝 Soporte para palabras (máximo 2 letras)")
    print("   🎯 Patrones optimizados para display 8x8")
    print("   📁 Patrones centralizados en patterns/letters.py")

if __name__ == "__main__":
    main() 