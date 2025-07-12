"""
Servidor web para Raspberry Pi Pico 2W
Maneja las peticiones HTTP y sirve la interfaz web para controlar el LED
"""

import socket
import json
import gc
import os
from config import LED_PIN_RED

class WebServer:
    def __init__(self, host, port, race_controller):
        """
        Inicializa el servidor web
        
        Args:
            host (str): Dirección IP del servidor
            port (int): Puerto del servidor
            race_controller: Instancia del controlador de carrera
        """
        self.host = host
        self.port = port
        self.race_controller = race_controller
        self.server_socket = None
        self.setup_socket()
        
    def setup_socket(self):
        """Configura el socket del servidor"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor web configurado en {self.host}:{self.port}")
        
    def handle_requests(self):
        """Maneja las peticiones HTTP entrantes"""
        try:
            # Sin timeout para aceptar conexiones
            client_socket, address = self.server_socket.accept()
            print(f"Petición de {address}")
            
            # Configurar timeout para la lectura
            client_socket.settimeout(2.0)
            request = client_socket.recv(1024).decode('utf-8')
            
            if request:
                response = self.process_request(request)
                # Enviar respuesta inmediatamente
                self.send_response(client_socket, response)
            
            client_socket.close()
            
        except OSError as e:
            # No hay peticiones pendientes - esto es normal
            if "timed out" not in str(e) and "110" not in str(e):
                print(f"Error en handle_requests: {e}")
            pass
            
    def send_response(self, client_socket, response):
        """Envía la respuesta HTTP de forma segura"""
        try:
            # Enviar en chunks si la respuesta es muy larga
            chunk_size = 1024
            for i in range(0, len(response), chunk_size):
                chunk = response[i:i + chunk_size]
                client_socket.send(chunk.encode('utf-8'))
        except Exception as e:
            print(f"Error enviando respuesta: {e}")
            
    def process_request(self, request):
        """Procesa la petición HTTP y retorna la respuesta"""
        lines = request.split('\n')
        if not lines:
            return self.http_response("400 Bad Request", "text/plain", "Bad Request")
            
        request_line = lines[0].strip()
        parts = request_line.split()
        
        if len(parts) < 2:
            return self.http_response("400 Bad Request", "text/plain", "Bad Request")
            
        method = parts[0]
        path = parts[1]
        
        print(f"Petición: {method} {path}")
        
        # Rutas de la API
        if path == "/":
            return self.serve_index()
        elif path == "/api/lap/increment":
            return self.api_lap_increment()
        elif path == "/api/lap/reset":
            return self.api_lap_reset()
        elif path == "/api/lap/status":
            return self.api_lap_status()
        elif path == "/api/led/on":
            return self.api_led_on()
        elif path == "/api/led/off":
            return self.api_led_off()
        elif path == "/api/led/toggle":
            return self.api_led_toggle()
        elif path == "/api/led/status":
            return self.api_led_status()
        elif path == "/api/animation/test":
            return self.api_animation_test()
        elif path == "/api/animation/set":
            return self.api_animation_set()
        elif path == "/api/animation/list":
            return self.api_animation_list()
        elif path == "/style.css":
            return self.serve_css()
        elif path == "/script.js":
            return self.serve_js()
        else:
            return self.http_response("404 Not Found", "text/plain", "Not Found")
            
    def serve_index(self):
        """Sirve el archivo index.html externo"""
        try:
            with open("web/index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            print("Longitud HTML:", len(html_content))
            return self.http_response("200 OK", "text/html", html_content)
        except Exception as e:
            print("Error al leer index.html:", e)
            return self.http_response("500 Internal Server Error", "text/plain", "Error interno del servidor")
        
    def serve_css(self):
        """Sirve el archivo style.css externo"""
        try:
            with open("web/style.css", "r", encoding="utf-8") as f:
                css_content = f.read()
            return self.http_response("200 OK", "text/css", css_content)
        except Exception as e:
            print("Error al leer style.css:", e)
            return self.http_response("404 Not Found", "text/plain", "CSS no encontrado")
        
    def serve_js(self):
        """Sirve el archivo script.js externo"""
        try:
            with open("web/script.js", "r", encoding="utf-8") as f:
                js_content = f.read()
            return self.http_response("200 OK", "application/javascript", js_content)
        except Exception as e:
            print("Error al leer script.js:", e)
            return self.http_response("404 Not Found", "text/plain", "JS no encontrado")
        
        
    def api_lap_increment(self):
        """API: Incrementar vuelta"""
        success = self.race_controller.increment_lap()
        status = self.race_controller.get_race_status()
        return self.json_response({
            "success": success,
            "message": "Vuelta incrementada" if success else "Ya se alcanzó el máximo",
            "race_status": status
        })
    
    def api_lap_reset(self):
        """API: Reiniciar carrera"""
        self.race_controller.reset_race()
        status = self.race_controller.get_race_status()
        return self.json_response({
            "success": True,
            "message": "Carrera reiniciada",
            "race_status": status
        })
    
    def api_lap_status(self):
        """API: Obtener estado de la carrera"""
        status = self.race_controller.get_race_status()
        return self.json_response({
            "success": True,
            "race_status": status
        })
    
    def api_led_on(self):
        """API: Encender LED"""
        self.race_controller.turn_on_led()
        return self.json_response({
            "success": True,
            "is_on": True,
            "message": "LED encendido"
        })
        
    def api_led_off(self):
        """API: Apagar LED"""
        self.race_controller.turn_off_led()
        return self.json_response({
            "success": True,
            "is_on": False,
            "message": "LED apagado"
        })
        
    def api_led_toggle(self):
        """API: Alternar LED"""
        is_on = self.race_controller.toggle_led()
        return self.json_response({
            "success": True,
            "is_on": is_on,
            "message": "LED alternado"
        })
        
    def api_led_status(self):
        """API: Obtener estado del LED"""
        is_on = self.race_controller.led.value() == 1
        return self.json_response({
            "success": True,
            "is_on": is_on,
            "pin": LED_PIN_RED
        })
    
    def api_animation_test(self):
        """API: Probar animación específica"""
        # Por ahora, usar animación por defecto
        animation_type = "checkered_flag"
        
        success = self.race_controller.test_animation(animation_type)
        return self.json_response({
            "success": success,
            "animation_type": animation_type,
            "message": "Animación ejecutada" if success else "Animación no válida"
        })
    
    def api_animation_set(self):
        """API: Cambiar animación de finalización"""
        # Por ahora, usar animación por defecto
        animation_type = "checkered_flag"
        
        success = self.race_controller.set_completion_animation(animation_type)
        return self.json_response({
            "success": success,
            "animation_type": animation_type,
            "message": "Animación configurada" if success else "Animación no válida"
        })
    
    def api_animation_list(self):
        """API: Obtener lista de animaciones disponibles"""
        animations = self.race_controller.get_available_animations()
        return self.json_response({
            "success": True,
            "animations": animations
        })
        
    def json_response(self, data):
        """Retorna una respuesta JSON"""
        return self.http_response("200 OK", "application/json", json.dumps(data))
        
    def http_response(self, status, content_type, content):
        """Retorna una respuesta HTTP completa con formato correcto"""
        response = "HTTP/1.1 {}\r\n".format(status)
        response += "Content-Type: {}; charset=utf-8\r\n".format(content_type)
        response += "Content-Length: {}\r\n".format(len(content.encode('utf-8')))
        response += "Connection: close\r\n"
        response += "\r\n"  # Doble salto de línea obligatorio
        response += content
        return response 