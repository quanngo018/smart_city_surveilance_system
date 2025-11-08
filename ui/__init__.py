"""
UI Module - Smart City Monitoring System
Centralized UI components and theme management.
"""

# ============================================================================
# THEME MANAGEMENT (from new modular structure)
# ============================================================================

# Core theme functions
from .manager import apply_theme, apply_page_config

# Individual theme modules (optional direct access)
from .anti_flash import apply_anti_flash, get_anti_flash_css
from .main_theme import apply_main_theme, get_main_theme_css
from .dataframe import apply_dataframe_styling, get_dataframe_css
from .charts import apply_chart_styling, get_chart_css, style_chart

# Color utilities
from .base import get_chart_colors, get_status_color


# ============================================================================
# UI COMPONENTS
# ============================================================================

from .components import (
    # Page structure
    render_page_header,
    render_section_header,
    render_divider,
    render_footer,
    
    # Layout
    render_columns,
    render_tabs,
    render_expander,
    
    # Data display
    render_metric_card,
    render_styled_dataframe,
    
    # Forms
    render_text_input,
    render_number_input,
    render_selectbox,
    render_button,
    
    # Messages
    render_info_box,
    render_success_box,
    render_warning_box,
    render_error_box,
)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Theme management
    'apply_theme',
    'apply_page_config',
    'apply_anti_flash',
    'apply_main_theme',
    'apply_dataframe_styling',
    'apply_chart_styling',
    
    # CSS getters
    'get_anti_flash_css',
    'get_main_theme_css',
    'get_dataframe_css',
    'get_chart_css',
    
    # Chart utilities
    'style_chart',
    'get_chart_colors',
    'get_status_color',
    
    # Page structure
    'render_page_header',
    'render_section_header',
    'render_divider',
    'render_footer',
    
    # Layout
    'render_columns',
    'render_tabs',
    'render_expander',
    
    # Data display
    'render_metric_card',
    'render_styled_dataframe',
    
    # Forms
    'render_text_input',
    'render_number_input',
    'render_selectbox',
    'render_button',
    
    # Messages
    'render_info_box',
    'render_success_box',
    'render_warning_box',
    'render_error_box',
]

