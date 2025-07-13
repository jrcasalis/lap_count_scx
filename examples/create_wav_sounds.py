"""
Script para crear archivos WAV simples de prueba
Genera sonidos básicos que deberían funcionar en cualquier navegador
"""

import wave
import struct
import math
import os

def create_beep_wav(filename, duration=0.5, frequency=800, sample_rate=44100):
    """Crea un archivo WAV con un beep simple"""
    
    # Calcular parámetros
    num_samples = int(sample_rate * duration)
    
    # Crear datos de audio (onda sinusoidal)
    audio_data = []
    for i in range(num_samples):
        # Generar onda sinusoidal
        sample = math.sin(2 * math.pi * frequency * i / sample_rate)
        # Convertir a entero de 16 bits
        sample = int(sample * 32767)
        audio_data.append(sample)
    
    # Crear archivo WAV
    with wave.open(filename, 'w') as wav_file:
        # Configurar parámetros
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        
        # Escribir datos
        for sample in audio_data:
            wav_file.writeframes(struct.pack('<h', sample))
    
    print(f"✅ Creado: {filename} ({duration}s, {frequency}Hz)")

def create_go_wav(filename, duration=1.0, frequency=600, sample_rate=44100):
    """Crea un archivo WAV con un sonido 'go' más largo"""
    
    # Calcular parámetros
    num_samples = int(sample_rate * duration)
    
    # Crear datos de audio (onda sinusoidal con fade)
    audio_data = []
    for i in range(num_samples):
        # Generar onda sinusoidal
        sample = math.sin(2 * math.pi * frequency * i / sample_rate)
        
        # Aplicar fade in/out
        fade_factor = 1.0
        if i < sample_rate * 0.1:  # Fade in en los primeros 0.1s
            fade_factor = i / (sample_rate * 0.1)
        elif i > num_samples - sample_rate * 0.1:  # Fade out en los últimos 0.1s
            fade_factor = (num_samples - i) / (sample_rate * 0.1)
        
        sample = sample * fade_factor
        
        # Convertir a entero de 16 bits
        sample = int(sample * 32767)
        audio_data.append(sample)
    
    # Crear archivo WAV
    with wave.open(filename, 'w') as wav_file:
        # Configurar parámetros
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        
        # Escribir datos
        for sample in audio_data:
            wav_file.writeframes(struct.pack('<h', sample))
    
    print(f"✅ Creado: {filename} ({duration}s, {frequency}Hz)")

def main():
    """Función principal"""
    print("🎵 === CREANDO ARCHIVOS WAV DE PRUEBA ===")
    
    # Crear directorio si no existe
    os.makedirs("web/sounds", exist_ok=True)
    
    # Crear archivos WAV
    create_beep_wav("web/sounds/beep.wav", duration=0.3, frequency=800)
    create_go_wav("web/sounds/go.wav", duration=0.8, frequency=600)
    
    print("\n📁 Archivos creados:")
    print("   - web/sounds/beep.wav (beep corto)")
    print("   - web/sounds/go.wav (sonido go)")
    
    print("\n🔧 Próximos pasos:")
    print("1. Actualizar el JavaScript para usar archivos .wav")
    print("2. Probar la reproducción con los nuevos archivos")
    print("3. Si funcionan, reemplazar los MP3 por WAV")

if __name__ == "__main__":
    main() 