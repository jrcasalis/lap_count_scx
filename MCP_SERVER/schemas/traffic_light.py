"""
Esquemas para datos del semáforo LED
"""

from typing import Optional
from enum import Enum

class TrafficLightState(str, Enum):
    """Estados del semáforo"""
    OFF = "off"
    BLINKING = "blinking"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

class TrafficLightStatus:
    """Estado del semáforo LED"""
    def __init__(self,
                 current_state: TrafficLightState = TrafficLightState.OFF,
                 red_pin: int = 11,
                 yellow_pin: int = 12,
                 green_pin: int = 13,
                 is_connected: bool = True,
                 blink_interval: float = 0.5,
                 pwm_freq: int = 1000,
                 duty_on: int = 1023,
                 duty_off: int = 0):
        self.current_state = current_state
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin
        self.is_connected = is_connected
        self.blink_interval = blink_interval
        self.pwm_freq = pwm_freq
        self.duty_on = duty_on
        self.duty_off = duty_off

class TrafficLightConfig:
    """Configuración del semáforo"""
    def __init__(self,
                 red_pin: int = 11,
                 yellow_pin: int = 12,
                 green_pin: int = 13,
                 blink_interval: float = 0.5,
                 red_duration: float = 3.0,
                 yellow_duration: float = 3.0,
                 green_duration: float = 0,
                 pwm_freq: int = 1000,
                 duty_on: int = 1023,
                 duty_off: int = 0,
                 voltage_compensation: bool = True):
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin
        self.blink_interval = blink_interval
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration
        self.pwm_freq = pwm_freq
        self.duty_on = duty_on
        self.duty_off = duty_off
        self.voltage_compensation = voltage_compensation 