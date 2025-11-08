"""
Main Dashboard Page - Smart City Monitoring System
Real-time event monitoring with interactive map and event feed.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

# UI Components
from ui.theme_manager import apply_page_config, apply_theme, get_status_color
from ui.components import (
    render_page_header,
    render_section_header,
    render_metric_card,
    render_styled_dataframe,
    render_columns,
    render_divider,
    render_info_box,
)

# Config and Utils
from config.settings import EVENT_TYPES
from utils.data_loader import initialize_data
from utils.map_utils import create_base_map, add_all_nodes
from utils.helpers import init_session_state
from utils.logger import log_info, LogOperation


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

apply_page_config(page_title="Smart City Monitoring System - Bảng điều khiển")
apply_theme()


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_dashboard_state() -> None:
    """Initialize dashboard session state."""
    
    # Load data
    init_session_state('nodes_df', None)
    init_session_state('events_df', None)
    
    if st.session_state.nodes_df is None or st.session_state.events_df is None:
        with LogOperation("Loading data for Main Dashboard"):
            nodes_df, events_df = initialize_data()
            st.session_state.nodes_df = nodes_df
            st.session_state.events_df = events_df
    
    # Initialize configuration
    if 'config' not in st.session_state:
        st.session_state.config = {
            'max_events_display': 10,
            'refresh_interval': 30,  # seconds
            'auto_refresh_enabled': True
        }
    
    # Initialize cameras data (mock)
    if 'cameras' not in st.session_state:
        st.session_state.cameras = pd.DataFrame({
            'camera_id': ['CAM_001', 'CAM_002', 'CAM_003', 'CAM_004', 'CAM_005', 
                         'CAM_006', 'CAM_007', 'CAM_008', 'CAM_009', 'CAM_010'],
            'node_id': ['NODE_001', 'NODE_001', 'NODE_001', 'NODE_002', 'NODE_002',
                       'NODE_002', 'NODE_002', 'NODE_004', 'NODE_004', 'NODE_004'],
            'camera_name': ['Cam 1', 'Cam 2', 'Cam 3', 'Cam 1', 'Cam 2',
                           'Cam 3', 'Cam 4', 'Cam 1', 'Cam 2', 'Cam 3'],
            'status': ['online', 'online', 'offline', 'online', 'online',
                      'online', 'online', 'online', 'offline', 'online']
        })


initialize_dashboard_state()


# ============================================================================
# AUTO-REFRESH
# ============================================================================

if st.session_state.config.get('auto_refresh_enabled', True):
    refresh_interval = st.session_state.config.get('refresh_interval', 30)
    st_autorefresh(interval=refresh_interval * 1000, key="dashboard_refresh")


# ============================================================================
# HEADER
# ============================================================================

render_page_header(
    title="Bảng điều khiển",
    description="**Hệ thống Giám sát Thành phố Thông minh**"
)


# ============================================================================
# TOP METRICS
# ============================================================================

col1, col2, col3 = render_columns(3)

total_nodes = len(st.session_state.nodes_df)
online_nodes = len(st.session_state.nodes_df[st.session_state.nodes_df['status'] == 'online'])
pending_events = len(st.session_state.events_df[st.session_state.events_df['status'] == 'pending'])

with col1:
    render_metric_card("Tổng số Node", str(total_nodes), f"{online_nodes} đang hoạt động")

with col2:
    render_metric_card("Tổng số Camera", str(len(st.session_state.cameras)))

with col3:
    render_metric_card("Sự kiện đang chờ", str(pending_events))

render_divider()


# ============================================================================
# MAIN CONTENT: MAP + EVENT FEED
# ============================================================================

col_map, col_events = st.columns([3, 2])


# ============================================================================
# A. MAP VIEW
# ============================================================================

with col_map:
    st.subheader("Bản đồ Trạng thái Node")
    
    # Create map with nodes
    m = create_base_map()
    add_all_nodes(m, st.session_state.nodes_df, show_popups=True)
    
    # Display map
    st_folium(m, width=None, height=450)
    
    # Legend
    st.markdown("""
    **Chú thích:**  
    🟢 **Xanh** = Node Trực tuyến | 🔴 **Đỏ** = Node Ngoại tuyến
    """)


# ============================================================================
# B. EVENT FEED
# ============================================================================

with col_events:
    st.subheader("Thông báo")
    
    # Event type names - from config
    event_type_names = EVENT_TYPES
    
    # Filter controls
    col_filter1 = st.columns(1)[0]
    
    with col_filter1:
        # Get unique event types and create display options
        valid_types = list(EVENT_TYPES.keys())
        unique_types = st.session_state.events_df['event_type'].unique().tolist()
        filtered_types = [t for t in unique_types if t in valid_types]
        
        # Create options with Vietnamese names
        event_options = ['Tất cả'] + [event_type_names.get(t, t) for t in sorted(filtered_types)]
        selected_display = st.selectbox("Loại sự kiện", event_options, key="event_type_filter")
        
        # Map back to English key
        if selected_display == 'Tất cả':
            selected_type = 'All'
        else:
            selected_type = next((k for k, v in event_type_names.items() if v == selected_display), 'All')
    
    # Filter events - only show valid event types
    valid_event_types = list(EVENT_TYPES.keys())
    filtered_events = st.session_state.events_df[
        (st.session_state.events_df['status'] == 'pending') &
        (st.session_state.events_df['event_type'].isin(valid_event_types))
    ].copy()
    
    if selected_type != 'All':
        filtered_events = filtered_events[filtered_events['event_type'] == selected_type]
    
    # Sort by timestamp (most recent first)
    filtered_events = filtered_events.sort_values('timestamp', ascending=False)
    
    # Limit to max display
    max_display = st.session_state.config.get('max_events_display', 10)
    filtered_events = filtered_events.head(max_display)
    
    st.caption(f"Hiển thị {len(filtered_events)} sự kiện")
    
    # Display events
    if len(filtered_events) == 0:
        st.info("Không có sự kiện nào đang chờ xử lý")
    else:
        for idx, event in filtered_events.iterrows():
            # Get Vietnamese event name
            event_name = event_type_names.get(event['event_type'], event['event_type'].replace('_', ' ').title())
            
            # Event card
            with st.expander(
                f"{event_name} - {event['location']}",
                expanded=False
            ):
                st.markdown(f"**Thời gian:** {event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Vị trí:** {event['location']}")
                st.markdown(f"**Node:** {event['node_id']}")
                st.markdown("---")
                st.markdown(f"**Mô tả:**")
                st.info(event['description'])
                
                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button(
                        "Đã xử lý",
                        key=f"resolve_{event['event_id']}",
                        use_container_width=True
                    ):
                        # Mark as resolved
                        st.session_state.events_df.loc[
                            st.session_state.events_df['event_id'] == event['event_id'],
                            'status'
                        ] = 'resolved'
                        st.success("Đã đánh dấu sự kiện là đã xử lý!")
                        time.sleep(0.5)
                        st.rerun()
                
                with col_btn2:
                    if st.button(
                        "Báo động giả",
                        key=f"false_{event['event_id']}",
                        use_container_width=True
                    ):
                        # Mark as false alarm
                        st.session_state.events_df.loc[
                            st.session_state.events_df['event_id'] == event['event_id'],
                            'status'
                        ] = 'false_alarm'
                        st.warning("Đã đánh dấu là báo động giả!")
                        time.sleep(0.5)
                        st.rerun()


# ============================================================================
# FOOTER INFO
# ============================================================================

st.markdown("---")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    refresh_status = "Bật" if st.session_state.config.get('auto_refresh_enabled') else "Tắt"
    st.caption(f"**Tự động làm mới:** {refresh_status}")

with col_info2:
    refresh_interval = st.session_state.config.get('refresh_interval', 30)
    st.caption(f"**Khoảng thời gian làm mới:** {refresh_interval}s")

with col_info3:
    st.caption(f"**Cập nhật lần cuối:** {datetime.now().strftime('%H:%M:%S')}")

log_info("Main Dashboard page rendered successfully")
