"""
Controlador de Carrera - Raspberry Pi Pico 2W
Menú interactivo para controlar la carrera desde consola
"""

import network
import time
from machine import Pin
from race_controller import RaceController
from config import *

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
        print("✅ WiFi conectado!")
        print(f"📡 Dirección IP: {wlan.ifconfig()[0]}")
        return wlan.ifconfig()[0]
    else:
        print("❌ Error al conectar WiFi")
        return None

def show_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("🏁 CONTROLADOR DE CARRERA - MENÚ PRINCIPAL")
    print("="*50)
    print("1. 📊 Mostrar estado actual")
    print("2. 🏁 Iniciar carrera")
    print("3. 🛑 Parar carrera")
    print("4. ⚠️ Iniciar previa (titileo)")
    print("5. ⏹️ Parar previa")
    print("6. 🔄 Reiniciar carrera")
    print("7. 🏎️ Cambiar nombre del piloto")
    print("8. 📺 Mostrar nombre en display")
    print("9. 🔴 Controlar LED")
    print("10. 💡 Controlar titileo del display")
    print("0. ❌ Salir")
    print("="*50)

def show_status():
    """Muestra el estado actual de la carrera"""
    params = RaceController.get_race_params()
    
    print("\n📊 ESTADO ACTUAL:")
    print("-" * 30)
    print(f"🏁 Vueltas: {params['current_laps']}/{params['max_laps']}")
    print(f"🏎️ Pilotos: {params['racer_names']}")
    print(f"🚦 Estado: {params['race_state']}")
    
    # Estado del semáforo
    if RaceController.traffic_light:
        traffic_status = RaceController.traffic_light.get_status()
        print(f"🚦 Semáforo: {traffic_status['state']}")
    
    # Estado del titileo del display
    blink_status = RaceController.get_stopped_blink_status()
    print(f"💡 Titileo display: {'💡 Habilitado' if blink_status else '⚪ Deshabilitado'}")

def start_race():
    """Inicia la carrera"""
    print("\n🏁 INICIANDO CARRERA...")
    
    # Iniciar previa primero si no está activa
    if RaceController.traffic_light:
        traffic_status = RaceController.traffic_light.get_status()
        if traffic_status['state'] == 'off':
            print("⚠️ Iniciando previa primero...")
            RaceController.start_race_previous()
            time.sleep(2)
    
    # Iniciar secuencia de countdown (roja -> amarilla -> verde)
    print("🚦 Iniciando countdown...")
    success = RaceController.start_race()
    if success:
        print("✅ Countdown iniciado!")
        print("🔴 Luz roja → 🟡 Luz amarilla → 🟢 Luz verde")
        print("🏎️ La carrera se iniciará automáticamente cuando se encienda la luz verde")
    else:
        print("❌ Error al iniciar countdown")

def stop_race():
    """Para la carrera"""
    print("\n🛑 PARANDO CARRERA...")
    
    # Parar semáforos
    RaceController.stop_race()
    print("✅ Semáforos apagados")
    
    print("✅ Carrera detenida exitosamente!")
    print("🏎️ El sensor ya no cuenta vueltas")

def start_previous():
    """Inicia la previa (titileo)"""
    print("\n⚠️ INICIANDO PREVIA...")
    
    success = RaceController.start_race_previous()
    if success:
        print("✅ Previa iniciada!")
        print("🚦 Todas las luces del semáforo titilan")
    else:
        print("❌ Error al iniciar previa")

def stop_previous():
    """Para la previa"""
    print("\n⏹️ PARANDO PREVIA...")
    
    success = RaceController.stop_race_previous()
    if success:
        print("✅ Previa detenida!")
        print("🚦 Semáforos apagados")
    else:
        print("❌ Error al detener previa")

def reset_race():
    """Reinicia la carrera"""
    print("\n🔄 REINICIANDO CARRERA...")
    
    # Parar todo primero
    RaceController.stop_race()
    
    # Reiniciar parámetros
    RaceController.__init__(max_laps=RACE_MAX_LAPS, num_racers=1, racer_names=["Piloto 1"])
    print("✅ Carrera reiniciada!")
    print("🏁 Contador en 0, listo para nueva carrera")

def change_racer_name():
    """Cambia el nombre del piloto"""
    print("\n🏎️ CAMBIAR NOMBRE DEL PILOTO")
    print("-" * 30)
    
    params = RaceController.get_race_params()
    current_name = params['racer_names'][0]
    print(f"Nombre actual: {current_name}")
    
    new_name = input("Nuevo nombre (máx 10 caracteres): ").strip()
    
    if new_name:
        if len(new_name) <= 10:
            # Actualizar el nombre en los parámetros
            RaceController.racer_names[0] = new_name
            print(f"✅ Nombre cambiado a: {new_name}")
        else:
            print("❌ Nombre demasiado largo (máximo 10 caracteres)")
    else:
        print("❌ Nombre vacío")

def display_racer_name():
    """Muestra el nombre del piloto en el display"""
    print("\n📺 MOSTRANDO NOMBRE EN DISPLAY...")
    
    params = RaceController.get_race_params()
    racer_name = params['racer_names'][0]
    print(f"🏎️ Mostrando: {racer_name}")
    
    # Mostrar en display usando el método del display
    if RaceController.display:
        RaceController.display.show_racer_name_fast(racer_name)
    print("✅ Nombre mostrado en display")

def control_led():
    """Controla el LED"""
    print("\n🔴 CONTROL DE LED")
    print("-" * 20)
    print("1. 🔴 Encender LED")
    print("2. ⚪ Apagar LED")
    print("3. 🔄 Alternar LED")
    print("4. 📊 Estado del LED")
    print("0. ↩️ Volver")
    
    choice = input("Opción: ").strip()
    
    if choice == "1":
        print("✅ LED encendido (función no implementada)")
    elif choice == "2":
        print("✅ LED apagado (función no implementada)")
    elif choice == "3":
        print("✅ LED alternado (función no implementada)")
    elif choice == "4":
        print("💡 Estado del LED: No implementado")
    elif choice == "0":
        return
    else:
        print("❌ Opción inválida")

def control_display_blink():
    """Controla el titileo del display"""
    print("\n💡 CONTROL DE TITILEO DEL DISPLAY")
    print("-" * 35)
    print("1. 💡 Habilitar titileo en STOPPED")
    print("2. ⚪ Deshabilitar titileo en STOPPED")
    print("3. 🔄 Alternar titileo")
    print("4. 📊 Estado del titileo")
    print("0. ↩️ Volver")
    
    choice = input("Opción: ").strip()
    
    if choice == "1":
        RaceController.set_stopped_blink(True)
        print("✅ Titileo habilitado")
    elif choice == "2":
        RaceController.set_stopped_blink(False)
        print("✅ Titileo deshabilitado")
    elif choice == "3":
        current_status = RaceController.get_stopped_blink_status()
        RaceController.set_stopped_blink(not current_status)
        new_status = RaceController.get_stopped_blink_status()
        status = "habilitado" if new_status else "deshabilitado"
        print(f"✅ Titileo alternado: {status}")
    elif choice == "4":
        status = RaceController.get_stopped_blink_status()
        status_text = "💡 Habilitado" if status else "⚪ Deshabilitado"
        print(f"📊 Estado del titileo: {status_text}")
    elif choice == "0":
        return
    else:
        print("❌ Opción inválida")

def main():
    """Función principal con menú interactivo"""
    print("🚀 Iniciando Controlador de Carrera...")
    
    # Inicializar controlador de carrera (usando métodos de clase)
    RaceController.__init__(max_laps=RACE_MAX_LAPS, num_racers=1, racer_names=["Piloto 1"])
    
    # Inicializar sensor TCRT5000
    sensor = Pin(SENSOR_TCRT5000_PIN, Pin.IN, Pin.PULL_UP)
    last_sensor_state = sensor.value()
    
    # Conectar WiFi
    ip_address = connect_wifi()
    if not ip_address:
        print("⚠️ No se pudo conectar a WiFi. Ejecutando en modo local...")
        ip_address = "192.168.1.100"
    
    print(f"🌐 Servidor disponible en: http://{ip_address}:{SERVER_PORT}")
    print("🎮 Usa el menú para controlar la carrera")
    
    try:
        while True:
            # Actualizar el estado del controlador (POLLING) - CRÍTICO para que funcionen los parpadeos
            RaceController.update()
            
            # Manejar sensor en segundo plano
            current_sensor_state = sensor.value()
            if last_sensor_state == 1 and current_sensor_state == 0:
                params = RaceController.get_race_params()
                if params['race_state'] == 'STARTED':
                    # Incrementar vuelta del primer corredor
                    RaceController.current_laps[0] += 1
                    print(f"🏁 ¡Vuelta detectada! {RaceController.current_laps[0]}/{RaceController.max_laps}")
            last_sensor_state = current_sensor_state
            
            # Mostrar menú
            show_menu()
            
            # Obtener opción del usuario
            choice = input("Selecciona una opción: ").strip()
            
            if choice == "1":
                show_status()
            elif choice == "2":
                start_race()
            elif choice == "3":
                stop_race()
            elif choice == "4":
                start_previous()
            elif choice == "5":
                stop_previous()
            elif choice == "6":
                reset_race()
            elif choice == "7":
                change_racer_name()
            elif choice == "8":
                display_racer_name()
            elif choice == "9":
                control_led()
            elif choice == "10":
                control_display_blink()
            elif choice == "0":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Intenta de nuevo.")
            
            # Pausa para leer
            input("\nPresiona Enter para continuar...")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo servidor...")
        race_controller.cleanup()
        print("✅ Servidor detenido")

if __name__ == "__main__":
    main() 