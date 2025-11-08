"""
Theme Manager - Smart City Monitoring System
Orchestrates all theme modules and provides unified interface.
"""

import streamlit as st
from typing import Optional

from config.settings import APP_CONFIG
from .anti_flash import apply_anti_flash
from .main_theme import apply_main_theme
from .dataframe import apply_dataframe_styling
from .charts import apply_chart_styling


# ============================================================================
# UNIFIED THEME APPLICATION
# ============================================================================

def apply_theme() -> None:
    """
    Apply the complete theme to the current page.
    This should be called in every page after st.set_page_config().
    
    Applies in order:
    1. Anti-flash CSS (prevents black flash) - DISABLED
    2. Main theme (global styling) - DISABLED FOR TESTING
    3. Dataframe styling - DISABLED FOR TESTING
    4. Chart styling - DISABLED FOR TESTING
    """
    # apply_anti_flash()  # DISABLED: Uncomment to re-enable anti-flash feature
    # apply_main_theme()  # DISABLED FOR TESTING: May be interfering with charts
    # apply_dataframe_styling()  # DISABLED FOR TESTING
    # apply_chart_styling()  # DISABLED FOR TESTING
    pass  # Temporarily applying NO CSS


def apply_page_config(
    page_title: Optional[str] = None,
    page_icon: Optional[str] = None,
    layout: str = "wide",
    initial_sidebar_state: str = "expanded"
) -> None:
    """
    Configure Streamlit page settings.
    
    Args:
        page_title: Title of the page (defaults to app config)
        page_icon: Icon for the page (defaults to app config)
        layout: Page layout ("wide" or "centered")
        initial_sidebar_state: Sidebar state ("expanded" or "collapsed")
    """
    st.set_page_config(
        page_title=page_title or APP_CONFIG['page_title'],
        page_icon=page_icon or APP_CONFIG['page_icon'],
        layout=layout,
        initial_sidebar_state=initial_sidebar_state
    )
