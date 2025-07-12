from machine import Pin
import utime

SENSOR_PIN = 16  # GP16 (ajusta si usas otro)

sensor = Pin(SENSOR_PIN, Pin.IN)

print("Prueba SOLO del sensor TCRT5000")
print("Muestra el valor leído en el pin cada 0.2 segundos.")

while True:
    valor = sensor.value()
    print(f"Valor sensor (GP{SENSOR_PIN}):", valor)
    utime.sleep(0.2) 