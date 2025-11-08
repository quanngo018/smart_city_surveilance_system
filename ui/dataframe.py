"""
Dataframe/Table CSS Module - Smart City Monitoring System
Styling for dataframes and tables with zebra striping and hover effects.
"""

import streamlit as st


# ============================================================================
# DATAFRAME CSS
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
# PUBLIC FUNCTIONS
# ============================================================================

def apply_dataframe_styling() -> None:
    """Apply dataframe/table CSS styling."""
    st.markdown(DATAFRAME_CSS, unsafe_allow_html=True)


def get_dataframe_css() -> str:
    """
    Get CSS for styling dataframes/tables.
    
    Returns:
        Dataframe CSS string
    """
    return DATAFRAME_CSS
