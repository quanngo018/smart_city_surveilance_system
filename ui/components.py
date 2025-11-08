"""
UI Components - Smart City Monitoring System
Reusable UI components for consistent interface across all pages.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List


# ============================================================================
# PAGE HEADERS
# ============================================================================

def render_page_header(title: str, description: Optional[str] = None) -> None:
    """
    Render a standardized page header.
    
    Args:
        title: Page title
        description: Optional page description
    """
    st.title(title)
    if description:
        st.markdown(description)
    st.markdown("---")


def render_section_header(title: str, level: int = 3) -> None:
    """
    Render a section header.
    
    Args:
        title: Section title
        level: Header level (1-6)
    """
    header_tag = f"h{level}"
    st.markdown(f"<{header_tag}>{title}</{header_tag}>", unsafe_allow_html=True)


# ============================================================================
# METRIC CARDS
# ============================================================================

def render_metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "normal",
    help_text: Optional[str] = None
) -> None:
    """
    Render a styled metric card.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Change indicator (optional)
        delta_color: Color of delta ("normal", "inverse", "off")
        help_text: Tooltip help text
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text
    )


# ============================================================================
# DATAFRAMES
# ============================================================================

def render_styled_dataframe(
    df: pd.DataFrame,
    column_config: Optional[Dict[str, Any]] = None,
    hide_index: bool = True,
    use_container_width: bool = True,
    height: Optional[int] = 400
) -> None:
    """
    Render a styled dataframe with consistent formatting.
    
    Args:
        df: DataFrame to display
        column_config: Column configuration dict
        hide_index: Whether to hide the index
        use_container_width: Whether to use full container width
        height: Optional fixed height
    """
    st.markdown("""
        <style>
        [data-testid="stDataFrame"] {
            background-color: #fafafa !important;
        }
        [data-testid="stDataFrame"] th {
            background-color: #f1f3f4 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df,
        column_config=column_config,
        hide_index=hide_index,
        use_container_width=use_container_width,
        height=height
    )


# ============================================================================
# MESSAGE BOXES
# ============================================================================

def render_info_box(message: str, icon: str = "ℹ️") -> None:
    """
    Render an info box.
    
    Args:
        message: Message to display
        icon: Icon emoji
    """
    st.info(f"{icon} {message}")


def render_success_box(message: str, icon: str = "✅") -> None:
    """
    Render a success box.
    
    Args:
        message: Message to display
        icon: Icon emoji
    """
    st.success(f"{icon} {message}")


def render_warning_box(message: str, icon: str = "⚠️") -> None:
    """
    Render a warning box.
    
    Args:
        message: Message to display
        icon: Icon emoji
    """
    st.warning(f"{icon} {message}")


def render_error_box(message: str, icon: str = "❌") -> None:
    """
    Render an error box.
    
    Args:
        message: Message to display
        icon: Icon emoji
    """
    st.error(f"{icon} {message}")


# ============================================================================
# FORMS
# ============================================================================

def render_text_input(
    label: str,
    key: Optional[str] = None,
    value: str = "",
    placeholder: str = "",
    help_text: Optional[str] = None,
    required: bool = False
) -> str:
    """
    Render a styled text input.
    
    Args:
        label: Input label
        key: Unique key for the widget
        value: Default value
        placeholder: Placeholder text
        help_text: Help tooltip
        required: Whether field is required
        
    Returns:
        Input value
    """
    label_text = f"{label} *" if required else label
    return st.text_input(
        label_text,
        key=key,
        value=value,
        placeholder=placeholder,
        help=help_text
    )


def render_number_input(
    label: str,
    key: Optional[str] = None,
    value: float = 0.0,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    step: Optional[float] = None,
    format_str: str = "%.2f",
    help_text: Optional[str] = None,
    required: bool = False
) -> float:
    """
    Render a styled number input.
    
    Args:
        label: Input label
        key: Unique key for the widget
        value: Default value
        min_value: Minimum value
        max_value: Maximum value
        step: Step increment
        format_str: Number format string
        help_text: Help tooltip
        required: Whether field is required
        
    Returns:
        Input value
    """
    label_text = f"{label} *" if required else label
    return st.number_input(
        label_text,
        key=key,
        value=value,
        min_value=min_value,
        max_value=max_value,
        step=step,
        format=format_str,
        help=help_text
    )


def render_selectbox(
    label: str,
    options: List[Any],
    key: Optional[str] = None,
    index: int = 0,
    help_text: Optional[str] = None,
    required: bool = False
) -> Any:
    """
    Render a styled selectbox.
    
    Args:
        label: Selectbox label
        options: List of options
        key: Unique key for the widget
        index: Default selected index
        help_text: Help tooltip
        required: Whether field is required
        
    Returns:
        Selected value
    """
    label_text = f"{label} *" if required else label
    return st.selectbox(
        label_text,
        options=options,
        key=key,
        index=index,
        help=help_text
    )


# ============================================================================
# BUTTONS
# ============================================================================

def render_button(
    label: str,
    key: Optional[str] = None,
    help_text: Optional[str] = None,
    use_container_width: bool = False,
    button_type: str = "secondary"
) -> bool:
    """
    Render a styled button.
    
    Args:
        label: Button label
        key: Unique key for the widget
        help_text: Help tooltip
        use_container_width: Whether to use full container width
        button_type: Button type ("primary" or "secondary")
        
    Returns:
        True if button was clicked
    """
    return st.button(
        label,
        key=key,
        help=help_text,
        use_container_width=use_container_width,
        type=button_type
    )


# ============================================================================
# TABS
# ============================================================================

def render_tabs(tab_labels: List[str]) -> List:
    """
    Render styled tabs.
    
    Args:
        tab_labels: List of tab labels
        
    Returns:
        List of tab objects
    """
    return st.tabs(tab_labels)


# ============================================================================
# COLUMNS
# ============================================================================

def render_columns(num_cols: int, gap: str = "medium") -> List:
    """
    Render columns with consistent spacing.
    
    Args:
        num_cols: Number of columns
        gap: Gap size ("small", "medium", "large")
        
    Returns:
        List of column objects
    """
    return st.columns(num_cols, gap=gap)


# ============================================================================
# EXPANDER
# ============================================================================

def render_expander(label: str, expanded: bool = False) -> Any:
    """
    Render a styled expander.
    
    Args:
        label: Expander label
        expanded: Whether initially expanded
        
    Returns:
        Expander context
    """
    return st.expander(label, expanded=expanded)


# ============================================================================
# DIVIDER
# ============================================================================

def render_divider() -> None:
    """Render a horizontal divider."""
    st.markdown("---")


# ============================================================================
# FOOTER
# ============================================================================

def render_footer(text: str) -> None:
    """
    Render a page footer.
    
    Args:
        text: Footer text
    """
    st.markdown("---")
    st.caption(text)
