"""
Configuration Settings for Smart City Monitoring System
Centralized configuration for paths, colors, constants, and app settings.
"""

from pathlib import Path
from typing import Dict, Any

# ============================================================================
# PATH CONFIGURATION
# ============================================================================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
NODES_CSV = DATA_DIR / "nodes.csv"
EVENTS_CSV = DATA_DIR / "events.csv"

# ============================================================================
# APP CONFIGURATION
# ============================================================================
APP_CONFIG: Dict[str, Any] = {
    "title": "Smart City Monitoring System",
    "page_title": "Smart City Monitoring System",
    "page_icon": "🏙️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "version": "2.0.0",
    "system_name": "Smart City Monitoring System",
}

# ============================================================================
# MAP CONFIGURATION
# ============================================================================
MAP_CONFIG: Dict[str, Any] = {
    "default_location": [21.028511, 105.804817],  # Hanoi center
    "default_zoom": 13,
    "edit_zoom": 15,
    "tiles": "OpenStreetMap",
}

# Map constants for backward compatibility
MAP_DEFAULT_CENTER = MAP_CONFIG["default_location"]
MAP_DEFAULT_ZOOM = MAP_CONFIG["default_zoom"]
MAP_TILE_STYLE = MAP_CONFIG["tiles"]
MAP_ATTRIBUTION = "OpenStreetMap contributors"

# Node marker colors
NODE_COLORS: Dict[str, str] = {
    "online": "green",
    "offline": "red",
}

NODE_MARKER_COLORS = NODE_COLORS  # Alias for compatibility

# Node marker icons
NODE_ICONS: Dict[str, str] = {
    "online": "check-circle",
    "offline": "exclamation-circle",
}

# ============================================================================
# EVENT TYPE CONFIGURATION
# ============================================================================
EVENT_TYPES: Dict[str, str] = {
    "suspicious_gathering": "Phát hiện có náo loạn, xô xát",
    "person_fall": "Phát hiện có người ngã",
    "suspicious_person": "Phát hiện có người khả nghi",
}

VALID_EVENT_TYPES = list(EVENT_TYPES.keys())

# Event type colors for map markers and charts
EVENT_TYPE_COLORS: Dict[str, str] = {
    "suspicious_gathering": "#ff6b6b",  # Red
    "person_fall": "#4ecdc4",           # Teal
    "suspicious_person": "#ffd93d",     # Yellow
}

# ============================================================================
# STATUS CONFIGURATION
# ============================================================================
STATUS_LABELS: Dict[str, str] = {
    "pending": "Đang chờ",
    "resolved": "Đã xử lý",
    "false_alarm": "Báo động giả",
}

# ============================================================================
# UI THEME CONFIGURATION
# ============================================================================
THEME_CONFIG: Dict[str, str] = {
    "background_color": "#FFFFFF",
    "text_color": "#000000",
    "sidebar_bg": "#F5F5F5",
    "card_bg": "#F8F8F8",
    "border_color": "#DDDDDD",
    "primary_color": "#4CAF50",
    "hover_color": "#F0F0F0",
}

# CSS for white theme
WHITE_THEME_CSS = """
<style>
    /* CRITICAL: Prevent black flash and black bars */
    html, body, #root, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Force white background globally - highest priority */
    * {
        transition: none !important;
    }
    
    body {
        background-color: #FFFFFF !important;
    }
    
    /* Remove Streamlit header black bar */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Toolbar background */
    [data-testid="stToolbar"] {
        background-color: #FFFFFF !important;
    }
    
    /* Decoration (top bar) */
    [data-testid="stDecoration"] {
        background-color: #FFFFFF !important;
        display: none !important;
    }
    
    /* Status widget */
    [data-testid="stStatusWidget"] {
        background-color: #FFFFFF !important;
    }
    
    /* Force white background on main app */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .main .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Main content area */
    .main {
        background-color: #FFFFFF !important;
    }
    
    /* Prevent black flash on load and page transitions */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* All containers */
    .element-container, .stMarkdown, .stText {
        background-color: transparent !important;
        color: #000000 !important;
    }
    
    /* IFrame backgrounds (for components like folium) */
    iframe {
        background-color: #FFFFFF !important;
    }
    
    /* Block container padding area */
    .block-container {
        background-color: #FFFFFF !important;
        padding-top: 1rem !important;
    }
    
    /* Remove any dark overlays */
    [data-testid="stImage"], [data-testid="stImageContainer"] {
        background-color: transparent !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
        border-right: 1px solid #DDDDDD !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #F5F5F5 !important;
    }
    
    /* All text elements */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #000000 !important;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #F8F8F8;
        border: 1px solid #DDDDDD;
        color: #000000 !important;
    }
    
    div[data-testid="metric-container"] * {
        color: #000000 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #333333;
    }
    
    .stButton>button:hover {
        background-color: #F0F0F0;
    }
    
    /* Selectbox and input fields */
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
    }
    
    /* Selectbox label */
    .stSelectbox label, .stMultiSelect label, .stTextInput label, .stNumberInput label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* Dropdown menus */
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
    
    /* Dropdown list items */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
    }
    
    ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    ul[role="listbox"] li:hover {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F8F8F8 !important;
        color: #000000 !important;
        border: 1px solid #DDDDDD !important;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #DDDDDD !important;
    }
    
    /* Dataframe/Table */
    .stDataFrame, [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
    }
    
    .stDataFrame table {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .stDataFrame thead tr th {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        border: 1px solid #DDDDDD !important;
    }
    
    .stDataFrame tbody tr td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #EEEEEE !important;
    }
    
    /* Plotly charts - force white background */
    .js-plotly-plot, .plotly {
        background-color: #FFFFFF !important;
    }
    
    .js-plotly-plot .plotly .svg-container {
        background-color: #FFFFFF !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF !important;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #E8E8E8 !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: #FFFFFF !important;
        border: 1px solid #4CAF50 !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #D0D0D0 !important;
        color: #000000 !important;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #F8F8F8;
        color: #000000;
        border: 1px solid #DDDDDD;
    }
    
    /* Additional fixes for black flash prevention */
    div[role="main"] {
        background-color: #FFFFFF !important;
    }
    
    /* Page container */
    .stApp > header + div {
        background-color: #FFFFFF !important;
    }
    
    /* Spinner and loading states */
    [data-testid="stSpinner"] {
        background-color: transparent !important;
    }
    
    /* Toast notifications */
    [data-testid="toastContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* Modal/Dialog backgrounds */
    [data-testid="stModal"], [data-testid="stDialog"] {
        background-color: #FFFFFF !important;
    }
    
    /* Bottom toolbar */
    footer {
        background-color: #FFFFFF !important;
        visibility: hidden;
    }
    
    /* Remove manage app button if visible */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Streamlit branding */
    footer:after {
        content: "";
        visibility: hidden;
        display: block;
    }
    
    /* Video/media elements */
    video, audio {
        background-color: #FFFFFF !important;
    }
    
    /* Code blocks */
    .stCode, pre, code {
        background-color: #F8F8F8 !important;
        color: #000000 !important;
        border: 1px solid #DDDDDD !important;
    }
    
    /* Ensure all child elements inherit */
    .stApp *, .main *, [data-testid="stAppViewContainer"] * {
        background-color: inherit;
    }
</style>
"""

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
DISPLAY_CONFIG: Dict[str, Any] = {
    "max_events_display": 10,
    "refresh_interval": 30,  # seconds
    "auto_refresh_enabled": True,
    "date_format": "%Y-%m-%d %H:%M:%S",
}

# ============================================================================
# VALIDATION RULES
# ============================================================================
VALIDATION_RULES: Dict[str, Any] = {
    "node_id_pattern": r"^NODE_\d{3}$",
    "camera_id_pattern": r"^CAM_\d{3}$",
    "lat_range": (-90, 90),
    "lon_range": (-180, 180),
    "max_cameras_per_node": 10,
}
