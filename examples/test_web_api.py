"""
Script de prueba para verificar las APIs del servidor web
"""

import socket
import json
import time

def test_api(host, port, endpoint):
    """Prueba una API específica"""
    try:
        # Crear socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        
        # Crear petición HTTP
        request = f"GET {endpoint} HTTP/1.1\r\n"
        request += f"Host: {host}:{port}\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"
        
        # Enviar petición
        sock.send(request.encode())
        
        # Recibir respuesta
        response = b""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data
        
        sock.close()
        
        # Parsear respuesta
        response_str = response.decode('utf-8')
        
        # Buscar el JSON en la respuesta
        json_start = response_str.find('\r\n\r\n') + 4
        if json_start > 3:
            json_data = response_str[json_start:]
            try:
                data = json.loads(json_data)
                return True, data
            except:
                return False, f"Error parsing JSON: {json_data[:100]}"
        else:
            return False, f"Response: {response_str[:100]}"
            
    except Exception as e:
        return False, f"Connection error: {e}"

def test_connectivity(host, port):
    """Prueba conectividad básica"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.close()
        return True
    except:
        return False

def main():
    """Función principal de prueba"""
    port = 8080
    
    # Lista de IPs posibles
    possible_ips = [
        "192.168.0.20",
        "192.168.1.100", 
        "192.168.1.101",
        "192.168.0.100",
        "192.168.0.101",
        "192.168.0.102"
    ]
    
    print("=== PRUEBA DE CONECTIVIDAD ===")
    
    # Probar conectividad básica
    working_ip = None
    for ip in possible_ips:
        print(f"Probando conectividad a {ip}:{port}...")
        if test_connectivity(ip, port):
            print(f"  ✅ Conectividad exitosa a {ip}")
            working_ip = ip
            break
        else:
            print(f"  ❌ Sin conectividad a {ip}")
    
    if not working_ip:
        print("\n❌ No se pudo conectar a ninguna IP")
        print("Verifica que:")
        print("1. La Pico esté ejecutando el servidor web")
        print("2. Estés en la misma red WiFi")
        print("3. La IP sea correcta")
        return
    
    print(f"\n=== PRUEBA DE APIs EN {working_ip} ===")
    
    # Lista de APIs a probar
    apis = [
        "/api/lap/status",
        "/api/led/status", 
        "/api/led/on",
        "/api/led/off",
        "/api/lap/increment",
        "/api/lap/reset"
    ]
    
    for api in apis:
        print(f"Probando {api}...")
        success, result = test_api(working_ip, port, api)
        
        if success:
            print(f"  ✅ Éxito: {result}")
        else:
            print(f"  ❌ Error: {result}")
        print()
    
    print("=== FIN DE PRUEBAS ===")

if __name__ == "__main__":
    main() 