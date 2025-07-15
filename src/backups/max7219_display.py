"""
Controlador Flexible para display MAX7219
Selecciona automáticamente entre versión single (8x8) y cascade (16x8)
según la configuración en config.py
"""

from config import MAX7219_DISPLAY_TYPE, MAX7219_DISPLAY_WIDTH

# Importar la versión correcta según la configuración
if MAX7219_DISPLAY_TYPE == "single":
    from max7219_display_single import MAX7219DisplaySingle as MAX7219Display
    print(f"Usando controlador MAX7219 Single Module (8x8)")
elif MAX7219_DISPLAY_TYPE == "cascade":
    from max7219_display_cascade import MAX7219Display as MAX7219Display
    print(f"Usando controlador MAX7219 Cascade ({MAX7219_DISPLAY_WIDTH}x8)")
else:
    raise ValueError(f"Tipo de display no válido: {MAX7219_DISPLAY_TYPE}. Use 'single' o 'cascade'")

# Re-exportar la clase para mantener compatibilidad
__all__ = ['MAX7219Display'] 