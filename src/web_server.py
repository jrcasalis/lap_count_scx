"""
Servidor web para Raspberry Pi Pico 2W
Maneja las peticiones HTTP y sirve la interfaz web para controlar el LED
"""

import socket
import json
import gc
import os
import time
from config import LED_PIN_RED, TRAFFIC_LIGHT_STATE_BLINKING, DEBUG_ENABLED

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
        """Maneja las peticiones HTTP entrantes de forma no bloqueante"""
        try:
            # Configurar socket como no bloqueante para respuesta rápida
            self.server_socket.setblocking(False)
            
            # Intentar aceptar conexión sin bloquear
            try:
                client_socket, address = self.server_socket.accept()
                print(f"🌐 Nueva conexión de {address}")
                
                # Configurar timeout muy corto para respuesta rápida
                client_socket.settimeout(0.5)  # 500ms en lugar de 2s
                print(f"⏱️ Timeout configurado: 0.5 segundos")
                
                request = client_socket.recv(1024).decode('utf-8')
                print(f"📥 Datos recibidos: {len(request)} caracteres")
                
                if request:
                    print(f"📋 Procesando petición...")
                    response = self.process_request(request)
                    print(f"📤 Enviando respuesta...")
                    # Enviar respuesta inmediatamente
                    self.send_response(client_socket, response)
                    print(f"✅ Respuesta enviada")
                else:
                    print(f"⚠️ Petición vacía recibida")
                
                print(f"🔌 Cerrando conexión con {address}")
                client_socket.close()
                print(f"✅ Conexión cerrada")
                
            except OSError as e:
                # No hay conexiones pendientes - esto es normal y esperado
                if "11" in str(e) or "timed out" in str(e):
                    # EAGAIN/EWOULDBLOCK - no hay conexiones pendientes
                    pass
                else:
                    print(f"❌ Error aceptando conexión: {e}")
                    
        except Exception as e:
            print(f"❌ Error en handle_requests: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            print(f"   Código de error: {getattr(e, 'errno', 'N/A')}")
            
    def send_response(self, client_socket, response):
        """Envía la respuesta HTTP de forma segura"""
        try:
            print(f"📤 Enviando respuesta - Tipo: {type(response)}, Longitud: {len(response)}")
            
            # Enviar en chunks si la respuesta es muy larga
            chunk_size = 1024
            total_sent = 0
            chunks_sent = 0
            
            for i in range(0, len(response), chunk_size):
                chunk = response[i:i + chunk_size]
                chunk_size_actual = len(chunk)
                
                try:
                    # Si response es bytes, enviar directamente; si no, codificar
                    if isinstance(response, bytes):
                        bytes_sent = client_socket.send(chunk)
                    else:
                        # Si response no es bytes, chunk tampoco lo es, así que codificar
                        bytes_sent = client_socket.send(chunk.encode('utf-8'))
                    
                    total_sent += bytes_sent
                    chunks_sent += 1
                    
                    if chunks_sent % 10 == 0:  # Log cada 10 chunks para no saturar
                        print(f"📦 Chunk {chunks_sent}: {bytes_sent}/{chunk_size_actual} bytes enviados")
                        
                except Exception as chunk_error:
                    print(f"❌ Error enviando chunk {chunks_sent}: {chunk_error}")
                    print(f"   Chunk size: {chunk_size_actual}, Bytes enviados hasta ahora: {total_sent}")
                    raise chunk_error
            
            print(f"✅ Respuesta enviada exitosamente: {total_sent} bytes en {chunks_sent} chunks")
            
        except Exception as e:
            print(f"❌ Error enviando respuesta: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            print(f"   Código de error: {getattr(e, 'errno', 'N/A')}")
            print(f"   Mensaje: {str(e)}")
            
            # Intentar cerrar el socket de forma segura
            try:
                client_socket.close()
                print("🔌 Socket cerrado después del error")
            except:
                print("⚠️ No se pudo cerrar el socket")
            
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
        elif path == "/api/race/start":
            return self.api_race_start()
        elif path == "/api/race/stop":
            return self.api_race_stop()
        elif path == "/api/race/status":
            return self.api_race_status()
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
        elif path == "/api/racer/name":
            return self.api_racer_name()
        elif path.startswith("/api/racer/name/set"):
            return self.api_racer_name_set(request)
        elif path == "/api/racer/display":
            return self.api_racer_display()
        elif path.startswith("/api/racer/scroll/speed"):
            return self.api_racer_scroll_speed(request)
        elif path == "/api/traffic-light/previous":
            return self.api_traffic_previous()
        elif path == "/api/traffic-light/previous-stop":
            return self.api_traffic_previous_stop()
        elif path == "/api/traffic-light/start":
            return self.api_traffic_start()
        elif path == "/api/traffic-light/stop":
            return self.api_traffic_stop()
        elif path == "/api/traffic-light/status":
            return self.api_traffic_status()
        elif path == "/style.css":
            return self.serve_css()
        elif path == "/script.js":
            return self.serve_js()
        elif path.startswith("/sounds/"):
            return self.serve_sound(path)
        elif path == "/test-sound.html":
            return self.serve_test_sound()
        elif path == "/test-sound-fix.html":
            return self.serve_test_sound_fix()
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
    
    def serve_test_sound(self):
        """Sirve el archivo de prueba de sonido"""
        try:
            with open("examples/test_browser_sound.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            return self.http_response("200 OK", "text/html", html_content)
        except Exception as e:
            print("Error al leer test_browser_sound.html:", e)
            return self.http_response("404 Not Found", "text/plain", "Archivo de prueba no encontrado")
    
    def serve_test_sound_fix(self):
        """Sirve el archivo de prueba de sonido corregido"""
        try:
            with open("test_sound_fix.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            return self.http_response("200 OK", "text/html", html_content)
        except Exception as e:
            print("Error al leer test_sound_fix.html:", e)
            return self.http_response("404 Not Found", "text/plain", "Archivo de prueba corregido no encontrado")
    
    def serve_sound(self, path):
        """Sirve archivos de sonido con el tipo MIME correcto según la extensión"""
        try:
            print(f"🎵 === SIRVIENDO ARCHIVO DE SONIDO ===")
            print(f"📁 Path solicitado: {path}")
            
            # Extraer el nombre del archivo de sonido
            sound_file = path.replace("/sounds/", "")
            print(f"📄 Nombre del archivo: {sound_file}")
            
            # Construir la ruta completa del archivo
            file_path = f"web/sounds/{sound_file}"
            print(f"🗂️ Ruta completa: {file_path}")
            
            # Leer el archivo de sonido en modo binario
            print(f"📖 Leyendo archivo...")
            try:
                with open(file_path, "rb") as f:
                    sound_content = f.read()
                print(f"✅ Archivo leído: {len(sound_content)} bytes")
            except OSError as e:
                print(f"❌ Error leyendo archivo: {e}")
                return self.http_response("404 Not Found", "text/plain", "Archivo de sonido no encontrado")

            # Determinar el tipo MIME según la extensión
            ext = sound_file.lower().split('.')[-1]
            if ext == "mp3":
                content_type = "audio/mpeg"
            elif ext == "wav":
                content_type = "audio/wav"
            else:
                content_type = "application/octet-stream"  # Por defecto
            print(f"🎵 Tipo MIME: {content_type} (extensión: .{ext})")
            
            print(f"📤 Preparando respuesta HTTP...")
            response = self.http_response("200 OK", content_type, sound_content, is_binary=True)
            print(f"✅ Respuesta preparada: {len(response)} bytes")
            
            return response
        except Exception as e:
            print(f"❌ Error al leer archivo de sonido {path}:")
            print(f"   Tipo de error: {type(e).__name__}")
            print(f"   Mensaje: {str(e)}")
            return self.http_response("404 Not Found", "text/plain", "Archivo de sonido no encontrado")
        
        
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
    
    def api_race_start(self):
        """API: Iniciar carrera"""
        success = self.race_controller.start_race()
        status = self.race_controller.get_race_status()
        return self.json_response({
            "success": success,
            "message": "Carrera iniciada" if success else "Error al iniciar carrera",
            "race_status": status
        })
    
    def api_race_stop(self):
        """API: Detener carrera"""
        success = self.race_controller.stop_race()
        status = self.race_controller.get_race_status()
        return self.json_response({
            "success": success,
            "message": "Carrera detenida" if success else "Error al detener carrera",
            "race_status": status
        })
    
    def api_race_status(self):
        """API: Obtener estado detallado de la carrera"""
        status = self.race_controller.get_race_status()
        return self.json_response({
            "success": True,
            "race_status": status,
            "message": "Estado de la carrera obtenido"
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
    
    def api_racer_name(self):
        """API: Obtener o cambiar nombre del piloto"""
        # Por ahora solo retorna el nombre actual
        # En el futuro se puede implementar cambio via POST
        racer_name = self.race_controller.get_racer_name()
        return self.json_response({
            "success": True,
            "racer_name": racer_name,
            "message": "Nombre del piloto obtenido"
        })
    
    def api_racer_name_set(self, request):
        """API: Cambiar nombre del piloto (GET con parámetro name)"""
        # Leer el nombre desde los parámetros de la URL
        new_name = "PILOTO"  # Nombre por defecto
        
        # Intentar leer el parámetro name de la URL
        try:
            # Buscar el parámetro name en la URL
            if "name=" in request:
                # Extraer el valor del parámetro name
                name_start = request.find("name=") + 5
                name_end = request.find("&", name_start)
                if name_end == -1:
                    name_end = request.find(" ", name_start)
                if name_end == -1:
                    name_end = len(request)
                
                if name_start < name_end:
                    new_name = request[name_start:name_end]
                    # Decodificar URL encoding
                    new_name = new_name.replace("%20", " ").replace("+", " ")
        except:
            pass  # Si hay error, usar el nombre por defecto
        
        success = self.race_controller.set_racer_name(new_name)
        
        if success:
            return self.json_response({
                "success": True,
                "racer_name": new_name,
                "message": "Nombre del piloto actualizado y mostrado en display"
            })
        else:
            return self.json_response({
                "success": False,
                "message": "Error al actualizar nombre del piloto"
            })
    
    def api_racer_display(self):
        """API: Mostrar nombre del piloto en display"""
        self.race_controller.display_racer_name()
        return self.json_response({
            "success": True,
            "message": "Nombre del piloto mostrado en display"
        })
    
    def api_racer_scroll_speed(self, request):
        """API: Obtener o cambiar velocidad del scroll del nombre del piloto"""
        # Por ahora solo retorna la velocidad actual
        # En el futuro se puede implementar cambio via parámetros
        current_speed = self.race_controller.get_scroll_speed()
        return self.json_response({
            "success": True,
            "scroll_speed": current_speed,
            "message": "Velocidad de scroll obtenida"
        })
    
    # =============================================================================
    # API DEL SEMÁFORO
    # =============================================================================
    
    def api_traffic_previous(self):
        """API: Iniciar previa (titileo)"""
        success = self.race_controller.race_previous()
        traffic_status = self.race_controller.get_traffic_light_status()
        return self.json_response({
            "success": success,
            "message": "Previa iniciada" if success else "Error al iniciar previa",
            "traffic_light_status": traffic_status
        })
    
    def api_traffic_previous_stop(self):
        """API: Terminar previa (titileo)"""
        success = self.race_controller.race_previous_stop()
        traffic_status = self.race_controller.get_traffic_light_status()
        return self.json_response({
            "success": success,
            "message": "Previa terminada" if success else "Error al terminar previa",
            "traffic_light_status": traffic_status
        })
    
    def api_traffic_start(self):
        """API: Iniciar carrera (secuencia de largada)"""
        try:
            # Si hay previa activa, terminarla automáticamente sin mensajes
            if self.race_controller.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
                if DEBUG_ENABLED:
                    print("[WEB] Previa activa detectada - terminando automáticamente")
                self.race_controller.traffic_light.race_previous_stop()
                # Esperar un momento para que se complete la terminación
                time.sleep(0.1)
            
            # Verificar que la previa se terminó correctamente
            if self.race_controller.traffic_light.current_state == TRAFFIC_LIGHT_STATE_BLINKING:
                if DEBUG_ENABLED:
                    print("[WEB] Previa aún activa, intentando terminar nuevamente")
                self.race_controller.traffic_light.race_previous_stop()
                time.sleep(0.1)
            
            success = self.race_controller.race_start()
            traffic_status = self.race_controller.get_traffic_light_status()
            race_status = self.race_controller.get_race_status()
            
            return self.json_response({
                "success": success,
                "message": "Carrera iniciada" if success else "Error al iniciar carrera",
                "traffic_light_status": traffic_status,
                "race_status": race_status
            })
        except Exception as e:
            if DEBUG_ENABLED:
                print(f"[WEB] Error en api_traffic_start: {e}")
            return self.json_response({
                "success": False,
                "message": f"Error al iniciar carrera: {str(e)}",
                "traffic_light_status": self.race_controller.get_traffic_light_status(),
                "race_status": self.race_controller.get_race_status()
            })
    
    def api_traffic_stop(self):
        """API: Parar carrera (apagar semáforos)"""
        success = self.race_controller.race_stop()
        traffic_status = self.race_controller.get_traffic_light_status()
        race_status = self.race_controller.get_race_status()
        
        return self.json_response({
            "success": success,
            "message": "Carrera parada" if success else "Error al parar carrera",
            "traffic_light_status": traffic_status,
            "race_status": race_status
        })
    
    def api_traffic_status(self):
        """API: Obtener estado del semáforo"""
        traffic_status = self.race_controller.get_traffic_light_status()
        race_status = self.race_controller.get_race_status()
        
        return self.json_response({
            "success": True,
            "traffic_light_status": traffic_status,
            "race_status": race_status,
            "message": "Estado del semáforo obtenido"
        })
        
    def json_response(self, data):
        """Retorna una respuesta JSON"""
        return self.http_response("200 OK", "application/json", json.dumps(data))
        
    def http_response(self, status, content_type, content, is_binary=False):
        """Retorna una respuesta HTTP completa con formato correcto"""
        response = "HTTP/1.1 {}\r\n".format(status)
        response += "Content-Type: {}\r\n".format(content_type)
        
        if is_binary:
            response += "Content-Length: {}\r\n".format(len(content))
        else:
            response += "Content-Length: {}\r\n".format(len(content.encode('utf-8')))
            
        response += "Connection: close\r\n"
        response += "\r\n"  # Doble salto de línea obligatorio
        
        if is_binary:
            # Para archivos binarios, codificar la respuesta como bytes
            response_bytes = response.encode('utf-8') + content
            return response_bytes
        else:
            response += content
            return response 