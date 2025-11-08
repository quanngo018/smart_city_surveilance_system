"""
Anti-Flash CSS Module - Smart City Monitoring System
Prevents black flash on page load/transition while allowing Plotly charts to render properly.
"""

import streamlit as st


# ============================================================================
# ANTI-FLASH CSS
# ============================================================================

ANTI_FLASH_CSS = """
<style>
    /* CRITICAL: Prevent black flash on page load/transition */
    html, body { 
        background-color: #FFFFFF !important; 
        margin: 0 !important;
        padding: 0 !important;
    }
    
    * { 
        transition: none !important;
        animation-duration: 0s !important;
    }
    
    [data-testid="stAppViewContainer"],
    .main,
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Remove black top bar */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    [data-testid="stToolbar"] {
        background-color: #FFFFFF !important;
    }
    
    /* EXCLUDE: Allow Plotly charts to render with their native SVG */
    .js-plotly-plot,
    .js-plotly-plot svg,
    .js-plotly-plot g,
    .js-plotly-plot rect,
    .js-plotly-plot path,
    .js-plotly-plot text {
        background-color: auto !important;
        color: auto !important;
    }
</style>
"""


# ============================================================================
# PUBLIC FUNCTIONS
# ============================================================================

def apply_anti_flash() -> None:
    """Apply anti-flash CSS to prevent page flashing."""
    st.markdown(ANTI_FLASH_CSS, unsafe_allow_html=True)


def get_anti_flash_css() -> str:
    """
    Get CSS to prevent page flash on load.
    
    Returns:
        Anti-flash CSS string
    """
    return ANTI_FLASH_CSS
