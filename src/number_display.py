"""
Display de Números para MAX7219
Módulo para mostrar números en el display de forma modular
"""

class NumberDisplay:
    def __init__(self, max7219_display):
        """
        Inicializa el display de números
        
        Args:
            max7219_display: Instancia del display MAX7219
        """
        self.display = max7219_display
        
        # Patrones para números del 0 al 9
        self.number_patterns = {
            '0': [
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b11000011,  # ██    ██
                0b11000011,  # ██    ██
                0b11000011,  # ██    ██
                0b11000011,  # ██    ██
                0b01100110,  #  ██  ██
                0b00111100   #   ████
            ],
            '1': [
                0b00011000,  #    ██
                0b00111000,  #   ███
                0b00011000,  #    ██
                0b00011000,  #    ██
                0b00011000,  #    ██
                0b00011000,  #    ██
                0b00011000,  #    ██
                0b01111110   #  ██████
            ],
            '2': [
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b00000110,  #      ██
                0b00001100,  #     ██
                0b00011000,  #    ██
                0b00110000,  #   ██
                0b01100000,  #  ██
                0b01111110   #  ██████
            ],
            '3': [
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b00000110,  #      ██
                0b00111100,  #   ████
                0b00000110,  #      ██
                0b00000110,  #      ██
                0b01100110,  #  ██  ██
                0b00111100   #   ████
            ],
            '4': [
                0b00001100,  #     ██
                0b00011100,  #    ███
                0b00111100,  #   ████
                0b01101100,  #  ██ ██
                0b01111110,  #  ██████
                0b00001100,  #     ██
                0b00001100,  #     ██
                0b00001100   #     ██
            ],
            '5': [
                0b01111110,  #  ██████
                0b01100000,  #  ██
                0b01100000,  #  ██
                0b01111100,  #  ██████
                0b00000110,  #      ██
                0b00000110,  #      ██
                0b01100110,  #  ██  ██
                0b00111100   #   ████
            ],
            '6': [
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b01100000,  #  ██
                0b01111100,  #  ██████
                0b01100110,  #  ██  ██
                0b01100110,  #  ██  ██
                0b01100110,  #  ██  ██
                0b00111100   #   ████
            ],
            '7': [
                0b01111110,  #  ██████
                0b00000110,  #      ██
                0b00001100,  #     ██
                0b00011000,  #    ██
                0b00110000,  #   ██
                0b01100000,  #  ██
                0b01100000,  #  ██
                0b01100000   #  ██
            ],
            '8': [
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b01100110,  #  ██  ██
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b01100110,  #  ██  ██
                0b01100110,  #  ██  ██
                0b00111100   #   ████
            ],
            '9': [
                0b00111100,  #   ████
                0b01100110,  #  ██  ██
                0b01100110,  #  ██  ██
                0b00111110,  #   ██████
                0b00000110,  #      ██
                0b00000110,  #      ██
                0b01100110,  #  ██  ██
                0b00111100   #   ████
            ]
        }
    
    def display_number(self, number):
        """
        Muestra un número en el display
        
        Args:
            number (int): Número a mostrar (0-99)
        """
        if number < 0 or number > 99:
            print(f"Número fuera de rango: {number}")
            return
        
        # Convertir número a string y rellenar con ceros manualmente
        number_str = str(number)
        if len(number_str) == 1:
            number_str = "0" + number_str  # Rellenar con cero a la izquierda
        
        # Mostrar dígitos uno por uno
        for i, digit in enumerate(number_str):
            if digit in self.number_patterns:
                self.display.display_letter(digit)
                # Pequeña pausa entre dígitos
                import time
                time.sleep(0.5)
    
    def display_lap_count(self, current_lap, max_laps):
        """
        Muestra el conteo de vueltas en formato "X/Y"
        
        Args:
            current_lap (int): Vuelta actual
            max_laps (int): Número máximo de vueltas
        """
        # Mostrar formato "X/Y" o solo "X" si es una sola vuelta
        if max_laps == 1:
            self.display_number(current_lap)
        else:
            # Mostrar "X/Y" de forma secuencial
            self.display_number(current_lap)
            import time
            time.sleep(0.3)
            # Mostrar "/" como separador
            self.display.display_letter('/')
            time.sleep(0.3)
            self.display_number(max_laps)
    
    def display_progress(self, current_lap, max_laps):
        """
        Muestra el progreso de la carrera
        
        Args:
            current_lap (int): Vuelta actual
            max_laps (int): Número máximo de vueltas
        """
        if current_lap == 0:
            # Mostrar "0" al inicio
            self.display_number(0)
        elif current_lap >= max_laps:
            # Mostrar "FIN" cuando se complete
            self.display.scroll_text('FIN')
        else:
            # Mostrar número de vuelta actual
            self.display_number(current_lap) 

    def scroll_number(self, number, delay=0.08):
        """
        Muestra un número con animación de scroll rápido y lo deja fijo al final
        Args:
            number (int): Número a mostrar (0-99)
            delay (float): Tiempo entre pasos de scroll
        """
        number_str = str(number)
        if len(number_str) == 1:
            number_str = "0" + number_str
        self.display.scroll_text(number_str, delay=delay)
        # Al terminar el scroll, dejar el número fijo
        self.display_number(number) 

    def scroll_number_horizontal(self, prev_number, new_number, delay=0.08):
        """
        Hace scroll lateral del número anterior al nuevo y deja el nuevo número fijo.
        Args:
            prev_number (int): Número anterior
            new_number (int): Nuevo número
            delay (float): Tiempo entre pasos de scroll
        """
        prev_str = str(prev_number)
        new_str = str(new_number)
        def get_columns(digit):
            pattern = self.number_patterns[digit]
            columns = []
            for col in range(8):
                col_val = 0
                for row in range(8):
                    if (pattern[row] >> (7-col)) & 1:
                        col_val |= (1 << (7-row))
                columns.append(col_val)
            return columns
        prev_cols = []
        for d in prev_str:
            prev_cols += get_columns(d)
        new_cols = []
        for d in new_str:
            new_cols += get_columns(d)
        total_cols = prev_cols + new_cols
        steps = len(prev_cols)
        for i in range(steps+1):
            window = total_cols[i:i+8]
            if len(window) < 8:
                window += new_cols[len(window)-8:]
            for row in range(8):
                row_val = 0
                for col in range(8):
                    if (window[col] >> (7-row)) & 1:
                        row_val |= (1 << (7-col))
                self.display.write_register(row+1, row_val)
            import time
            time.sleep(delay)
        # Ya no se llama a self.display_number(new_number) para evitar parpadeo 