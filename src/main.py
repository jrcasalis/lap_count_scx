"""
Controlador de Carrera - Raspberry Pi Pico 2W
Servidor Web Principal
"""

import time
from race_controller import RaceController
from web_server import WebServer

def main():
    """Función principal que inicializa todo el sistema"""
    print("🏁 CONTROLADOR DE CARRERA - SERVIDOR WEB")
    print("=" * 50)
    
    # Inicializar el controlador de carrera
    print("🔧 Inicializando controlador de carrera...")
    RaceController(max_laps=15, num_racers=2, racer_names=["Piloto 1", "Piloto 2"])
    print("✅ Controlador inicializado")
    
    # Mostrar estado inicial
    params = RaceController.get_race_params()
    print(f"🏁 Estado inicial: {params['race_state']}")
    print(f"🏎️ Pilotos: {params['racer_names']}")
    print(f"💡 Titileo: {'💡 Habilitado' if RaceController.get_stopped_blink_status() else '⚪ Deshabilitado'}")
    
    # Iniciar servidor web
    print("\n🌐 Iniciando servidor web...")
    server = WebServer()
    
    try:
        # Ejecutar servidor web (esto incluye el polling del titileo)
        server.run()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error en el servidor: {e}")
    finally:
        # Limpiar recursos
        if server:
            server.stop_server()
        print("🧹 Recursos liberados")

if __name__ == "__main__":
    main() 