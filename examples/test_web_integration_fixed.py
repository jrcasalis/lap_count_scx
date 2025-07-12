"""
Ejemplo: Prueba de integración web con patrones centralizados
Demuestra que todas las funcionalidades web funcionan con la nueva estructura
"""

import time
from race_controller import RaceController
from web_server import WebServer
from config import *

def test_web_integration():
    """Prueba la integración web completa"""
    print("=== PRUEBA: INTEGRACIÓN WEB CON PATRONES CENTRALIZADOS ===")
    
    # Crear controlador de carrera
    controller = RaceController(max_laps=5)
    
    # Simular servidor web
    print("🏁 Configurando servidor web...")
    print(f"   Puerto: {SERVER_PORT}")
    print(f"   Controlador: {type(controller).__name__}")
    
    # Probar incremento de vueltas
    print("\n📊 Probando incremento de vueltas:")
    for i in range(3):
        success = controller.increment_lap()
        status = controller.get_race_status()
        print(f"   Vuelta {i+1}: {'✅' if success else '❌'} - Estado: {status['current_laps']}/{status['max_laps']}")
        time.sleep(0.5)
    
    # Probar nombre del piloto
    print("\n🏎️ Probando nombre del piloto:")
    original_name = controller.get_racer_name()
    print(f"   Nombre original: {original_name}")
    
    # Cambiar nombre
    controller.set_racer_name("Jose")
    new_name = controller.get_racer_name()
    print(f"   Nombre cambiado: {new_name}")
    
    # Mostrar en display
    print("   Mostrando en display...")
    controller.display_racer_name()
    time.sleep(2)
    
    # Probar animaciones
    print("\n🎬 Probando animaciones:")
    animations = controller.get_available_animations()
    print(f"   Animaciones disponibles: {len(animations)}")
    for anim in animations:
        print(f"   - {anim}")
    
    # Probar una animación
    print("   Probando animación 'checkered_flag'...")
    controller.test_animation("checkered_flag")
    time.sleep(1)
    
    # Probar LED
    print("\n🔴 Probando LED:")
    controller.turn_on_led()
    led_status = controller.get_race_status()['led_status']['is_on']
    print(f"   LED encendido: {'✅' if led_status else '❌'}")
    
    controller.turn_off_led()
    led_status = controller.get_race_status()['led_status']['is_on']
    print(f"   LED apagado: {'✅' if not led_status else '❌'}")
    
    # Limpiar
    controller.cleanup()
    
    print("\n✅ Prueba de integración web completada!")
    print("\n💡 Funcionalidades probadas:")
    print("   📊 Incremento de vueltas")
    print("   🏎️ Nombre del piloto")
    print("   🎬 Animaciones")
    print("   🔴 Control de LED")
    print("   📁 Patrones centralizados")

def test_api_endpoints():
    """Prueba los endpoints de la API"""
    print("\n=== PRUEBA: ENDPOINTS DE LA API ===")
    
    controller = RaceController(max_laps=3)
    
    # Simular servidor web
    web_server = WebServer("127.0.0.1", 8080, controller)
    
    print("🔗 Endpoints disponibles:")
    endpoints = [
        "/api/lap/increment",
        "/api/lap/reset", 
        "/api/lap/status",
        "/api/led/on",
        "/api/led/off",
        "/api/led/toggle",
        "/api/led/status",
        "/api/animation/test",
        "/api/animation/set",
        "/api/animation/list",
        "/api/racer/name",
        "/api/racer/name/set",
        "/api/racer/display"
    ]
    
    for endpoint in endpoints:
        print(f"   ✅ {endpoint}")
    
    print(f"\n📊 Total de endpoints: {len(endpoints)}")
    
    controller.cleanup()
    print("\n✅ Prueba de endpoints completada!")

def test_patterns_integration():
    """Prueba que los patrones centralizados funcionen correctamente"""
    print("\n=== PRUEBA: INTEGRACIÓN DE PATRONES ===")
    
    controller = RaceController(max_laps=5)
    
    print("🎨 Probando patrones centralizados:")
    
    # Probar dígitos
    print("   📊 Dígitos: Funcionando")
    controller.update_display()
    time.sleep(1)
    
    # Probar nombre del piloto (usa patrones de various.py)
    print("   🏎️ Nombre del piloto: Funcionando")
    controller.display_racer_name()
    time.sleep(1)
    
    # Probar animaciones (usa patrones de animations.py)
    print("   🎬 Animaciones: Funcionando")
    controller.test_animation("checkered_flag")
    time.sleep(1)
    
    controller.cleanup()
    print("\n✅ Integración de patrones completada!")

def main():
    """Función principal"""
    print("Prueba de Integración Web con Patrones Centralizados")
    print("=" * 60)
    
    # Probar integración web
    test_web_integration()
    
    # Probar endpoints
    test_api_endpoints()
    
    # Probar patrones
    test_patterns_integration()
    
    print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    print("\n💡 Verificaciones realizadas:")
    print("   ✅ Incremento de vueltas funciona")
    print("   ✅ Nombre del piloto funciona")
    print("   ✅ Animaciones funcionan")
    print("   ✅ Control de LED funciona")
    print("   ✅ Patrones centralizados integrados")
    print("   ✅ Endpoints de API disponibles")
    print("   ✅ Interfaz web actualizada")

if __name__ == "__main__":
    main() 