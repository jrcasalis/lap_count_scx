"""
Ejemplo básico de control de LED
Este archivo demuestra el control básico del LED sin servidor web
Útil para probar las conexiones del hardware
"""

from machine import Pin
import time

# Configuración del LED
LED_PIN = 0  # GP0
led = Pin(LED_PIN, Pin.OUT)

def blink_led(times=5, delay=0.5):
    """
    Parpadea el LED un número específico de veces
    
    Args:
        times (int): Número de parpadeos
        delay (float): Tiempo entre parpadeos en segundos
    """
    print(f"Parpadeando LED {times} veces...")
    
    for i in range(times):
        print(f"Parpadeo {i+1}/{times}")
        led.value(1)  # Encender
        time.sleep(delay)
        led.value(0)  # Apagar
        time.sleep(delay)
    
    print("Parpadeo completado")

def test_led():
    """Prueba básica del LED"""
    print("=== Prueba Básica del LED ===")
    print(f"LED conectado al pin GP{LED_PIN}")
    
    # Encender LED
    print("1. Encendiendo LED...")
    led.value(1)
    time.sleep(2)
    
    # Apagar LED
    print("2. Apagando LED...")
    led.value(0)
    time.sleep(1)
    
    # Parpadear LED
    print("3. Parpadeando LED...")
    blink_led(3, 0.3)
    
    print("=== Prueba completada ===")

def interactive_control():
    """Control interactivo del LED desde la consola"""
    print("=== Control Interactivo del LED ===")
    print("Comandos disponibles:")
    print("  'on'  - Encender LED")
    print("  'off' - Apagar LED")
    print("  'blink' - Parpadear LED")
    print("  'quit' - Salir")
    
    while True:
        try:
            command = input("Comando: ").strip().lower()
            
            if command == 'on':
                led.value(1)
                print("LED encendido")
            elif command == 'off':
                led.value(0)
                print("LED apagado")
            elif command == 'blink':
                blink_led(3, 0.2)
            elif command == 'quit':
                print("Saliendo...")
                led.value(0)  # Asegurar que LED esté apagado
                break
            else:
                print("Comando no válido. Usa: on, off, blink, quit")
                
        except KeyboardInterrupt:
            print("\nSaliendo...")
            led.value(0)
            break

if __name__ == "__main__":
    # Ejecutar prueba básica
    test_led()
    
    # Preguntar si quiere control interactivo
    try:
        response = input("\n¿Quieres control interactivo? (y/n): ").strip().lower()
        if response in ['y', 'yes', 'sí', 'si']:
            interactive_control()
    except KeyboardInterrupt:
        print("\nPrograma terminado")
        led.value(0)  # Asegurar que LED esté apagado 