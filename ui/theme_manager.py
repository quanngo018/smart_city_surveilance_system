"""
Theme Manager - Smart City Monitoring System
Centralized theme and CSS management for consistent UI across all pages.
"""

import streamlit as st
from typing import Optional
from config.settings import APP_CONFIG, THEME_CONFIG


# ============================================================================
# ANTI-FLASH CSS - Apply immediately to prevent page flashing
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
# DATAFRAME/TABLE CSS
# ============================================================================

DATAFRAME_CSS = """
<style>
    /* === Robust DataFrame/Table Styling === */
    [data-testid="stDataFrame"] {
        background-color: unset !important;
        border: 2px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }

    /* Force black text for all dataframe content */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] *,
    [data-testid="stDataFrame"] span,
    [data-testid="stDataFrame"] div,
    [data-testid="stDataFrame"] p {
        color: #000000 !important;
    }

    /* Table elements - white background with black text */
    [data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    [data-testid="stDataFrame"] thead,
    [data-testid="stDataFrame"] tbody,
    [data-testid="stDataFrame"] tr {
        background-color: transparent !important;
        color: #000000 !important;
    }
    
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] td {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e5e7eb !important;
        padding: 8px !important;
    }

    /* Header styling - light gray background with black text */
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] thead th {
        background-color: #f3f4f6 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #d1d5db !important;
    }

    /* Grid cells (for AG Grid) - ensure black text */
    [data-testid="stDataFrame"] div[role="gridcell"],
    [data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e5e7eb !important;
    }
    
    [data-testid="stDataFrame"] div[role="row"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Zebra striping for better readability */
    [data-testid="stDataFrame"] table tbody tr:nth-child(even) td {
        background-color: #f9fafb !important;
    }
    
    [data-testid="stDataFrame"] table tbody tr:nth-child(odd) td {
        background-color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] div[role="row"]:nth-child(even) div[role="gridcell"] {
        background-color: #f9fafb !important;
    }
    
    /* Hover effect */
    [data-testid="stDataFrame"] table tbody tr:hover td {
        background-color: #f0f9ff !important;
    }
</style>
"""


# ============================================================================
# CHART/PLOTLY CSS
# ============================================================================

CHART_CSS = """
<style>
    /* === Chart and Plotly Styling === */
    
    /* Plotly charts - white background for contrast */
    .js-plotly-plot, .plotly {
        background-color: #ffffff !important;
    }
    
    .js-plotly-plot .plotly .svg-container {
        background-color: #ffffff !important;
    }
    
    .js-plotly-plot .plotly .main-svg {
        background-color: #ffffff !important;
    }
    
    /* Force ALL chart text to be black - EXCEPT pie chart slice labels */
    .js-plotly-plot text,
    .js-plotly-plot .plotly text,
    .plotly text,
    text.plotly {
        fill: #000000 !important;
        color: #000000 !important;
    }
    
    /* Pie chart slice text can be white for visibility on colored slices */
    .js-plotly-plot .slice text,
    .slice text {
        fill: inherit !important;
        color: inherit !important;
    }
    
    /* Chart titles - bold black */
    .gtitle, .g-gtitle {
        fill: #000000 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* Axis titles - bold black */
    .g-xtitle, .g-ytitle {
        fill: #000000 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Axis tick labels - black */
    .xtick text, .ytick text {
        fill: #000000 !important;
        font-size: 12px !important;
    }
    
    /* Legend text - black */
    .legend text {
        fill: #000000 !important;
    }
    
    /* Annotation text - black */
    .annotation-text {
        fill: #000000 !important;
    }
    
    /* Plotly modebar (toolbar) */
    .modebar {
        background-color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .modebar-btn svg {
        fill: #000000 !important;
    }
    
    /* Grid lines - light gray for visibility */
    .gridlayer .x, .gridlayer .y {
        stroke: #e5e7eb !important;
    }
    
    /* Default plotly color scheme for data (colorful but readable) */
    /* These will be overridden by explicit color specifications in code */
    .trace {
        stroke-width: 2px !important;
    }
    
    /* Ensure bars, lines, and markers are visible */
    .point, .scatter .point {
        opacity: 1 !important;
    }
    
    .bar, .bars .bar {
        opacity: 1 !important;
    }
    
    path.line {
        opacity: 1 !important;
    }
    
    /* Plotly SVG containers - must allow native rendering */
    .js-plotly-plot .svg-container,
    .js-plotly-plot .main-svg,
    .js-plotly-plot svg rect[class*="bg"] {
        background-color: transparent !important;
    }
</style>
"""


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

def get_anti_flash_css() -> str:
    """Get CSS to prevent page flash on load."""
    return ANTI_FLASH_CSS


def get_dataframe_css() -> str:
    """Get CSS for styling dataframes/tables."""
    return DATAFRAME_CSS


def get_chart_css() -> str:
    """Get CSS for styling charts and plotly graphs."""
    return CHART_CSS


def get_main_theme_css() -> str:
    """Get main theme CSS."""
    return MAIN_THEME_CSS


def apply_theme() -> None:
    """
    Apply the complete white theme to the current page.
    This should be called in every page after st.set_page_config().
    """
    # Apply anti-flash CSS first (critical)
    st.markdown(ANTI_FLASH_CSS, unsafe_allow_html=True)
    
    # Apply main theme
    st.markdown(MAIN_THEME_CSS, unsafe_allow_html=True)
    
    # Apply dataframe styling
    st.markdown(DATAFRAME_CSS, unsafe_allow_html=True)
    
    # Apply chart styling
    st.markdown(CHART_CSS, unsafe_allow_html=True)


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


def get_chart_colors() -> list:
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


def style_chart(fig, height: int = 400, show_legend: bool = True):
    """Apply consistent visible styling to a Plotly figure.

    Ensures:
    - White backgrounds
    - Black fonts
    - Light gray grid
    - Fallback forcing of trace colors if Plotly/theme caused white traces
    - Optional legend toggle
    """
    fig.update_layout(
        height=height,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#000000', size=12),
        title_font=dict(color='#000000', size=16),
        legend=dict(font=dict(color='#000000', size=12)),
        xaxis=dict(gridcolor='#e5e7eb', title_font=dict(color='#000000')),
        yaxis=dict(gridcolor='#e5e7eb', title_font=dict(color='#000000')),
        showlegend=show_legend
    )

    palette = get_chart_colors()
    # Force each trace to have a visible color if empty/white
    for i, trace in enumerate(fig.data):
        fallback_color = palette[i % len(palette)]
        # Line charts
        if hasattr(trace, 'line'):
            if getattr(trace.line, 'color', None) in (None, '#FFFFFF', 'white'):
                trace.line.color = fallback_color
            if getattr(trace.line, 'width', None) is None:
                trace.line.width = 3
        # Markers
        if hasattr(trace, 'marker'):
            if getattr(trace.marker, 'color', None) in (None, '#FFFFFF', 'white'):
                trace.marker.color = fallback_color
            # Only scatter-like traces support marker.size
            if getattr(trace, 'type', None) in ('scatter', 'scattergl'):
                if getattr(trace.marker, 'size', None) in (None, 0):
                    trace.marker.size = 8
        # Pie / Bar fallback
        if trace.type == 'bar':
            if getattr(trace, 'marker', None):
                if getattr(trace.marker, 'color', None) in (None, '#FFFFFF', 'white'):
                    trace.marker.color = fallback_color
                if getattr(trace.marker, 'line', None) and getattr(trace.marker.line, 'color', None) in (None, '#FFFFFF', 'white'):
                    trace.marker.line.color = '#000000'
        if trace.type == 'pie':
            # Ensure text visible
            trace.textfont = dict(color='#000000', size=14)
            if getattr(trace, 'marker', None):
                if getattr(trace.marker, 'line', None):
                    trace.marker.line.color = '#000000'
                    trace.marker.line.width = 2
    return fig


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
