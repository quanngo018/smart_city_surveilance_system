"""
Configuration Package for Smart City Monitoring System
Contains centralized settings and constants.
"""

from .settings import (
    APP_CONFIG,
    MAP_CONFIG,
    EVENT_TYPES,
    STATUS_LABELS,
    WHITE_THEME_CSS,
    DISPLAY_CONFIG,
    VALIDATION_RULES
)

__all__ = [
    'APP_CONFIG',
    'MAP_CONFIG',
    'EVENT_TYPES',
    'STATUS_LABELS',
    'WHITE_THEME_CSS',
    'DISPLAY_CONFIG',
    'VALIDATION_RULES'
]
