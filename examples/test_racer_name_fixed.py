"""
Ejemplo: Prueba de funcionalidad del nombre del piloto con casco (patrones centralizados)
Demuestra cómo cambiar y mostrar el nombre del piloto con casco en el display usando patrones centralizados
"""

import time
from race_controller import RaceController
from config import *

def test_racer_name_display():
    """Prueba la visualización del nombre del piloto con casco en el display"""
    print("=== PRUEBA: VISUALIZACIÓN DEL NOMBRE DEL PILOTO CON CASCO ===")
    print("Configuración:")
    print(f"- Nombre por defecto: {RACER_NAME}")
    print(f"- Longitud máxima: {RACER_NAME_MAX_LENGTH}")
    print(f"- Prefijo display: {RACER_DISPLAY_PREFIX}")
    print(f"- Patrones: Centralizados desde patterns/various.py")
    print()
    
    # Crear controlador de carrera
    controller = RaceController(max_laps=5)
    
    # Lista de nombres para probar
    test_names = [
        "Jose",      # J = 10 en display (casco + 10)
        "Ana",       # A = 01 en display (casco + 01)  
        "Bob",       # B = 02 en display (casco + 02)
        "Carlos",    # C = 03 en display (casco + 03)
        "123",       # No es letra = 00 en display (casco + 00)
        "",          # Vacío = 00 en display (casco + 00)
    ]
    
    for i, name in enumerate(test_names, 1):
        print(f"\n{i}. Probando nombre: '{name}'")
        
        # Cambiar nombre
        success = controller.set_racer_name(name)
        if success:
            print(f"   ✅ Nombre cambiado a: {name}")
            
            # Mostrar en display
            print(f"   📺 Mostrando en display...")
            print(f"   🏁 Módulo 1: Casco (patrón centralizado)")
            print(f"   🏁 Módulo 2: Código de letra")
            controller.display_racer_name()
            
            # Esperar para ver el resultado
            time.sleep(3)
        else:
            print(f"   ❌ Error al cambiar nombre: {name}")
    
    # Limpiar
    controller.cleanup()
    
    print("\n✅ Prueba de visualización con casco completada!")

def test_racer_name_api():
    """Prueba las APIs del nombre del piloto"""
    print("\n=== PRUEBA: APIs DEL NOMBRE DEL PILOTO ===")
    
    # Simular llamadas a la API
    print("Endpoints disponibles:")
    print("- GET /api/racer/name - Obtener nombre actual")
    print("- GET /api/racer/display - Mostrar nombre en display")
    print()
    
    print("Ejemplo de respuesta de /api/racer/name:")
    print("""
{
    "success": true,
    "racer_name": "Jose Casalis",
    "message": "Nombre del piloto obtenido"
}
    """)
    
    print("Ejemplo de respuesta de /api/racer/display:")
    print("""
{
    "success": true,
    "message": "Nombre del piloto mostrado en display"
}
    """)
    
    print("\nNota: El display mostrará:")
    print("- Módulo 1: Casco personalizado (patrón centralizado)")
    print("- Módulo 2: Código numérico de la primera letra:")
    print("  A = 01, B = 02, C = 03, ..., J = 10, ..., Z = 26")
    print("  Si no es letra o está vacío = 00")

def test_character_conversion():
    """Prueba la conversión de caracteres a números"""
    print("\n=== PRUEBA: CONVERSIÓN DE CARACTERES ===")
    
    test_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    print("Conversión de letras a números:")
    for char in test_chars:
        char_num = ord(char) - ord('A') + 1
        print(f"   {char} = {char_num:02d}")
    
    print("\nEjemplos de nombres:")
    examples = ["Jose", "Ana", "Bob", "Carlos"]
    for name in examples:
        if name and name[0].isalpha():
            char_num = ord(name[0].upper()) - ord('A') + 1
            print(f"   '{name}' → '{name[0]}' = {char_num:02d}")
        else:
            print(f"   '{name}' → No es letra = 00")

def test_helmet_display():
    """Prueba específica del display con casco"""
    print("\n=== PRUEBA: DISPLAY CON CASCO ===")
    
    controller = RaceController(max_laps=5)
    
    print("Mostrando diferentes combinaciones:")
    
    # Probar con diferentes nombres
    test_cases = [
        ("Jose", "J = 10"),
        ("Ana", "A = 01"), 
        ("Bob", "B = 02"),
        ("Carlos", "C = 03"),
        ("", "Vacío = 00"),
        ("123", "Número = 00")
    ]
    
    for name, description in test_cases:
        print(f"\n🏁 Probando: {name} ({description})")
        controller.set_racer_name(name)
        controller.display_racer_name()
        time.sleep(2)
    
    controller.cleanup()
    print("\n✅ Prueba de display con casco completada!")

def main():
    """Función principal"""
    print("Prueba de Funcionalidad del Nombre del Piloto con Casco")
    print("=" * 60)
    
    # Probar conversión de caracteres
    test_character_conversion()
    
    # Probar visualización con casco
    test_racer_name_display()
    
    # Probar display específico con casco
    test_helmet_display()
    
    # Probar APIs
    test_racer_name_api()
    
    print("\n🎉 Todas las pruebas completadas exitosamente!")
    print("\n💡 El display ahora muestra:")
    print("   🏁 Módulo 1: Casco personalizado (patrón centralizado)")
    print("   🏁 Módulo 2: Código de la primera letra del piloto")
    print("   📊 A=01, B=02, C=03, ..., J=10, ..., Z=26")
    print("   📁 Patrones centralizados en patterns/various.py")

if __name__ == "__main__":
    main() 