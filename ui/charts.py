"""
Charts CSS Module - Smart City Monitoring System
Plotly chart styling and utilities for consistent, visible charts.
"""

import streamlit as st
from .base import get_chart_colors


# ============================================================================
# CHART CSS
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
# PUBLIC FUNCTIONS
# ============================================================================

def apply_chart_styling() -> None:
    """Apply chart/Plotly CSS styling."""
    # st.markdown(CHART_CSS, unsafe_allow_html=True)
    pass  # TEMPORARILY DISABLED FOR DEBUGGING


def get_chart_css() -> str:
    """
    Get CSS for styling charts and plotly graphs.
    
    Returns:
        Chart CSS string
    """
    return CHART_CSS


def style_chart(fig, height: int = 400, show_legend: bool = True):
    """
    Apply consistent visible styling to a Plotly figure.

    Ensures:
    - White backgrounds
    - Black fonts
    - Light gray grid
    - Fallback forcing of trace colors if Plotly/theme caused white traces
    - Optional legend toggle
    
    Args:
        fig: Plotly figure object
        height: Chart height in pixels
        show_legend: Whether to display legend
        
    Returns:
        Styled Plotly figure
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
