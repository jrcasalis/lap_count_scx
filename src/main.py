"""
Controlador de Carrera - Raspberry Pi Pico 2W
Servidor Web Principal
"""

import time
from race_controller import RaceController
from web_server import WebServer
from config import RACE_MAX_LAPS, SENSOR_TCRT5000_PIN, SENSOR_DEBOUNCE_TIME


def main():
    """Función principal que inicializa todo el sistema"""
    print("🏁 CONTROLADOR DE CARRERA - SERVIDOR WEB")
    print("=" * 50)
    
    # Inicializar el controlador de carrera (mínimo para compatibilidad)
    print("\uD83D\uDD27 Inicializando controlador de carrera...")
    controller = RaceController(max_laps=15, num_racers=2, racer_names=["Piloto 1", "Piloto 2"])
    print("\u2705 Controlador inicializado")
    
    # Todo el código relacionado con el sensor IR y el contador de vueltas ha sido eliminado para reiniciar la lógica desde cero.
    
    # Iniciar servidor web
    print("\n🌐 Iniciando servidor web...")
    server = WebServer(controller)
    
    try:
        # Ejecutar servidor web (esto incluye el polling del titileo y sensor)
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