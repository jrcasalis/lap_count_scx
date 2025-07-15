"""
Contador de Vueltas
Módulo para manejar el conteo de vueltas de forma modular
"""

class LapCounter:
    def __init__(self, max_laps=10):
        """
        Inicializa el contador de vueltas
        
        Args:
            max_laps (int): Número máximo de vueltas permitidas
        """
        self.current_laps = 0
        self.max_laps = max_laps
        self.is_completed = False
        
    def increment_lap(self):
        """
        Incrementa el contador de vueltas
        
        Returns:
            bool: True si se pudo incrementar, False si ya se alcanzó el máximo
        """
        if self.current_laps < self.max_laps:
            self.current_laps += 1
            if self.current_laps >= self.max_laps:
                self.is_completed = True
            return True
        return False
    
    def reset_counter(self):
        """Reinicia el contador de vueltas"""
        self.current_laps = 0
        self.is_completed = False
    
    def get_current_laps(self):
        """Retorna el número actual de vueltas"""
        return self.current_laps
    
    def get_max_laps(self):
        """Retorna el número máximo de vueltas"""
        return self.max_laps
    
    def is_race_completed(self):
        """Retorna True si la carrera está completada"""
        return self.is_completed
    
    def get_remaining_laps(self):
        """Retorna las vueltas restantes"""
        return max(0, self.max_laps - self.current_laps)
    
    def set_max_laps(self, max_laps):
        """
        Cambia el número máximo de vueltas
        
        Args:
            max_laps (int): Nuevo número máximo de vueltas
        """
        self.max_laps = max_laps
        if self.current_laps > self.max_laps:
            self.current_laps = self.max_laps
        self.is_completed = (self.current_laps >= self.max_laps)
    
    def get_status(self):
        """Retorna el estado completo del contador"""
        return {
            "current_laps": self.current_laps,
            "max_laps": self.max_laps,
            "remaining_laps": self.get_remaining_laps(),
            "is_completed": self.is_completed,
            "progress_percentage": (self.current_laps / self.max_laps) * 100 if self.max_laps > 0 else 0
        } 