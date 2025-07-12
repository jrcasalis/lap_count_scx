"""
Patrones de animaciones para display MAX7219
Patrones 8x8 para animaciones de bandera a cuadros y otras
"""

# Patrones de bandera a cuadros 2x2 (4 variaciones)
CHECKERED_FLAG_PATTERNS = [
    # Variación 1: Cuadros básicos
    [0b11001100, 0b11001100, 0b00110011, 0b00110011, 0b11001100, 0b11001100, 0b00110011, 0b00110011],
    
    # Variación 2: Cuadros invertidos
    [0b00110011, 0b00110011, 0b11001100, 0b11001100, 0b00110011, 0b00110011, 0b11001100, 0b11001100],
    
    # Variación 3: Cuadros alternados
    [0b10101010, 0b01010101, 0b10101010, 0b01010101, 0b10101010, 0b01010101, 0b10101010, 0b01010101],
    
    # Variación 4: Cuadros cruzados
    [0b10011001, 0b01100110, 0b10011001, 0b01100110, 0b10011001, 0b01100110, 0b10011001, 0b01100110]
]

# Patrones de animación pulsante
PULSE_PATTERNS = [
    [0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x3C, 0x3C, 0x3C, 0x3C, 0x00, 0x00],
    [0x00, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x00],
    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
    [0x00, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x00],
    [0x00, 0x00, 0x3C, 0x3C, 0x3C, 0x3C, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00],
]

# Patrones de animación ondulante
WAVE_PATTERNS = [
    [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80],
    [0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x01],
    [0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x01, 0x02],
    [0x08, 0x10, 0x20, 0x40, 0x80, 0x01, 0x02, 0x04],
    [0x10, 0x20, 0x40, 0x80, 0x01, 0x02, 0x04, 0x08],
    [0x20, 0x40, 0x80, 0x01, 0x02, 0x04, 0x08, 0x10],
    [0x40, 0x80, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20],
    [0x80, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40],
]

# Patrones de animación giratoria
SPINNING_PATTERNS = [
    [0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00001000, 0b00000100, 0b00000010, 0b00000001],
    [0b01000000, 0b00100000, 0b00010000, 0b00001000, 0b00000100, 0b00000010, 0b00000001, 0b10000000],
    [0b00100000, 0b00010000, 0b00001000, 0b00000100, 0b00000010, 0b00000001, 0b10000000, 0b01000000],
    [0b00010000, 0b00001000, 0b00000100, 0b00000010, 0b00000001, 0b10000000, 0b01000000, 0b00100000],
    [0b00001000, 0b00000100, 0b00000010, 0b00000001, 0b10000000, 0b01000000, 0b00100000, 0b00010000],
    [0b00000100, 0b00000010, 0b00000001, 0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00001000],
    [0b00000010, 0b00000001, 0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00001000, 0b00000100],
    [0b00000001, 0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00001000, 0b00000100, 0b00000010],
]

def get_checkered_flag_pattern(variation=0):
    """Obtiene un patrón de bandera a cuadros específico"""
    return CHECKERED_FLAG_PATTERNS[variation % len(CHECKERED_FLAG_PATTERNS)]

def get_pulse_patterns():
    """Obtiene todos los patrones de pulsación"""
    return PULSE_PATTERNS

def get_wave_patterns():
    """Obtiene todos los patrones de onda"""
    return WAVE_PATTERNS

def get_spinning_patterns():
    """Obtiene todos los patrones de giro"""
    return SPINNING_PATTERNS

def get_animation_patterns(animation_type):
    """Obtiene patrones según el tipo de animación"""
    patterns = {
        'checkered': CHECKERED_FLAG_PATTERNS,
        'pulse': PULSE_PATTERNS,
        'wave': WAVE_PATTERNS,
        'spinning': SPINNING_PATTERNS
    }
    return patterns.get(animation_type, []) 