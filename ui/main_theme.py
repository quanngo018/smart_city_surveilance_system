"""
Main Theme CSS Module - Smart City Monitoring System
Global app theming for body, sidebar, buttons, inputs, tabs, etc.
"""

import streamlit as st


# ============================================================================
# MAIN THEME CSS
# ============================================================================

MAIN_THEME_CSS = """
<style>
    /* === Global Styling === */
    
    /* Body and containers */
    html, body, #root, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .main .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        padding-top: 2rem !important;
    }
    
    .main {
        background-color: #FFFFFF !important;
    }
    
    /* === Sidebar === */
    section[data-testid="stSidebar"] {
        background-color: #f2f3f5 !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #f2f3f5 !important;
    }
    
    /* === Text Elements === */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    p, span, div, label {
        color: #000000 !important;
    }
    
    /* Markdown text */
    .stMarkdown, .stMarkdown * {
        color: #000000 !important;
    }
    
    /* === Metric Cards === */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #000000 !important;
    }
    
    div[data-testid="metric-container"] * {
        color: #000000 !important;
    }
    
    /* === Buttons === */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #333333 !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }
    
    .stButton>button:hover {
        background-color: #F0F0F0 !important;
        border-color: #000000 !important;
    }
    
    .stButton>button[kind="primary"] {
        background-color: #4CAF50 !important;
        color: #FFFFFF !important;
        border: 1px solid #4CAF50 !important;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: #45a049 !important;
    }
    
    /* === Input Fields === */
    .stSelectbox, .stMultiSelect, .stTextInput, .stNumberInput {
        background-color: #FFFFFF !important;
    }
    
    .stSelectbox > div > div, 
    .stMultiSelect > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px !important;
    }
    
    .stSelectbox label, .stMultiSelect label, .stTextInput label, .stNumberInput label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* === Dropdowns === */
    [data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    [data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }
    
    [role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    [role="option"]:hover {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
    }
    
    [aria-selected="true"] {
        background-color: #E0E0E0 !important;
        color: #000000 !important;
    }
    
    /* === Tabs === */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF !important;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #E8E8E8 !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px 4px 0 0 !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: #FFFFFF !important;
        border: 1px solid #4CAF50 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #D0D0D0 !important;
        color: #000000 !important;
    }
    
    /* === Expander === */
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 4px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
        border-top: none !important;
    }
    
    /* === Alert Boxes === */
    .stAlert {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 4px !important;
    }
    
    /* === Footer === */
    footer {
        background-color: #FFFFFF !important;
        visibility: hidden !important;
    }
    
    #MainMenu {
        visibility: hidden !important;
    }
</style>
"""


# ============================================================================
# PUBLIC FUNCTIONS
# ============================================================================

def apply_main_theme() -> None:
    """Apply main theme CSS for global app styling."""
    st.markdown(MAIN_THEME_CSS, unsafe_allow_html=True)


def get_main_theme_css() -> str:
    """
    Get main theme CSS.
    
    Returns:
        Main theme CSS string
    """
    return MAIN_THEME_CSS
