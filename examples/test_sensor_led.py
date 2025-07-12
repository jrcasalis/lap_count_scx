from machine import Pin
import utime

LED_PIN = 0  # GP0 (ajusta si usas otro)
SENSOR_PIN = 16  # GP16 (ajusta si usas otro)

led = Pin(LED_PIN, Pin.OUT)
sensor = Pin(SENSOR_PIN, Pin.IN)

print("Prueba de sensor TCRT5000 y LED rojo")
print("Acerca un objeto al sensor para encender el LED por 5 segundos.")

last_sensor_state = sensor.value()
led_timer = 0

while True:
    current_sensor_state = sensor.value()
    # Detectar flanco descendente (detección de objeto)
    if last_sensor_state == 1 and current_sensor_state == 0:
        print("[TCRT5000] Detección de objeto - Encendiendo LED rojo por 5 segundos")
        led.value(1)
        led_timer = utime.ticks_ms()
    # Apagar LED después de 5 segundos
    if led.value() == 1 and led_timer and utime.ticks_diff(utime.ticks_ms(), led_timer) > 5000:
        led.value(0)
        led_timer = 0
    last_sensor_state = current_sensor_state
    utime.sleep(0.01) 