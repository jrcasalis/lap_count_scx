"""
Servidor Web Optimizado para MicroPython
Raspberry Pi Pico W - Controlador de Carrera
"""

import network
import socket
import time
import gc
from config import *
from race_controller import RaceController

class WebServer:
    def __init__(self, controller):
        self.controller = controller
        self.wlan = None
        self.server_socket = None
        self.is_running = False
        self.last_update = 0
        self.update_interval = 0.1

    def connect_wifi(self):
        print("[WEB] Conectando a WiFi...")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print(f"[WEB] Conectando a {WIFI_SSID}...")
            self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            max_wait = 10
            while max_wait > 0:
                if self.wlan.isconnected():
                    break
                max_wait -= 1
                print("[WEB] Esperando conexión...")
                time.sleep(1)
        if self.wlan.isconnected():
            ip = self.wlan.ifconfig()[0]
            print(f"[WEB] ✅ WiFi conectado!")
            print(f"[WEB] 📡 Dirección IP: {ip}")
            print(f"[WEB] 🌐 Servidor web: http://{ip}:80")
            return ip
        else:
            print("[WEB] ❌ Error al conectar WiFi")
            return None

    def start_server(self):
        print("[WEB] Iniciando servidor web...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind(('', 80))
            self.server_socket.listen(5)
            self.server_socket.settimeout(0.1)
            self.is_running = True
            print("[WEB] ✅ Servidor iniciado en puerto 80")
            return True
        except Exception as e:
            print(f"[WEB] ❌ Error iniciando servidor: {e}")
            return False

    def stop_server(self):
        print("[WEB] Deteniendo servidor web...")
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        print("[WEB] ✅ Servidor detenido")

    def handle_request(self, client_socket, address):
        try:
            client_socket.settimeout(0.1)
            try:
                request = client_socket.recv(1024).decode('utf-8')
            except Exception:
                request = ''
            if not request:
                response = self.get_404()
            else:
                print(f"[WEB] Solicitud de {address}: {request.split()[0]} {request.split()[1]}")
                lines = request.split('\n')
                if len(lines) < 1:
                    response = self.get_404()
                else:
                    request_line = lines[0].strip()
                    if not request_line:
                        response = self.get_404()
                    else:
                        try:
                            method, path, _ = request_line.split(' ', 2)
                        except Exception:
                            response = self.get_404()
                        else:
                            if method == 'GET':
                                if path == '/' or path == '/index.html':
                                    response = self.serve_index()
                                elif path == '/start_race':
                                    self.controller.start_race()
                                    response = self.text_response('Carrera iniciada')
                                elif path == '/stop_race':
                                    self.controller.stop_race()
                                    response = self.text_response('Carrera detenida')
                                elif path == '/start_previous':
                                    self.controller.start_race_previous()
                                    response = self.text_response('Previa iniciada')
                                elif path == '/stop_previous':
                                    self.controller.stop_race_previous()
                                    response = self.text_response('Previa detenida')
                                elif path == '/reset':
                                    self.controller.inicializar_carrera()
                                    response = self.text_response('Parámetros reseteados')
                                else:
                                    response = self.get_404()
                            else:
                                response = self.get_405()
            client_socket.sendall(response)
        except Exception as e:
            print(f"[WEB] Error manejando solicitud: {e}")
        finally:
            try:
                client_socket.settimeout(0)
                while True:
                    if not client_socket.recv(1024):
                        break
            except:
                pass
            client_socket.close()

    def serve_index(self):
        try:
            with open('../web/index.html', 'r') as f:
                html = f.read()
        except Exception:
            html = "<html><body>Error cargando index.html</body></html>"
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(html))
        return (headers + html).encode('utf-8')

    def text_response(self, msg):
        body = msg
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(body))
        return (headers + body).encode('utf-8')

    def get_404(self):
        body = "404 Not Found"
        headers = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(body))
        return (headers + body).encode('utf-8')

    def get_405(self):
        body = "405 Method Not Allowed"
        headers = (
            "HTTP/1.1 405 Method Not Allowed\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(body))
        return (headers + body).encode('utf-8')

    def run(self):
        print("[WEB] 🚀 Iniciando servidor web básico...")
        ip = self.connect_wifi()
        if not ip:
            print("[WEB] ❌ No se pudo conectar a WiFi")
            return False
        if not self.start_server():
            return False
        print(f"[WEB] 🌐 Servidor web disponible en: http://{ip}:80")
        print("[WEB] 💡 El titileo del display y semáforo continúa funcionando")
        while self.is_running:
            try:
                current_time = time.time()
                if current_time - self.last_update >= self.update_interval:
                    self.controller.update()
                    self.controller.poll_sensor_and_update_laps()
                    self.last_update = current_time
                try:
                    client_socket, address = self.server_socket.accept()
                    self.handle_request(client_socket, address)
                except OSError as e:
                    if hasattr(e, 'errno') and e.errno == 110:
                        pass
                    else:
                        print(f"[WEB] Error aceptando conexión: {e}")
                except Exception as e:
                    print(f"[WEB] Error aceptando conexión: {e}")
                gc.collect()
            except KeyboardInterrupt:
                print("\n[WEB] ⏹️ Deteniendo servidor...")
                break
            except Exception as e:
                print(f"[WEB] Error en bucle principal: {e}")
                time.sleep(1)
        self.stop_server()
        return True

def start_web_server():
    # Assuming RaceController is available globally or passed as an argument
    # For now, we'll create an instance directly, but ideally, it should be passed
    # from the main application.
    # For demonstration, we'll create a dummy controller if not available.
    # In a real scenario, you'd pass the actual RaceController instance.
    # For now, we'll create a dummy one.
    class DummyController:
        def update(self):
            print("Dummy update called")
        def poll_sensor_and_update_laps(self):
            print("Dummy poll_sensor_and_update_laps called")
        def start_race(self):
            print("Dummy start_race called")
        def stop_race(self):
            print("Dummy stop_race called")
        def start_race_previous(self):
            print("Dummy start_race_previous called")
        def stop_race_previous(self):
            print("Dummy stop_race_previous called")
        def inicializar_carrera(self):
            print("Dummy inicializar_carrera called")

    dummy_controller = DummyController()
    server = WebServer(dummy_controller)
    return server.run()

if __name__ == "__main__":
    start_web_server() 