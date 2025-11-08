"""
Data Loader Module for Smart City Monitoring System
Handles loading and validation of data from CSV files.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
import streamlit as st

from config.settings import NODES_CSV, EVENTS_CSV, VALID_EVENT_TYPES
from utils.logger import log_info, log_error, log_warning, log_critical, LogOperation


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=60)
def load_nodes(csv_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load nodes data from CSV file with caching.
    
    Args:
        csv_path: Path to nodes CSV file (default: from config)
    
    Returns:
        DataFrame containing nodes data
    
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        pd.errors.EmptyDataError: If CSV is empty
    """
    path = csv_path or NODES_CSV
    
    try:
        with LogOperation(f"Loading nodes from {path}"):
            df = pd.read_csv(path)
            
            # Validate required columns
            required_columns = ['node_id', 'name', 'lat', 'lon', 'status', 'num_cameras', 'assists_others']
            missing_columns = set(required_columns) - set(df.columns)
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            log_info(f"Loaded {len(df)} nodes successfully")
            return df
            
    except FileNotFoundError:
        log_error(f"Nodes CSV file not found: {path}")
        raise
    except pd.errors.EmptyDataError:
        log_error(f"Nodes CSV file is empty: {path}")
        raise
    except Exception as e:
        log_error(f"Error loading nodes: {e}", exc_info=True)
        raise


@st.cache_data(ttl=60)
def load_events(csv_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load events data from CSV file with caching.
    
    Args:
        csv_path: Path to events CSV file (default: from config)
    
    Returns:
        DataFrame containing events data with timestamp parsed
    
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        pd.errors.EmptyDataError: If CSV is empty
    """
    path = csv_path or EVENTS_CSV
    
    try:
        with LogOperation(f"Loading events from {path}"):
            df = pd.read_csv(path)
            
            # Validate required columns
            required_columns = ['event_id', 'timestamp', 'node_id', 'location', 
                              'event_type', 'description', 'status']
            missing_columns = set(required_columns) - set(df.columns)
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Parse timestamp
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter to only valid event types
            invalid_events = df[~df['event_type'].isin(VALID_EVENT_TYPES)]
            if len(invalid_events) > 0:
                log_warning(
                    f"Found {len(invalid_events)} events with invalid types, "
                    f"filtering them out"
                )
                df = df[df['event_type'].isin(VALID_EVENT_TYPES)]
            
            log_info(f"Loaded {len(df)} events successfully")
            return df
            
    except FileNotFoundError:
        log_error(f"Events CSV file not found: {path}")
        raise
    except pd.errors.EmptyDataError:
        log_error(f"Events CSV file is empty: {path}")
        raise
    except Exception as e:
        log_error(f"Error loading events: {e}", exc_info=True)
        raise


# ============================================================================
# DATA SAVING FUNCTIONS
# ============================================================================

def save_nodes(df: pd.DataFrame, csv_path: Optional[Path] = None) -> bool:
    """
    Save nodes data to CSV file.
    
    Args:
        df: DataFrame containing nodes data
        csv_path: Path to save CSV file (default: from config)
    
    Returns:
        True if successful, False otherwise
    """
    path = csv_path or NODES_CSV
    
    try:
        with LogOperation(f"Saving {len(df)} nodes to {path}"):
            df.to_csv(path, index=False)
            log_info(f"Saved nodes successfully")
            return True
            
    except Exception as e:
        log_error(f"Error saving nodes: {e}", exc_info=True)
        return False


def save_events(df: pd.DataFrame, csv_path: Optional[Path] = None) -> bool:
    """
    Save events data to CSV file.
    
    Args:
        df: DataFrame containing events data
        csv_path: Path to save CSV file (default: from config)
    
    Returns:
        True if successful, False otherwise
    """
    path = csv_path or EVENTS_CSV
    
    try:
        with LogOperation(f"Saving {len(df)} events to {path}"):
            df.to_csv(path, index=False)
            log_info(f"Saved events successfully")
            return True
            
    except Exception as e:
        log_error(f"Error saving events: {e}", exc_info=True)
        return False


# ============================================================================
# DATA VALIDATION FUNCTIONS
# ============================================================================

def validate_node_data(node_data: dict) -> Tuple[bool, str]:
    """
    Validate node data before saving.
    
    Args:
        node_data: Dictionary containing node information
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['node_id', 'name', 'lat', 'lon', 'status', 'num_cameras', 'assists_others']
    
    # Check required fields
    for field in required_fields:
        if field not in node_data:
            return False, f"Missing required field: {field}"
    
    # Validate latitude
    try:
        lat = float(node_data['lat'])
        if not -90 <= lat <= 90:
            return False, f"Latitude must be between -90 and 90, got {lat}"
    except (ValueError, TypeError):
        return False, f"Invalid latitude value: {node_data['lat']}"
    
    # Validate longitude
    try:
        lon = float(node_data['lon'])
        if not -180 <= lon <= 180:
            return False, f"Longitude must be between -180 and 180, got {lon}"
    except (ValueError, TypeError):
        return False, f"Invalid longitude value: {node_data['lon']}"
    
    # Validate status
    if node_data['status'] not in ['online', 'offline']:
        return False, f"Status must be 'online' or 'offline', got {node_data['status']}"
    
    # Validate num_cameras
    try:
        num_cameras = int(node_data['num_cameras'])
        if num_cameras < 0:
            return False, f"Number of cameras cannot be negative"
    except (ValueError, TypeError):
        return False, f"Invalid number of cameras: {node_data['num_cameras']}"
    
    return True, ""


def validate_event_data(event_data: dict) -> Tuple[bool, str]:
    """
    Validate event data before saving.
    
    Args:
        event_data: Dictionary containing event information
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['event_id', 'timestamp', 'node_id', 'location', 
                      'event_type', 'description', 'status']
    
    # Check required fields
    for field in required_fields:
        if field not in event_data:
            return False, f"Missing required field: {field}"
    
    # Validate event type
    if event_data['event_type'] not in VALID_EVENT_TYPES:
        return False, f"Invalid event type: {event_data['event_type']}"
    
    # Validate status
    if event_data['status'] not in ['pending', 'resolved', 'false_alarm']:
        return False, f"Invalid status: {event_data['status']}"
    
    return True, ""


# ============================================================================
# DATA INITIALIZATION
# ============================================================================

def initialize_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Initialize and load all required data.
    
    Returns:
        Tuple of (nodes_df, events_df)
    """
    try:
        nodes_df = load_nodes()
        events_df = load_events()
        return nodes_df, events_df
    except Exception as e:
        log_critical(f"Failed to initialize data: {e}", exc_info=True)
        st.error(f"Failed to load data: {e}")
        st.stop()
