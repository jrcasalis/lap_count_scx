"""
Ejemplo: Prueba del display con casco (patrones centralizados)
Demuestra cómo funciona el nuevo sistema que muestra un casco + código de letra usando patrones centralizados
"""

import time
from race_controller import RaceController

def test_helmet_display():
    """Prueba el display con casco y código de letra"""
    print("=== PRUEBA: DISPLAY CON CASCO ===")
    print("Configuración:")
    print("- Módulo 1: Casco personalizado (patrón centralizado)")
    print("- Módulo 2: Código de la primera letra del piloto")
    print("- Patrones: Centralizados desde patterns/various.py")
    print()
    
    # Crear controlador
    controller = RaceController(max_laps=5)
    
    # Lista de nombres para probar
    test_names = [
        ("Jose", "J = 10"),
        ("Ana", "A = 01"), 
        ("Bob", "B = 02"),
        ("Carlos", "C = 03"),
        ("David", "D = 04"),
        ("Elena", "E = 05"),
        ("", "Vacío = 00"),
        ("123", "Número = 00")
    ]
    
    print("Probando diferentes nombres:")
    print("🏁 Módulo 1: Casco (patrón centralizado)")
    print("🏁 Módulo 2: Código de letra")
    print()
    
    for i, (name, description) in enumerate(test_names, 1):
        print(f"{i}. Probando: '{name}' ({description})")
        
        # Cambiar nombre
        controller.set_racer_name(name)
        
        # Mostrar en display
        controller.display_racer_name()
        
        # Esperar para ver el resultado
        time.sleep(2)
    
    # Limpiar
    controller.cleanup()
    
    print("\n✅ Prueba completada!")
    print("\n💡 El display muestra:")
    print("   🏁 Módulo 1: Casco personalizado (patrón centralizado)")
    print("   🏁 Módulo 2: Código de la primera letra")
    print("   📊 A=01, B=02, C=03, ..., J=10, ..., Z=26")
    print("   📁 Patrones centralizados en patterns/various.py")

def main():
    """Función principal"""
    print("Prueba del Display con Casco")
    print("=" * 40)
    
    test_helmet_display()
    
    print("\n🎉 ¡Prueba completada exitosamente!")

if __name__ == "__main__":
    main() 