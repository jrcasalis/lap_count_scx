"""
Ejemplo: Test de nombre del piloto desde la web (versión corregida)
Prueba la funcionalidad completa de cambiar y mostrar el nombre del piloto
con parámetros de URL y conversión a mayúsculas
"""

import time
from race_controller import RaceController
from web_server import WebServer
from config import *

def test_racer_name_web_fixed():
    """Prueba el nombre del piloto desde la web con parámetros"""
    print("=== Test de Nombre del Piloto desde Web (Corregido) ===")
    
    # Crear controlador
    controller = RaceController(max_laps=10)
    
    # Crear servidor web
    server = WebServer("0.0.0.0", SERVER_PORT, controller)
    
    print(f"Servidor web iniciado en 0.0.0.0:{SERVER_PORT}")
    print("Accede a la interfaz web para probar:")
    print(f"http://<ip-pico>:{SERVER_PORT}")
    print("\nInstrucciones:")
    print("1. Abre la interfaz web en tu navegador")
    print("2. Ve a la sección 'Nombre del Piloto'")
    print("3. Escribe un nombre (se convertirá automáticamente a mayúsculas)")
    print("4. Presiona 'Guardar Nombre'")
    print("5. Deberías ver el scroll del nombre real en el display")
    print("6. El nombre se guardará y se mostrará automáticamente")
    print("\nPruebas adicionales:")
    print("- Escribe 'juan' y debería guardarse como 'JUAN'")
    print("- Escribe 'maria' y debería guardarse como 'MARIA'")
    print("- El campo siempre se mantiene en mayúsculas")
    
    try:
        # Manejar peticiones web
        while True:
            server.handle_requests()
            time.sleep(0.1)  # Pequeña pausa para no saturar CPU
            
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        controller.cleanup()
        print("Servidor detenido")

if __name__ == "__main__":
    test_racer_name_web_fixed() 