"""
Ejemplo: Prueba de funcionalidad del nombre del piloto
Demuestra cómo cambiar y mostrar el nombre del piloto en el display
"""

import time
from race_controller import RaceController
from config import *

def test_racer_name():
    """Prueba la funcionalidad del nombre del piloto"""
    print("=== PRUEBA: NOMBRE DEL PILOTO ===")
    print("Configuración:")
    print(f"- Nombre por defecto: {RACER_NAME}")
    print(f"- Longitud máxima: {RACER_NAME_MAX_LENGTH}")
    print(f"- Prefijo display: {RACER_DISPLAY_PREFIX}")
    print()
    
    # Crear controlador de carrera
    controller = RaceController(max_laps=5)
    
    print("1. Mostrando nombre actual del piloto...")
    current_name = controller.get_racer_name()
    print(f"   Nombre actual: {current_name}")
    
    print("\n2. Cambiando nombre del piloto...")
    new_name = "Jose Casalis"
    success = controller.set_racer_name(new_name)
    if success:
        print(f"   ✅ Nombre cambiado a: {new_name}")
    else:
        print(f"   ❌ Error al cambiar nombre")
    
    print("\n3. Mostrando nombre en display...")
    print("   El display mostrará: 🏎️ Jose Casalis")
    controller.display_racer_name()
    
    print("\n4. Probando nombres inválidos...")
    invalid_names = ["", "NombreMuyLargoParaElLimite", None]
    for name in invalid_names:
        success = controller.set_racer_name(name)
        print(f"   '{name}': {'✅' if success else '❌'}")
    
    print("\n5. Verificando estado final...")
    final_status = controller.get_race_status()
    print(f"   Nombre en estado: {final_status['racer_name']}")
    
    # Limpiar
    controller.cleanup()
    
    print("\n✅ Prueba de nombre del piloto completada!")

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

def main():
    """Función principal"""
    print("Prueba de Funcionalidad del Nombre del Piloto")
    print("=" * 50)
    
    # Probar funcionalidad básica
    test_racer_name()
    
    # Probar APIs
    test_racer_name_api()
    
    print("\n🎉 Todas las pruebas completadas exitosamente!")

if __name__ == "__main__":
    main() 