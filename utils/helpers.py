"""
Helper Utilities Module for Smart City Monitoring System
Common utility functions used across the application.
"""

from datetime import datetime
from typing import Tuple, Optional
import streamlit as st

from utils.logger import log_debug


# ============================================================================
# DATE/TIME FORMATTING
# ============================================================================

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.
    
    Args:
        dt: Datetime object
        format_str: Format string (default: YYYY-MM-DD HH:MM:SS)
    
    Returns:
        Formatted datetime string
    """
    try:
        return dt.strftime(format_str)
    except Exception as e:
        log_debug(f"Error formatting datetime: {e}")
        return str(dt)


def format_datetime_vietnamese(dt: datetime) -> str:
    """
    Format datetime in Vietnamese style.
    
    Args:
        dt: Datetime object
    
    Returns:
        Formatted datetime string in Vietnamese
    """
    try:
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except Exception as e:
        log_debug(f"Error formatting datetime: {e}")
        return str(dt)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    Parse datetime string to datetime object.
    
    Args:
        dt_str: Datetime string
        format_str: Format string
    
    Returns:
        Datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(dt_str, format_str)
    except Exception as e:
        log_debug(f"Error parsing datetime '{dt_str}': {e}")
        return None


# ============================================================================
# COORDINATE VALIDATION
# ============================================================================

def validate_coordinates(lat: float, lon: float) -> Tuple[bool, str]:
    """
    Validate latitude and longitude coordinates.
    
    Args:
        lat: Latitude value
        lon: Longitude value
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check latitude
    try:
        lat_float = float(lat)
        if not -90 <= lat_float <= 90:
            return False, f"Latitude must be between -90 and 90, got {lat_float}"
    except (ValueError, TypeError):
        return False, f"Invalid latitude value: {lat}"
    
    # Check longitude
    try:
        lon_float = float(lon)
        if not -180 <= lon_float <= 180:
            return False, f"Longitude must be between -180 and 180, got {lon_float}"
    except (ValueError, TypeError):
        return False, f"Invalid longitude value: {lon}"
    
    return True, ""


def parse_coordinates_from_map_click(click_data: str) -> Optional[Tuple[float, float]]:
    """
    Parse coordinates from Folium map click data.
    
    Args:
        click_data: String containing click coordinates (format: "Lat, Lon: (lat, lon)")
    
    Returns:
        Tuple of (lat, lon) or None if parsing fails
    """
    try:
        # Expected format: "Lat, Lon: (10.762622, 106.660172)"
        coords_str = click_data.split(": ")[1].strip("()")
        lat, lon = map(float, coords_str.split(", "))
        return lat, lon
    except Exception as e:
        log_debug(f"Error parsing coordinates from '{click_data}': {e}")
        return None


# ============================================================================
# STRING FORMATTING
# ============================================================================

def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length with suffix.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing/replacing invalid characters.
    
    Args:
        filename: Input filename
    
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


# ============================================================================
# UI HELPERS
# ============================================================================

def show_success_message(message: str, duration: int = 3) -> None:
    """
    Display success message with auto-dismiss.
    
    Args:
        message: Success message
        duration: Duration in seconds
    """
    placeholder = st.empty()
    placeholder.success(message)
    import time
    time.sleep(duration)
    placeholder.empty()


def show_error_message(message: str, duration: int = 5) -> None:
    """
    Display error message with auto-dismiss.
    
    Args:
        message: Error message
        duration: Duration in seconds
    """
    placeholder = st.empty()
    placeholder.error(message)
    import time
    time.sleep(duration)
    placeholder.empty()


def show_warning_message(message: str, duration: int = 4) -> None:
    """
    Display warning message with auto-dismiss.
    
    Args:
        message: Warning message
        duration: Duration in seconds
    """
    placeholder = st.empty()
    placeholder.warning(message)
    import time
    time.sleep(duration)
    placeholder.empty()


def create_metric_card(label: str, value: str, delta: Optional[str] = None) -> None:
    """
    Create a styled metric card.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta value
    """
    st.metric(label=label, value=value, delta=delta)


# ============================================================================
# STATUS HELPERS
# ============================================================================

def get_status_color(status: str) -> str:
    """
    Get color for status value.
    
    Args:
        status: Status string (online/offline, pending/resolved/false_alarm)
    
    Returns:
        Color string
    """
    status_colors = {
        'online': 'green',
        'offline': 'red',
        'pending': 'orange',
        'resolved': 'green',
        'false_alarm': 'gray'
    }
    return status_colors.get(status.lower(), 'gray')


def get_status_label_vietnamese(status: str) -> str:
    """
    Get Vietnamese label for status.
    
    Args:
        status: Status string in English
    
    Returns:
        Status label in Vietnamese
    """
    status_labels = {
        'online': 'Trực tuyến',
        'offline': 'Ngoại tuyến',
        'pending': 'Đang xử lý',
        'resolved': 'Đã giải quyết',
        'false_alarm': 'Báo động giả'
    }
    return status_labels.get(status.lower(), status)


# ============================================================================
# DATA HELPERS
# ============================================================================

def safe_get(dictionary: dict, key: str, default: any = "N/A") -> any:
    """
    Safely get value from dictionary with default.
    
    Args:
        dictionary: Input dictionary
        key: Key to retrieve
        default: Default value if key not found
    
    Returns:
        Value or default
    """
    return dictionary.get(key, default)


def convert_to_int(value: any, default: int = 0) -> int:
    """
    Safely convert value to integer.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Integer value
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def convert_to_float(value: any, default: float = 0.0) -> float:
    """
    Safely convert value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Float value
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# ============================================================================
# STREAMLIT HELPERS
# ============================================================================

def apply_custom_css(css: str) -> None:
    """
    Apply custom CSS to Streamlit app.
    
    Args:
        css: CSS string
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def inject_css_early(css: str) -> None:
    """
    Inject CSS as early as possible to prevent flash.
    Uses aggressive styling to override defaults immediately.
    
    Args:
        css: CSS string to inject
    """
    # First inject with regular method
    st.markdown(css, unsafe_allow_html=True)
    
    # Also inject a minimal critical CSS that loads immediately
    critical_css = """
    <style>
        /* CRITICAL CSS - Loads first to prevent black flash */
        html, body { 
            background-color: #FFFFFF !important; 
            margin: 0 !important;
            padding: 0 !important;
        }
        * { 
            transition: none !important; 
            animation-duration: 0s !important;
        }
        [data-testid="stApp"], 
        [data-testid="stAppViewContainer"],
        .main,
        header[data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }
        [data-testid="stDecoration"] {
            display: none !important;
        }
    </style>
    """
    st.markdown(critical_css, unsafe_allow_html=True)


def set_page_config(
    page_title: str = "Smart City Monitoring",
    page_icon: str = "🏙️",
    layout: str = "wide"
) -> None:
    """
    Configure Streamlit page settings.
    
    Args:
        page_title: Page title
        page_icon: Page icon
        layout: Page layout ('wide' or 'centered')
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )


def init_session_state(key: str, default_value: any) -> None:
    """
    Initialize session state variable if not exists.
    
    Args:
        key: Session state key
        default_value: Default value
    """
    if key not in st.session_state:
        st.session_state[key] = default_value
        log_debug(f"Initialized session state '{key}' with value: {default_value}")


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_non_empty(value: str, field_name: str = "Field") -> Tuple[bool, str]:
    """
    Validate that a string is not empty.
    
    Args:
        value: String value to validate
        field_name: Name of the field for error message
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value or not value.strip():
        return False, f"{field_name} cannot be empty"
    return True, ""


def validate_positive_number(value: any, field_name: str = "Value") -> Tuple[bool, str]:
    """
    Validate that a value is a positive number.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error message
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        num = float(value)
        if num <= 0:
            return False, f"{field_name} must be positive"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a number"


def validate_in_range(
    value: float, 
    min_val: float, 
    max_val: float, 
    field_name: str = "Value"
) -> Tuple[bool, str]:
    """
    Validate that a value is within a range.
    
    Args:
        value: Value to validate
        min_val: Minimum value
        max_val: Maximum value
        field_name: Name of the field for error message
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        num = float(value)
        if not min_val <= num <= max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a number"
