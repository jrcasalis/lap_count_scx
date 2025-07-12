"""
Patrones varios para display MAX7219
Patrones 8x8 para diferentes dibujos e iconos
"""

# Patrón de casco principal
HELMET = [
    0b00111100,
    0b01111110,
    0b11111111,
    0b11100000,
    0b11110000,
    0b11111000,
    0b01111111,
    0b00111111
]

# Patrón de casco alternativo (más simple)
HELMET_SIMPLE = [
    0b00011000,
    0b00111100,
    0b01111110,
    0b01111110,
    0b01111110,
    0b00111100,
    0b00111100,
    0b00000000
]

# Patrón de casco vacío (para testing)
HELMET_EMPTY = [
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000
]

# Patrón de corazón
HEART = [
    0b01100110,
    0b11111111,
    0b11111111,
    0b11111111,
    0b01111110,
    0b00111100,
    0b00011000,
    0b00000000
]

# Patrón de estrella
STAR = [
    0b00011000,
    0b00011000,
    0b11111111,
    0b01111110,
    0b11111111,
    0b00011000,
    0b00011000,
    0b00000000
]

# Patrón de flecha hacia arriba
ARROW_UP = [
    0b00011000,
    0b00111100,
    0b01111110,
    0b11111111,
    0b00011000,
    0b00011000,
    0b00011000,
    0b00000000
]

# Patrón de flecha hacia abajo
ARROW_DOWN = [
    0b00011000,
    0b00011000,
    0b00011000,
    0b11111111,
    0b01111110,
    0b00111100,
    0b00011000,
    0b00000000
]

# Patrón de flecha hacia la derecha
ARROW_RIGHT = [
    0b00000000,
    0b00010000,
    0b00110000,
    0b11111111,
    0b11111111,
    0b00110000,
    0b00010000,
    0b00000000
]

# Patrón de flecha hacia la izquierda
ARROW_LEFT = [
    0b00000000,
    0b00001000,
    0b00001100,
    0b11111111,
    0b11111111,
    0b00001100,
    0b00001000,
    0b00000000
]

# Patrón de check (✓)
CHECK = [
    0b00000000,
    0b00000001,
    0b00000010,
    0b00000100,
    0b10001000,
    0b01010000,
    0b00100000,
    0b00000000
]

# Patrón de X
X_MARK = [
    0b10000001,
    0b01000010,
    0b00100100,
    0b00011000,
    0b00011000,
    0b00100100,
    0b01000010,
    0b10000001
]

# Patrón de círculo
CIRCLE = [
    0b00111100,
    0b01100110,
    0b11000011,
    0b11000011,
    0b11000011,
    0b11000011,
    0b01100110,
    0b00111100
]

# Patrón de cuadrado
SQUARE = [
    0b11111111,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b10000001,
    0b11111111
]

# Patrón de triángulo
TRIANGLE = [
    0b00011000,
    0b00111100,
    0b01111110,
    0b11111111,
    0b00000000,
    0b00000000,
    0b00000000,
    0b00000000
]

def get_helmet_pattern(helmet_type='default'):
    """Obtiene el patrón de casco según el tipo especificado"""
    patterns = {
        'default': HELMET,
        'simple': HELMET_SIMPLE,
        'empty': HELMET_EMPTY
    }
    return patterns.get(helmet_type, HELMET)

def get_various_pattern(pattern_name):
    """Obtiene cualquier patrón disponible por nombre"""
    patterns = {
        # Cascos
        'helmet': HELMET,
        'helmet_simple': HELMET_SIMPLE,
        'helmet_empty': HELMET_EMPTY,
        
        # Símbolos
        'heart': HEART,
        'star': STAR,
        'check': CHECK,
        'x_mark': X_MARK,
        
        # Flechas
        'arrow_up': ARROW_UP,
        'arrow_down': ARROW_DOWN,
        'arrow_right': ARROW_RIGHT,
        'arrow_left': ARROW_LEFT,
        
        # Formas geométricas
        'circle': CIRCLE,
        'square': SQUARE,
        'triangle': TRIANGLE,
    }
    return patterns.get(pattern_name, HELMET_EMPTY)

def get_available_patterns():
    """Retorna la lista de todos los patrones disponibles"""
    return [
        'helmet', 'helmet_simple', 'helmet_empty',
        'heart', 'star', 'check', 'x_mark',
        'arrow_up', 'arrow_down', 'arrow_right', 'arrow_left',
        'circle', 'square', 'triangle'
    ] 