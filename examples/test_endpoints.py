import requests

BASE_URL = 'http://192.168.0.20'  # Cambia la IP si es necesario
ENDPOINTS = [
    '/',
    '/start_race',
    '/stop_race',
    '/start_previous',
    '/stop_previous',
    '/reset',
    '/api/status',
    '/favicon.ico',
    '/script.js',
]

def test_endpoint(endpoint):
    url = BASE_URL + endpoint
    print(f'\n===> Probando: {url}')
    try:
        resp = requests.get(url, timeout=5)
        print(f'Código HTTP: {resp.status_code}')
        content_type = resp.headers.get('Content-Type', '')
        print(f'Content-Type: {content_type}')
        if 'application/json' in content_type:
            try:
                print('Respuesta JSON:', resp.json())
            except Exception as e:
                print('Error decodificando JSON:', e)
                print('Texto:', resp.text)
        elif 'text/html' in content_type or 'text/plain' in content_type:
            print('Respuesta texto:', resp.text[:200], '...')
        elif 'image/x-icon' in content_type:
            print('Respuesta favicon recibida (bytes):', len(resp.content))
        elif 'application/javascript' in content_type:
            print('Respuesta JS recibida (bytes):', len(resp.content))
            print('Primeras líneas JS:', resp.text[:200], '...')
        else:
            print('Respuesta:', resp.text[:200], '...')
    except Exception as e:
        print(f'❌ Error accediendo a {url}: {e}')

if __name__ == '__main__':
    print('===> Test de endpoints del servidor MCP')
    for ep in ENDPOINTS:
        test_endpoint(ep)
    print('\n===> Prueba finalizada') 