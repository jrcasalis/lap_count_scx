#!/usr/bin/env python3
"""
Script de instalación para copiar archivos a la Raspberry Pi Pico
"""

import os
import shutil
import sys

def copy_files_to_pico():
    """Copia los archivos necesarios a la Pico"""
    
    # Lista de archivos a copiar (actualizada)
    files_to_copy = [
        ('src/main.py', 'main.py'),
        ('src/web_server.py', 'web_server.py'),
        ('src/led_controller.py', 'led_controller.py'),
        ('src/max7219_dual_display_configurable.py', 'max7219_dual_display_configurable.py'),
        ('src/race_controller.py', 'race_controller.py'),
        ('src/lap_counter.py', 'lap_counter.py'),
        ('src/config.py', 'config.py'),
        ('web/index.html', 'index.html'),
        ('web/style.css', 'style.css'),
        ('web/script.js', 'script.js'),
        # Ejemplos relevantes
        ('examples/test_checkered_flag_alternating.py', 'test_checkered_flag_alternating.py'),
        ('examples/test_checkered_flag_blink.py', 'test_checkered_flag_blink.py'),
        ('examples/test_animations.py', 'test_animations.py'),
        ('examples/test_complete_system.py', 'test_complete_system.py'),
        ('examples/test_web_integration.py', 'test_web_integration.py'),
        ('examples/test_simple_configurable.py', 'test_simple_configurable.py'),
        ('examples/test_rotation_examples.py', 'test_rotation_examples.py'),
        ('examples/test_configurable_display.py', 'test_configurable_display.py'),
        ('examples/test_racer_name.py', 'test_racer_name.py'),
        ('examples/test_racer_name_scroll.py', 'test_racer_name_scroll.py'),
        ('examples/test_web_racer_name_fixed.py', 'test_web_racer_name_fixed.py'),
    ]
    
    print("Copiando archivos a la Raspberry Pi Pico...")
    
    for source, destination in files_to_copy:
        if os.path.exists(source):
            try:
                shutil.copy2(source, destination)
                print(f"✓ Copiado: {source} → {destination}")
            except Exception as e:
                print(f"✗ Error copiando {source}: {e}")
        else:
            print(f"✗ Archivo no encontrado: {source}")
    
    print("\nInstalación completada!")
    print("\nPara probar el sistema de contador de vueltas:")
    print("1. Conecta la Pico al ordenador")
    print("2. Abre Thonny IDE")
    print("3. Para probar el sistema completo:")
    print("   exec(open('test_complete_system.py').read())")
    print("4. Para probar la animación de bandera a cuadros alternante:")
    print("   exec(open('test_checkered_flag_alternating.py').read())")
    print("5. Para probar todas las animaciones:")
    print("   exec(open('test_animations.py').read())")
    print("6. Para probar la integración web:")
    print("   exec(open('test_web_integration.py').read())")
    print("7. Para probar el nombre del piloto:")
    print("   exec(open('test_racer_name.py').read())")
    print("8. Para probar el scroll del nombre del piloto:")
    print("   exec(open('test_racer_name_scroll.py').read())")
    print("9. Para probar el nombre del piloto desde la web:")
    print("   exec(open('test_web_racer_name_fixed.py').read())")
    print("\nPara ejecutar el proyecto completo:")
    print("1. Ejecuta: exec(open('main.py').read())")

if __name__ == "__main__":
    copy_files_to_pico() 