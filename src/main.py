"""
Controlador de Carrera - Raspberry Pi Pico 2W
Servidor Web Principal
"""

import time
from race_controller import RaceController
from web_server import WebServer
from config import RACE_MAX_LAPS, RACE_NUM_RACERS, RACER_NAME


def main():
    """Función principal que inicializa todo el sistema"""
    print("🏁 CONTROLADOR DE CARRERA - SERVIDOR WEB")
    print("=" * 50)
    
    # Inicializar el controlador de carrera usando configuraciones
    print("\uD83D\uDD27 Inicializando controlador de carrera...")
    print(f"   📊 Configuración: {RACE_MAX_LAPS} vueltas, {RACE_NUM_RACERS} corredor(es)")
    
    # Generar nombres de pilotos basados en la configuración
    racer_names = [f"{RACER_NAME} {i+1}" for i in range(RACE_NUM_RACERS)]
    
    controller = RaceController(
        max_laps=RACE_MAX_LAPS, 
        num_racers=RACE_NUM_RACERS, 
        racer_names=racer_names
    )
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