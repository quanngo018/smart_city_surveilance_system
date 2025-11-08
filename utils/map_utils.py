"""
Map Utilities Module for Smart City Monitoring System
Provides functions for creating and customizing Folium maps.
"""

import folium
from folium import plugins
import pandas as pd
from typing import Optional, Tuple, Dict, Any

from config.settings import (
    MAP_DEFAULT_CENTER, MAP_DEFAULT_ZOOM, MAP_TILE_STYLE, MAP_ATTRIBUTION,
    NODE_MARKER_COLORS, EVENT_TYPE_COLORS, EVENT_TYPES
)
from utils.logger import log_info, log_debug, LogOperation


# ============================================================================
# BASE MAP CREATION
# ============================================================================

def create_base_map(
    center: Optional[Tuple[float, float]] = None,
    zoom: Optional[int] = None,
    tile_style: Optional[str] = None
) -> folium.Map:
    """
    Create a base Folium map with default settings.
    
    Args:
        center: Map center coordinates (lat, lon) - default from config
        zoom: Initial zoom level - default from config
        tile_style: Map tile style - default from config
    
    Returns:
        Folium Map object
    """
    center = center or MAP_DEFAULT_CENTER
    zoom = zoom or MAP_DEFAULT_ZOOM
    tile_style = tile_style or MAP_TILE_STYLE
    
    with LogOperation(f"Creating base map centered at {center}"):
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles=tile_style,
            attr=MAP_ATTRIBUTION
        )
        
        log_debug(f"Created map with zoom={zoom}, tiles={tile_style}")
        return m


def create_clickable_map(
    center: Optional[Tuple[float, float]] = None,
    zoom: Optional[int] = None,
    initial_marker: Optional[Tuple[float, float]] = None
) -> folium.Map:
    """
    Create a map with click-to-select functionality for coordinates.
    
    Args:
        center: Map center coordinates (lat, lon)
        zoom: Initial zoom level
        initial_marker: Initial marker position (lat, lon)
    
    Returns:
        Folium Map object with click handler
    """
    m = create_base_map(center=center, zoom=zoom)
    
    # Add click handler
    m.add_child(folium.LatLngPopup())
    
    # Add initial marker if provided
    if initial_marker:
        folium.Marker(
            location=initial_marker,
            popup="Vị trí đã chọn",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        log_debug(f"Added initial marker at {initial_marker}")
    
    return m


# ============================================================================
# NODE MARKERS
# ============================================================================

def add_node_marker(
    m: folium.Map,
    node_data: Dict[str, Any],
    show_popup: bool = True
) -> None:
    """
    Add a single node marker to the map.
    
    Args:
        m: Folium Map object
        node_data: Dictionary containing node information
        show_popup: Whether to show popup on marker
    """
    lat = node_data.get('lat')
    lon = node_data.get('lon')
    
    if lat is None or lon is None:
        log_debug(f"Skipping node {node_data.get('node_id')} - missing coordinates")
        return
    
    # Determine marker color based on status
    status = node_data.get('status', 'offline')
    color = NODE_MARKER_COLORS.get(status, 'gray')
    
    # Create popup content
    popup_html = f"""
    <div style="font-family: Arial; min-width: 200px;">
        <h4 style="margin: 0 0 10px 0;">{node_data.get('name', 'N/A')}</h4>
        <table style="width: 100%;">
            <tr><td><b>ID:</b></td><td>{node_data.get('node_id', 'N/A')}</td></tr>
            <tr><td><b>Trạng thái:</b></td><td>{status}</td></tr>
            <tr><td><b>Số camera:</b></td><td>{node_data.get('num_cameras', 0)}</td></tr>
            <tr><td><b>Hỗ trợ node khác:</b></td><td>{node_data.get('assists_others', 'N/A')}</td></tr>
        </table>
    </div>
    """
    
    # Add marker
    marker = folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300) if show_popup else None,
        tooltip=node_data.get('name', 'N/A'),
        icon=folium.Icon(color=color, icon='video-camera', prefix='fa')
    )
    marker.add_to(m)
    
    log_debug(f"Added marker for node {node_data.get('node_id')} at ({lat}, {lon})")


def add_all_nodes(
    m: folium.Map,
    nodes_df: pd.DataFrame,
    show_popups: bool = True
) -> None:
    """
    Add all nodes from DataFrame to the map.
    
    Args:
        m: Folium Map object
        nodes_df: DataFrame containing nodes data
        show_popups: Whether to show popups on markers
    """
    with LogOperation(f"Adding {len(nodes_df)} nodes to map"):
        for _, node in nodes_df.iterrows():
            add_node_marker(m, node.to_dict(), show_popup=show_popups)


# ============================================================================
# EVENT MARKERS
# ============================================================================

def add_event_marker(
    m: folium.Map,
    event_data: Dict[str, Any],
    node_coords: Optional[Tuple[float, float]] = None
) -> None:
    """
    Add a single event marker to the map.
    
    Args:
        m: Folium Map object
        event_data: Dictionary containing event information
        node_coords: Coordinates of associated node (lat, lon)
    """
    if node_coords is None:
        log_debug(f"Skipping event {event_data.get('event_id')} - no coordinates")
        return
    
    lat, lon = node_coords
    
    # Determine marker color based on event type
    event_type = event_data.get('event_type', '')
    color = EVENT_TYPE_COLORS.get(event_type, 'gray')
    
    # Get Vietnamese event type name
    event_type_vn = EVENT_TYPES.get(event_type, event_type)
    
    # Create popup content
    popup_html = f"""
    <div style="font-family: Arial; min-width: 250px;">
        <h4 style="margin: 0 0 10px 0; color: {color};">{event_type_vn}</h4>
        <table style="width: 100%;">
            <tr><td><b>ID:</b></td><td>{event_data.get('event_id', 'N/A')}</td></tr>
            <tr><td><b>Thời gian:</b></td><td>{event_data.get('timestamp', 'N/A')}</td></tr>
            <tr><td><b>Địa điểm:</b></td><td>{event_data.get('location', 'N/A')}</td></tr>
            <tr><td><b>Node:</b></td><td>{event_data.get('node_id', 'N/A')}</td></tr>
            <tr><td><b>Trạng thái:</b></td><td>{event_data.get('status', 'N/A')}</td></tr>
        </table>
        <p style="margin: 10px 0 0 0;"><b>Chi tiết:</b><br>{event_data.get('description', 'N/A')}</p>
    </div>
    """
    
    # Add circle marker for events
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=event_type_vn,
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7
    ).add_to(m)
    
    log_debug(f"Added event marker for {event_type} at ({lat}, {lon})")


def add_events_to_map(
    m: folium.Map,
    events_df: pd.DataFrame,
    nodes_df: pd.DataFrame
) -> None:
    """
    Add all events from DataFrame to the map using node coordinates.
    
    Args:
        m: Folium Map object
        events_df: DataFrame containing events data
        nodes_df: DataFrame containing nodes data
    """
    with LogOperation(f"Adding {len(events_df)} events to map"):
        # Create node_id to coordinates mapping
        node_coords_map = {}
        for _, node in nodes_df.iterrows():
            node_coords_map[node['node_id']] = (node['lat'], node['lon'])
        
        # Add event markers
        for _, event in events_df.iterrows():
            node_id = event.get('node_id')
            if node_id in node_coords_map:
                add_event_marker(m, event.to_dict(), node_coords_map[node_id])


# ============================================================================
# MAP ENHANCEMENTS
# ============================================================================

def add_marker_cluster(m: folium.Map) -> plugins.MarkerCluster:
    """
    Add a marker cluster group to the map for better performance with many markers.
    
    Args:
        m: Folium Map object
    
    Returns:
        MarkerCluster object
    """
    marker_cluster = plugins.MarkerCluster().add_to(m)
    log_debug("Added marker cluster to map")
    return marker_cluster


def add_fullscreen_button(m: folium.Map) -> None:
    """
    Add a fullscreen button to the map.
    
    Args:
        m: Folium Map object
    """
    plugins.Fullscreen(
        position='topright',
        title='Toàn màn hình',
        title_cancel='Thoát toàn màn hình',
        force_separate_button=True
    ).add_to(m)
    log_debug("Added fullscreen button to map")


def add_measure_control(m: folium.Map) -> None:
    """
    Add a measurement control to the map for distance/area measurements.
    
    Args:
        m: Folium Map object
    """
    plugins.MeasureControl(
        position='topleft',
        primary_length_unit='kilometers',
        secondary_length_unit='meters',
        primary_area_unit='sqkilometers',
        secondary_area_unit='sqmeters'
    ).add_to(m)
    log_debug("Added measure control to map")


def add_minimap(m: folium.Map) -> None:
    """
    Add a minimap overview to the map.
    
    Args:
        m: Folium Map object
    """
    minimap = plugins.MiniMap(toggle_display=True)
    m.add_child(minimap)
    log_debug("Added minimap to map")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_bounds_from_nodes(nodes_df: pd.DataFrame) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Calculate map bounds from nodes data.
    
    Args:
        nodes_df: DataFrame containing nodes data
    
    Returns:
        Tuple of ((min_lat, min_lon), (max_lat, max_lon))
    """
    if nodes_df.empty:
        return MAP_DEFAULT_CENTER, MAP_DEFAULT_CENTER
    
    min_lat = nodes_df['lat'].min()
    max_lat = nodes_df['lat'].max()
    min_lon = nodes_df['lon'].min()
    max_lon = nodes_df['lon'].max()
    
    return ((min_lat, min_lon), (max_lat, max_lon))


def fit_map_to_nodes(m: folium.Map, nodes_df: pd.DataFrame) -> None:
    """
    Adjust map view to fit all nodes.
    
    Args:
        m: Folium Map object
        nodes_df: DataFrame containing nodes data
    """
    bounds = get_bounds_from_nodes(nodes_df)
    m.fit_bounds(bounds)
    log_debug(f"Fitted map to bounds: {bounds}")
