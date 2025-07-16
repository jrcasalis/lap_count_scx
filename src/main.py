"""
Controlador de Carrera - Raspberry Pi Pico 2W
Servidor Web Principal
"""

import time
from race_controller import RaceController
from web_server import WebServer
from config import (
    RACE_MAX_LAPS, RACE_NUM_RACERS, RACER_NAME, 
    SERVER_ONLY_MODE, ENABLE_WEB_INTERFACE
)


def main():
    """Función principal que inicializa todo el sistema"""
    print("🏁 CONTROLADOR DE CARRERA - SERVIDOR MCP")
    print("=" * 50)
    
    # Mostrar modo de operación
    if SERVER_ONLY_MODE:
        print("🔧 MODO: Servidor API únicamente")
        print("   📱 Consumir desde aplicación mobile")
    else:
        print("🌐 MODO: Servidor con interfaz web")
        if ENABLE_WEB_INTERFACE:
            print("   💻 Interfaz web habilitada")
        else:
            print("   💻 Interfaz web deshabilitada")
    
    # Inicializar el controlador de carrera usando configuraciones
    print("\n🔧 Inicializando controlador de carrera...")
    print(f"   📊 Configuración: {RACE_MAX_LAPS} vueltas, {RACE_NUM_RACERS} corredor(es)")
    
    # Generar nombres de pilotos basados en la configuración
    racer_names = [f"{RACER_NAME} {i+1}" for i in range(RACE_NUM_RACERS)]
    
    controller = RaceController(
        max_laps=RACE_MAX_LAPS, 
        num_racers=RACE_NUM_RACERS, 
        racer_names=racer_names
    )
    print("✅ Controlador inicializado")
    
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


def run_server_only():
    """Función para ejecutar solo el servidor API (sin interfaz web)"""
    print("🚀 Iniciando servidor MCP (Maestro de Control de Pista)...")
    main()


def run_with_interface():
    """Función para ejecutar con interfaz web"""
    print("🌐 Iniciando servidor con interfaz web...")
    main()


if __name__ == "__main__":
    if SERVER_ONLY_MODE:
        run_server_only()
    else:
        run_with_interface() 