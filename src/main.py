"""
Controlador de Carrera - Raspberry Pi Pico 2W
Archivo principal que maneja la conexión WiFi, servidor web y control de carrera
"""

import network
import socket
import time
from machine import Pin
from web_server import WebServer
from race_controller import RaceController
from config import WIFI_SSID, WIFI_PASSWORD, SERVER_PORT, LED_PIN_RED, SENSOR_TCRT5000_PIN
import utime

def connect_wifi():
    """Conecta a la red WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Conectando a {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Esperar hasta 10 segundos para conectar
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print("Esperando conexión...")
            time.sleep(1)
    
    if wlan.isconnected():
        print("WiFi conectado!")
        print(f"Dirección IP: {wlan.ifconfig()[0]}")
        return wlan.ifconfig()[0]
    else:
        print("Error al conectar WiFi")
        return None

def main():
    """Función principal"""
    print("Iniciando Controlador de Carrera...")
    
    # Inicializar controlador de carrera
    race_controller = RaceController(max_laps=10)
    
    # Inicializar sensor TCRT5000
    sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN)
    last_sensor_state = sensor.value()
    
    # Conectar WiFi
    ip_address = connect_wifi()
    if not ip_address:
        print("No se pudo conectar a WiFi. Ejecutando en modo local...")
        ip_address = "192.168.1.100"  # IP por defecto
    
    # Inicializar servidor web
    web_server = WebServer(ip_address, SERVER_PORT, race_controller)
    
    print(f"Servidor web iniciado en http://{ip_address}:{SERVER_PORT}")
    print("Presiona Ctrl+C para detener")
    
    try:
        # Bucle principal del servidor
        while True:
            web_server.handle_requests()
            current_sensor_state = sensor.value()
            # Detectar flanco descendente (detección de objeto)
            if last_sensor_state == 1 and current_sensor_state == 0:
                print("[TCRT5000] Detección de objeto - Incrementando vuelta")
                race_controller.increment_lap()
            last_sensor_state = current_sensor_state
            time.sleep(0.01)  # Pequeña pausa para no saturar el CPU
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        race_controller.cleanup()

if __name__ == "__main__":
    main() 