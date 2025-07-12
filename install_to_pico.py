#!/usr/bin/env python3
"""
Script de instalación para copiar archivos a la Raspberry Pi Pico
"""

import os
import shutil
import sys

def copy_files_to_pico():
    """Copia los archivos necesarios a la Pico"""
    
    # Lista de archivos a copiar
    files_to_copy = [
        ('src/main.py', 'main.py'),
        ('src/web_server.py', 'web_server.py'),
        ('src/led_controller.py', 'led_controller.py'),
        ('src/max7219_display.py', 'max7219_display.py'),
        ('src/config.py', 'config.py'),
        ('web/index.html', 'index.html'),
        ('web/style.css', 'style.css'),
        ('web/script.js', 'script.js'),
        ('examples/test_max7219_simple.py', 'test_max7219_simple.py'),
        ('examples/test_max7219_alternative.py', 'test_max7219_alternative.py')
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
    print("\nPara probar el display MAX7219:")
    print("1. Conecta la Pico al ordenador")
    print("2. Abre Thonny IDE")
    print("3. Si el primer test falla, prueba:")
    print("   exec(open('test_max7219_alternative.py').read())")
    print("4. O el test simple:")
    print("   exec(open('test_max7219_simple.py').read())")
    print("\nPara ejecutar el proyecto completo:")
    print("1. Ejecuta: exec(open('main.py').read())")

if __name__ == "__main__":
    copy_files_to_pico() 