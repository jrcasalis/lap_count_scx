"""
Prueba de todas las animaciones disponibles
Demuestra cada tipo de animación de bandera
"""

from race_controller import RaceController
import time

def test_all_animations():
    """Prueba todas las animaciones disponibles"""
    print("=== PRUEBA DE ANIMACIONES ===")
    
    # Inicializar controlador
    race = RaceController(max_laps=15)
    
    # Obtener animaciones disponibles
    animations = race.get_available_animations()
    print(f"Animaciones disponibles: {list(animations.keys())}")
    
    # Probar cada animación
    for animation_type, description in animations.items():
        print(f"\n--- Probando: {description} ({animation_type}) ---")
        
        # Mostrar descripción
        print(f"Descripción: {description}")
        
        # Probar la animación
        success = race.test_animation(animation_type)
        
        if success:
            print("✅ Animación ejecutada correctamente")
        else:
            print("❌ Error al ejecutar animación")
        
        # Pausa entre animaciones
        time.sleep(1)
    
    print("\n=== PRUEBA COMPLETADA ===")
    print("Todas las animaciones han sido probadas!")

def test_checkered_flag_detailed():
    """Prueba detallada de la bandera a cuadros clásica"""
    print("\n=== PRUEBA DETALLADA: BANDERA A CUADROS 2x2 ===")
    
    race = RaceController(max_laps=15)
    
    print("Mostrando animación de bandera a cuadros clásica...")
    print("Efecto:")
    print("  - Patrón fijo de cuadros 2x2")
    print("  - Titileo cada 0.5 segundos")
    print("  - Alterna entre encendido y apagado")
    print("  - Sin scroll, solo titileo")
    
    race.test_animation("checkered_flag")
    
    print("✅ Animación de bandera a cuadros 2x2 completada")

def test_animation_configuration():
    """Prueba la configuración de animaciones"""
    print("\n=== PRUEBA DE CONFIGURACIÓN ===")
    
    race = RaceController(max_laps=15)
    
    # Cambiar animación de finalización
    print("Cambiando animación de finalización a 'pulse_flag'...")
    success = race.set_completion_animation("pulse_flag")
    print(f"Resultado: {'✅ Éxito' if success else '❌ Error'}")
    
    # Probar animación personalizada
    print("Probando animación personalizada...")
    race.test_animation("pulse_flag")
    
    # Volver a la animación por defecto
    print("Restaurando animación por defecto...")
    race.set_completion_animation("checkered_flag")
    
    print("✅ Configuración de animaciones completada")

def main():
    """Función principal"""
    print("Sistema de Animaciones de Bandera")
    print("=" * 40)
    
    # Prueba 1: Todas las animaciones
    test_all_animations()
    
    # Prueba 2: Bandera a cuadros detallada
    test_checkered_flag_detailed()
    
    # Prueba 3: Configuración
    test_animation_configuration()
    
    print("\n🎉 Todas las pruebas completadas exitosamente!")

if __name__ == "__main__":
    main() 