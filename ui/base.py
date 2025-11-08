"""
Base UI Module - Smart City Monitoring System
Core utilities, color palettes, and shared constants.
"""

from typing import List


# ============================================================================
# COLOR PALETTES
# ============================================================================

def get_chart_colors() -> List[str]:
    """
    Get a list of distinct, vibrant colors for charts.
    Returns colors that are clearly visible on white background.
    
    Returns:
        List of color codes (hex format)
    """
    return [
        '#EF4444',  # Red
        '#3B82F6',  # Blue
        '#F59E0B',  # Amber/Orange
        '#10B981',  # Green
        '#8B5CF6',  # Purple
        '#EC4899',  # Pink
        '#14B8A6',  # Teal
        '#F97316',  # Deep Orange
        '#6366F1',  # Indigo
        '#84CC16',  # Lime
    ]


def get_status_color(status: str) -> str:
    """
    Get color for status indicators.
    
    Args:
        status: Status string (e.g., 'online', 'offline', 'pending')
    
    Returns:
        Color code (hex format)
    """
    status_colors = {
        'online': '#10B981',      # Green
        'offline': '#EF4444',     # Red
        'pending': '#F59E0B',     # Amber
        'resolved': '#3B82F6',    # Blue
        'false_alarm': '#6B7280', # Gray
        'active': '#10B981',      # Green
        'inactive': '#EF4444',    # Red
        'warning': '#F59E0B',     # Amber
        'error': '#EF4444',       # Red
        'success': '#10B981',     # Green
        'info': '#3B82F6',        # Blue
    }
    return status_colors.get(status.lower(), '#6B7280')  # Default gray


# ============================================================================
# LAYOUT CONSTANTS
# ============================================================================

DEFAULT_CHART_HEIGHT = 400
DEFAULT_DATAFRAME_HEIGHT = 400
DEFAULT_BORDER_RADIUS = "8px"
DEFAULT_PADDING = "1rem"
