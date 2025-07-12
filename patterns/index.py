"""
Índice central de patrones para display MAX7219
Exporta todos los patrones de manera organizada
"""

# Importar todos los patrones
from .digits import DIGITS, get_digit_pattern, get_two_digits_pattern
from .letters import LETTERS, get_letter_pattern, get_word_pattern, get_available_letters, get_letter_info
from .various import (
    HELMET, HELMET_SIMPLE, HELMET_EMPTY, HEART, STAR, ARROW_UP, ARROW_DOWN,
    ARROW_RIGHT, ARROW_LEFT, CHECK, X_MARK, CIRCLE, SQUARE, TRIANGLE,
    get_helmet_pattern, get_various_pattern, get_available_patterns
)
from .animations import (
    CHECKERED_FLAG_PATTERNS, PULSE_PATTERNS, WAVE_PATTERNS, SPINNING_PATTERNS,
    get_checkered_flag_pattern, get_pulse_patterns, get_wave_patterns, 
    get_spinning_patterns, get_animation_patterns
)

# Exportar todo de manera centralizada
__all__ = [
    # Dígitos
    'DIGITS',
    'get_digit_pattern',
    'get_two_digits_pattern',
    
    # Letras
    'LETTERS',
    'get_letter_pattern',
    'get_word_pattern',
    'get_available_letters',
    'get_letter_info',
    
    # Varios (cascos, símbolos, flechas, formas)
    'HELMET',
    'HELMET_SIMPLE', 
    'HELMET_EMPTY',
    'HEART',
    'STAR',
    'ARROW_UP',
    'ARROW_DOWN',
    'ARROW_RIGHT',
    'ARROW_LEFT',
    'CHECK',
    'X_MARK',
    'CIRCLE',
    'SQUARE',
    'TRIANGLE',
    'get_helmet_pattern',
    'get_various_pattern',
    'get_available_patterns',
    
    # Animaciones
    'CHECKERED_FLAG_PATTERNS',
    'PULSE_PATTERNS',
    'WAVE_PATTERNS', 
    'SPINNING_PATTERNS',
    'get_checkered_flag_pattern',
    'get_pulse_patterns',
    'get_wave_patterns',
    'get_spinning_patterns',
    'get_animation_patterns'
]

# Diccionario de todos los patrones disponibles
ALL_PATTERNS = {
    'digits': DIGITS,
    'letters': LETTERS,
    'helmet': HELMET,
    'helmet_simple': HELMET_SIMPLE,
    'helmet_empty': HELMET_EMPTY,
    'heart': HEART,
    'star': STAR,
    'arrow_up': ARROW_UP,
    'arrow_down': ARROW_DOWN,
    'arrow_right': ARROW_RIGHT,
    'arrow_left': ARROW_LEFT,
    'check': CHECK,
    'x_mark': X_MARK,
    'circle': CIRCLE,
    'square': SQUARE,
    'triangle': TRIANGLE,
    'checkered_flag': CHECKERED_FLAG_PATTERNS,
    'pulse': PULSE_PATTERNS,
    'wave': WAVE_PATTERNS,
    'spinning': SPINNING_PATTERNS
}

def get_pattern(pattern_type, **kwargs):
    """Función centralizada para obtener cualquier patrón"""
    if pattern_type == 'digit':
        return get_digit_pattern(kwargs.get('digit', '0'))
    elif pattern_type == 'two_digits':
        return get_two_digits_pattern(kwargs.get('value', 0))
    elif pattern_type == 'letter':
        return get_letter_pattern(kwargs.get('letter', 'A'))
    elif pattern_type == 'word':
        return get_word_pattern(kwargs.get('word', 'AB'), kwargs.get('max_length', 2))
    elif pattern_type == 'helmet':
        return get_helmet_pattern(kwargs.get('helmet_type', 'default'))
    elif pattern_type == 'various':
        return get_various_pattern(kwargs.get('pattern_name', 'helmet'))
    elif pattern_type == 'animation':
        return get_animation_patterns(kwargs.get('animation_type', 'checkered'))
    else:
        return ALL_PATTERNS.get(pattern_type, []) 