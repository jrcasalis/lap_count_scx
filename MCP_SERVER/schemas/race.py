"""
Esquemas para datos de carrera
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RaceState(str, Enum):
    """Estados posibles de una carrera"""
    STOPPED = "STOPPED"
    PREVIOUS = "PREVIOUS"
    STARTED = "STARTED"
    FINISHED = "FINISHED"

class RaceAction(str, Enum):
    """Acciones disponibles para una carrera"""
    START = "start"
    STOP = "stop"
    RESET = "reset"
    START_PREVIOUS = "start_previous"
    STOP_PREVIOUS = "stop_previous"

class RaceStatus(BaseModel):
    """Estado actual de la carrera"""
    race_state: RaceState = Field(..., description="Estado actual de la carrera")
    current_laps: int = Field(..., description="Número de vueltas actuales")
    max_laps: int = Field(..., description="Número máximo de vueltas")
    remaining_laps: int = Field(..., description="Vueltas restantes")
    progress_percentage: float = Field(..., description="Porcentaje de progreso")
    is_completed: bool = Field(..., description="Si la carrera está completada")
    racer_name: str = Field(..., description="Nombre del piloto")
    sensor_active: bool = Field(..., description="Si el sensor está activo")
    timestamp: float = Field(..., description="Timestamp de la última actualización")

class RaceConfig(BaseModel):
    """Configuración de la carrera"""
    max_laps: int = Field(default=9, description="Número máximo de vueltas")
    num_racers: int = Field(default=1, description="Número de corredores")
    racer_names: List[str] = Field(default_factory=list, description="Nombres de los corredores")
    auto_reset: bool = Field(default=True, description="Reset automático al completar")
    show_flag_animation: bool = Field(default=True, description="Mostrar animación de bandera")

class RaceActionRequest(BaseModel):
    """Solicitud de acción de carrera"""
    action: RaceAction = Field(..., description="Acción a ejecutar")
    parameters: Optional[dict] = Field(default=None, description="Parámetros adicionales")

class RaceActionResponse(BaseModel):
    """Respuesta de acción de carrera"""
    success: bool = Field(..., description="Si la acción fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    action: str = Field(..., description="Acción ejecutada")
    error: Optional[str] = Field(default=None, description="Error si ocurrió")
    data: Optional[dict] = Field(default=None, description="Datos adicionales") 