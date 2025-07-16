"""
Servidor Web Optimizado para MicroPython
Raspberry Pi Pico W - Controlador de Carrera
"""

import network
import socket
import time
import gc
import json
from config import *
from race_controller import RaceController

class WebServer:
    def __init__(self, controller):
        self.controller = controller
        self.wlan = None
        self.server_socket = None
        self.is_running = False
        self.last_update = 0
        self.update_interval = WEB_SERVER_UPDATE_INTERVAL

    def connect_wifi(self):
        print("[WEB] Conectando a WiFi...")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print(f"[WEB] Conectando a {WIFI_SSID}...")
            self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            max_wait = WIFI_CONNECT_TIMEOUT
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
                client_socket.sendall(response)
            else:
                print(f"[WEB] Solicitud de {address}: {request.split()[0]} {request.split()[1]}")
                lines = request.split('\n')
                if len(lines) < 1:
                    response = self.get_404()
                    client_socket.sendall(response)
                else:
                    request_line = lines[0].strip()
                    if not request_line:
                        response = self.get_404()
                        client_socket.sendall(response)
                    else:
                        try:
                            method, path, _ = request_line.split(' ', 2)
                        except Exception:
                            response = self.get_404()
                            client_socket.sendall(response)
                        else:
                            if method == 'GET':
                                if path == '/' or path == '/index.html':
                                    _, send_index_streaming = self.serve_index()
                                    send_index_streaming(client_socket)
                                elif path == '/favicon.ico':
                                    response = self.serve_favicon()
                                    client_socket.sendall(response)
                                elif path == '/script.js':
                                    response = self.serve_script()
                                    client_socket.sendall(response)
                                elif path == '/api/status':
                                    response = self.json_response(self.get_race_status())
                                    client_socket.sendall(response)
                                elif path == '/start_race':
                                    try:
                                        ok = self.controller.start_race()
                                        if ok:
                                            response = self.json_response({
                                                'success': True,
                                                'message': 'Carrera iniciada',
                                                'action': 'start_race'
                                            })
                                        else:
                                            response = self.json_response({
                                                'success': False,
                                                'message': 'No se pudo iniciar la carrera',
                                                'action': 'start_race',
                                                'error': 'Error en RaceController o semáforo'
                                            })
                                    except Exception as e:
                                        print(f"[WEB] Error en /start_race: {e}")
                                        response = self.json_response({
                                            'success': False,
                                            'message': 'Excepción en start_race',
                                            'error': str(e),
                                            'action': 'start_race'
                                        })
                                    client_socket.sendall(response)
                                elif path == '/stop_race':
                                    self.controller.stop_race()
                                    response = self.json_response({
                                        'success': True,
                                        'message': 'Carrera detenida',
                                        'action': 'stop_race'
                                    })
                                    client_socket.sendall(response)
                                elif path == '/start_previous':
                                    self.controller.start_race_previous()
                                    response = self.json_response({
                                        'success': True,
                                        'message': 'Previa iniciada',
                                        'action': 'start_previous'
                                    })
                                    client_socket.sendall(response)
                                elif path == '/stop_previous':
                                    self.controller.stop_race_previous()
                                    response = self.json_response({
                                        'success': True,
                                        'message': 'Previa detenida',
                                        'action': 'stop_previous'
                                    })
                                elif path == '/reset':
                                    try:
                                        self.controller.inicializar_carrera()
                                        response = self.json_response({
                                            'success': True,
                                            'message': 'Parámetros reseteados',
                                            'action': 'reset'
                                        })
                                    except Exception as e:
                                        response = self.json_response({
                                            'success': False,
                                            'error': str(e),
                                            'message': 'Error al resetear parámetros',
                                            'action': 'reset'
                                        })
                                    client_socket.sendall(response)
                                else:
                                    response = self.get_404()
                                    client_socket.sendall(response)
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

    def get_race_status(self):
        """Obtiene el estado completo de la carrera"""
        try:
            # Usar el primer corredor (índice 0) para compatibilidad
            current_laps = self.controller.current_laps[0] if self.controller.current_laps else 0
            max_laps = RACE_MAX_LAPS
            return {
                'success': True,
                'race_state': self.controller.race_state,
                'current_laps': current_laps,
                'max_laps': max_laps,
                'remaining_laps': max(0, max_laps - current_laps),
                'progress_percentage': round((current_laps / max_laps) * 100, 1) if max_laps else 0,
                'is_completed': self.controller.race_state == 'FINISHED',
                'traffic_light_state': self.controller.traffic_light.get_status() if self.controller.traffic_light else None,
                'racer_name': RACER_NAME,
                'sensor_active': SENSOR_AUTO_INCREMENT,
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error obteniendo estado de la carrera'
            }

    def serve_index(self):
        def send_index_streaming(sock):
            try:
                print(f"[WEB] Streaming archivo HTML desde: web/index.html")
                headers = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n\r\n"
                )
                sock.sendall(headers.encode('utf-8'))
                with open('web/index.html', 'r') as f:
                    for line in f:
                        sock.sendall(line.encode('utf-8'))
                print(f"[WEB] HTML enviado por streaming")
            except Exception as e:
                print(f"[WEB] Error en streaming HTML: {e}")
                error_html = f"<html><body>Error cargando index.html: {e}</body></html>"
                sock.sendall(error_html.encode('utf-8'))
        return None, send_index_streaming

    def serve_favicon(self):
        """Sirve un favicon básico (1x1 pixel transparente)"""
        # Favicon básico de 1x1 pixel transparente en formato ICO
        favicon_data = b'\x00\x00\x01\x00\x01\x00\x01\x01\x00\x00\x01\x00\x18\x00\x28\x00\x00\x00\x16\x00\x00\x00\x28\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: image/x-icon\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(favicon_data))
        return headers.encode('utf-8') + favicon_data

    def serve_script(self):
        """Sirve el archivo JavaScript"""
        try:
            print(f"[WEB] Intentando cargar JavaScript desde: web/script.js")
            with open('web/script.js', 'r') as f:
                script = f.read()
            print(f"[WEB] JavaScript cargado correctamente ({len(script)} caracteres)")
        except Exception as e:
            print(f"[WEB] Error cargando JavaScript: {e}")
            script = "console.error('Error cargando script.js: " + str(e) + "');"
        
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/javascript\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(script))
        return (headers + script).encode('utf-8')

    def json_response(self, data):
        """Devuelve una respuesta JSON"""
        try:
            body = json.dumps(data, separators=(',', ':'))
        except Exception as e:
            body = json.dumps({
                'success': False,
                'error': 'Error serializando JSON',
                'message': str(e)
            }, separators=(',', ':'))
        
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(body))
        return (headers + body).encode('utf-8')

    def text_response(self, msg):
        """Devuelve una respuesta de texto plano (mantiene compatibilidad)"""
        body = msg
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(body))
        return (headers + body).encode('utf-8')

    def get_404(self):
        body = json.dumps({
            'success': False,
            'error': '404 Not Found',
            'message': 'Endpoint no encontrado'
        }, separators=(',', ':'))
        headers = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n"
        ).format(len(body))
        return (headers + body).encode('utf-8')

    def get_405(self):
        body = json.dumps({
            'success': False,
            'error': '405 Method Not Allowed',
            'message': 'Método HTTP no permitido'
        }, separators=(',', ':'))
        headers = (
            "HTTP/1.1 405 Method Not Allowed\r\n"
            "Content-Type: application/json\r\n"
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
                break
        self.stop_server()

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