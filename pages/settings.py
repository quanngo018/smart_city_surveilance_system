"""
Settings Page - Smart City Monitoring System
Configuration for nodes, cameras, and display settings with interactive map selection.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
import folium

# UI Components (must import first for theming)
from ui.theme_manager import apply_page_config, apply_theme
from ui.components import (
    render_page_header,
    render_section_header,
    render_styled_dataframe,
    render_text_input,
    render_number_input,
    render_selectbox,
    render_button,
    render_tabs,
    render_columns,
    render_info_box,
    render_success_box,
    render_warning_box,
    render_error_box,
    render_divider,
    render_footer,
)

# Config and Utils
from config.settings import MAP_DEFAULT_CENTER
from utils.data_loader import initialize_data, save_nodes
from utils.map_utils import create_base_map
from utils.helpers import init_session_state, validate_coordinates
from utils.logger import log_info, log_warning, LogOperation


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

apply_page_config(page_title="Smart City Monitoring System - Cài đặt")
apply_theme()



# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_settings_state() -> None:
    """Initialize settings session state."""
    
    # Load data
    init_session_state('nodes_df', None)
    init_session_state('events_df', None)
    
    if st.session_state.nodes_df is None or st.session_state.events_df is None:
        with LogOperation("Loading data for Settings page"):
            nodes_df, events_df = initialize_data()
            st.session_state.nodes_df = nodes_df
            st.session_state.events_df = events_df
    
    # Initialize configuration
    if 'config' not in st.session_state:
        st.session_state.config = {
            'max_events_display': 10,
            'refresh_interval': 30,
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
    
    # Initialize coordinates for add node
    if 'add_node_lat' not in st.session_state:
        st.session_state.add_node_lat = MAP_DEFAULT_CENTER[0]
        st.session_state.add_node_lon = MAP_DEFAULT_CENTER[1]


initialize_settings_state()


# ============================================================================
# HEADER
# ============================================================================

render_page_header(
    title="Cài đặt",
    description="Cấu hình nodes, cameras và tùy chọn hiển thị"
)


# ============================================================================
# SUB-TABS
# ============================================================================

tab1, tab2, tab3 = render_tabs([
    "Cài đặt Node",
    "Cài đặt Camera",
    "Cài đặt Hiển thị"
])


# ============================================================================
# TAB 1: NODE SETTINGS
# ============================================================================

with tab1:
    st.subheader("Quản lý Node")
    st.markdown("Quản lý các AI edge nodes (Jetson Nano, Jetson Orin)")
    
    # Display nodes table
    render_section_header("Các Node hiện tại")
    
    # Prepare display dataframe with better formatting
    nodes_display = st.session_state.nodes_df.copy()
    
    # Format coordinates to 6 decimal places
    nodes_display['lat'] = nodes_display['lat'].apply(lambda x: f"{x:.6f}")
    nodes_display['lon'] = nodes_display['lon'].apply(lambda x: f"{x:.6f}")
    
    # Translate status to Vietnamese with color indicators
    status_map = {'online': '🟢 Trực tuyến', 'offline': '🔴 Ngoại tuyến'}
    nodes_display['status'] = nodes_display['status'].map(status_map)
    
    # Translate assists_others
    assists_map = {'yes': 'Có', 'no': 'Không'}
    nodes_display['assists_others'] = nodes_display['assists_others'].map(assists_map)
    
    # Rename columns to Vietnamese
    nodes_display.columns = ['Node ID', 'Tên', 'Vĩ độ', 'Kinh độ', 'Trạng thái', 'Số Camera', 'Hỗ trợ Node khác']
    
    # Display with custom styling using component
    render_styled_dataframe(
        nodes_display,
        column_config={
            "Node ID": st.column_config.TextColumn("Node ID", width="small"),
            "Tên": st.column_config.TextColumn("Tên", width="medium"),
            "Vĩ độ": st.column_config.TextColumn("Vĩ độ", width="small"),
            "Kinh độ": st.column_config.TextColumn("Kinh độ", width="small"),
            "Trạng thái": st.column_config.TextColumn("Trạng thái", width="small"),
            "Số Camera": st.column_config.NumberColumn("Số Camera", width="small"),
            "Hỗ trợ Node khác": st.column_config.TextColumn("Hỗ trợ", width="small"),
        }
    )
    
    render_divider()
    
    # Node Actions
    col_action1, col_action2 = render_columns(2)
    
    # ========================================================================
    # ADD NODE
    # ========================================================================
    with col_action1:
        st.markdown("### Thêm Node Mới")
        
        # Map for selecting location
        st.markdown("#### Chọn vị trí trên bản đồ")
        st.caption("Click vào bản đồ để chọn tọa độ cho node mới")
        
        add_map = folium.Map(
            location=[st.session_state.add_node_lat, st.session_state.add_node_lon],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        # Add marker at selected location
        folium.Marker(
            location=[st.session_state.add_node_lat, st.session_state.add_node_lon],
            popup=f"Tọa độ đã chọn<br>Lat: {st.session_state.add_node_lat:.6f}<br>Lon: {st.session_state.add_node_lon:.6f}",
            icon=folium.Icon(color='red')
        ).add_to(add_map)
        
        # Display map and get click data
        map_data = st_folium(add_map, width=None, height=300, key="add_node_map")
        
        # Update coordinates if map was clicked
        if map_data and map_data.get('last_clicked'):
            st.session_state.add_node_lat = map_data['last_clicked']['lat']
            st.session_state.add_node_lon = map_data['last_clicked']['lng']
            st.rerun()
        
        st.info(f"📍 Tọa độ hiện tại: **{st.session_state.add_node_lat:.6f}, {st.session_state.add_node_lon:.6f}**")
        
        with st.form("add_node_form"):
            new_node_id = st.text_input("Node ID *", placeholder="ví dụ: NODE_006")
            new_node_name = st.text_input("Tên Node *", placeholder="ví dụ: Jetson Nano - Cầu Giấy")
            
            col_lat, col_lon = st.columns(2)
            with col_lat:
                new_lat = st.number_input("Vĩ độ *", value=st.session_state.add_node_lat, format="%.6f", help="Hoặc click trên bản đồ để chọn")
            with col_lon:
                new_lon = st.number_input("Kinh độ *", value=st.session_state.add_node_lon, format="%.6f", help="Hoặc click trên bản đồ để chọn")
            
            new_status = st.selectbox("Trạng thái *", ["online", "offline"])
            new_cameras = st.number_input("Số lượng Camera", min_value=0, max_value=10, value=2)
            new_assists = st.selectbox("Hỗ trợ Node khác", ["yes", "no"])
            
            submit_add = st.form_submit_button("Thêm Node", use_container_width=True)
            
            if submit_add:
                if not new_node_id or not new_node_name:
                    st.error("Vui lòng điền đầy đủ các trường bắt buộc (đánh dấu *)")
                elif new_node_id in st.session_state.nodes_df['node_id'].values:
                    st.error(f"Node ID '{new_node_id}' đã tồn tại!")
                else:
                    # Validate coordinates
                    is_valid, error_msg = validate_coordinates(new_lat, new_lon)
                    if not is_valid:
                        st.error(error_msg)
                    else:
                        # Add new node
                        new_node = pd.DataFrame([{
                            'node_id': new_node_id,
                            'name': new_node_name,
                            'lat': new_lat,
                            'lon': new_lon,
                            'status': new_status,
                            'num_cameras': new_cameras,
                            'assists_others': new_assists
                        }])
                        
                        st.session_state.nodes_df = pd.concat(
                            [st.session_state.nodes_df, new_node],
                            ignore_index=True
                        )
                        
                        # Save to CSV
                        save_nodes(st.session_state.nodes_df)
                        
                        # Reset coordinates for next add
                        st.session_state.add_node_lat = MAP_DEFAULT_CENTER[0]
                        st.session_state.add_node_lon = MAP_DEFAULT_CENTER[1]
                        
                        log_info(f"Added new node: {new_node_id}")
                        st.success(f"Node '{new_node_name}' đã được thêm thành công!")
                        st.rerun()
    
    # ========================================================================
    # EDIT / DELETE NODE
    # ========================================================================
    with col_action2:
        st.markdown("### Chỉnh sửa / Xóa Node")
        
        if len(st.session_state.nodes_df) == 0:
            st.warning("Không có node nào để chỉnh sửa")
        else:
            # Map for selecting node to edit
            st.markdown("#### Chọn node cần chỉnh sửa trên bản đồ")
            st.caption("Click vào marker để chọn node muốn chỉnh sửa")
            
            # Create map with all nodes
            edit_select_map = create_base_map()
            
            # Add markers for all nodes
            for _, node in st.session_state.nodes_df.iterrows():
                marker_color = 'green' if node['status'] == 'online' else 'red'
                
                folium.Marker(
                    location=[node['lat'], node['lon']],
                    popup=f"<b>{node['name']}</b><br>ID: {node['node_id']}<br>Click để chỉnh sửa",
                    tooltip=f"{node['name']} - Click để chỉnh sửa",
                    icon=folium.Icon(color=marker_color)
                ).add_to(edit_select_map)
            
            # Display map and get click data
            edit_select_data = st_folium(edit_select_map, width=None, height=300, key="edit_select_map")
            
            # Find which node was clicked
            selected_node = None
            selected_node_id = None
            
            if edit_select_data and edit_select_data.get('last_object_clicked'):
                clicked = edit_select_data['last_object_clicked']
                clicked_lat = clicked.get('lat')
                clicked_lon = clicked.get('lng')
                
                # Find node at these coordinates (with small tolerance)
                tolerance = 0.0001
                for _, node in st.session_state.nodes_df.iterrows():
                    if (abs(node['lat'] - clicked_lat) < tolerance and 
                        abs(node['lon'] - clicked_lon) < tolerance):
                        selected_node = node
                        selected_node_id = node['node_id']
                        st.session_state.selected_edit_node_id = selected_node_id
                        st.session_state.edit_node_lat = float(node['lat'])
                        st.session_state.edit_node_lon = float(node['lon'])
                        break
            
            # Use previously selected node if exists
            if 'selected_edit_node_id' in st.session_state and selected_node is None:
                selected_node_id = st.session_state.selected_edit_node_id
                selected_node = st.session_state.nodes_df[
                    st.session_state.nodes_df['node_id'] == selected_node_id
                ].iloc[0]
                
                # Initialize edit coordinates
                if 'edit_node_lat' not in st.session_state:
                    st.session_state.edit_node_lat = float(selected_node['lat'])
                    st.session_state.edit_node_lon = float(selected_node['lon'])
            
            # Show edit form if node is selected
            if selected_node is not None:
                st.success(f"✅ Đã chọn node: **{selected_node['name']}** (ID: {selected_node_id})")
                
                # Map for editing location
                st.markdown("#### Chỉnh sửa vị trí")
                st.caption("Click vào bản đồ để thay đổi tọa độ")
                
                edit_map = folium.Map(
                    location=[st.session_state.edit_node_lat, st.session_state.edit_node_lon],
                    zoom_start=15,
                    tiles='OpenStreetMap'
                )
                
                # Add marker at selected location
                folium.Marker(
                    location=[st.session_state.edit_node_lat, st.session_state.edit_node_lon],
                    popup=f"{selected_node['name']}<br>Lat: {st.session_state.edit_node_lat:.6f}<br>Lon: {st.session_state.edit_node_lon:.6f}",
                    icon=folium.Icon(color='blue')
                ).add_to(edit_map)
                
                # Display map and get click data
                edit_map_data = st_folium(edit_map, width=None, height=300, key=f"edit_location_map_{selected_node_id}")
                
                # Update coordinates if map was clicked
                if edit_map_data and edit_map_data.get('last_clicked'):
                    st.session_state.edit_node_lat = edit_map_data['last_clicked']['lat']
                    st.session_state.edit_node_lon = edit_map_data['last_clicked']['lng']
                    st.rerun()
                
                st.info(f"📍 Tọa độ hiện tại: **{st.session_state.edit_node_lat:.6f}, {st.session_state.edit_node_lon:.6f}**")
                
                with st.form("edit_node_form"):
                    edit_name = st.text_input("Tên Node", value=selected_node['name'])
                    
                    col_lat2, col_lon2 = st.columns(2)
                    with col_lat2:
                        edit_lat = st.number_input("Vĩ độ", value=st.session_state.edit_node_lat, format="%.6f", help="Hoặc click trên bản đồ để chọn")
                    with col_lon2:
                        edit_lon = st.number_input("Kinh độ", value=st.session_state.edit_node_lon, format="%.6f", help="Hoặc click trên bản đồ để chọn")
                    
                    edit_status = st.selectbox(
                        "Trạng thái",
                        ["online", "offline"],
                        index=0 if selected_node['status'] == 'online' else 1
                    )
                    edit_cameras = st.number_input(
                        "Số lượng Camera",
                        min_value=0,
                        max_value=10,
                        value=int(selected_node['num_cameras'])
                    )
                    edit_assists = st.selectbox(
                        "Hỗ trợ Node khác",
                        ["yes", "no"],
                        index=0 if selected_node['assists_others'] == 'yes' else 1
                    )
                    
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        submit_edit = st.form_submit_button("Lưu Thay đổi", use_container_width=True)
                    
                    with col_btn2:
                        submit_delete = st.form_submit_button(
                            "Xóa Node",
                            use_container_width=True,
                            type="secondary"
                        )
                    
                    if submit_edit:
                        # Validate coordinates
                        is_valid, error_msg = validate_coordinates(edit_lat, edit_lon)
                        if not is_valid:
                            st.error(error_msg)
                        else:
                            # Update node
                            st.session_state.nodes_df.loc[
                                st.session_state.nodes_df['node_id'] == selected_node_id,
                                ['name', 'lat', 'lon', 'status', 'num_cameras', 'assists_others']
                            ] = [edit_name, edit_lat, edit_lon, edit_status, edit_cameras, edit_assists]
                            
                            # Save to CSV
                            save_nodes(st.session_state.nodes_df)
                            
                            # Clear selection
                            if 'selected_edit_node_id' in st.session_state:
                                del st.session_state.selected_edit_node_id
                            
                            log_info(f"Updated node: {selected_node_id}")
                            st.success(f"Node '{edit_name}' đã được cập nhật thành công!")
                            st.rerun()
                    
                    if submit_delete:
                        # Delete node
                        st.session_state.nodes_df = st.session_state.nodes_df[
                            st.session_state.nodes_df['node_id'] != selected_node_id
                        ]
                        
                        # Save to CSV
                        save_nodes(st.session_state.nodes_df)
                        
                        # Clear selection
                        if 'selected_edit_node_id' in st.session_state:
                            del st.session_state.selected_edit_node_id
                        
                        log_warning(f"Deleted node: {selected_node_id}")
                        st.warning(f"Node '{selected_node['name']}' đã được xóa!")
                        st.rerun()
            else:
                st.info("👆 Click vào một marker trên bản đồ để chọn node cần chỉnh sửa")


# ============================================================================
# TAB 2: CAMERA SETTINGS
# ============================================================================

with tab2:
    st.subheader("Quản lý Camera")
    st.markdown("Quản lý các camera kết nối với nodes")
    
    # Display cameras table
    st.markdown("### Các Camera hiện tại")
    
    # Prepare display dataframe with better formatting
    cameras_display = st.session_state.cameras.copy()
    
    # Join with nodes to show node names
    cameras_display = cameras_display.merge(
        st.session_state.nodes_df[['node_id', 'name']],
        on='node_id',
        how='left'
    )
    
    # Translate status to Vietnamese with color indicators
    status_map = {'online': '🟢 Trực tuyến', 'offline': '🔴 Ngoại tuyến'}
    cameras_display['status'] = cameras_display['status'].map(status_map)
    
    # Rename and reorder columns
    cameras_display = cameras_display[['camera_id', 'camera_name', 'name', 'status']]
    cameras_display.columns = ['Camera ID', 'Tên Camera', 'Node gốc', 'Trạng thái']
    
    # Display with custom styling
    st.dataframe(
        cameras_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Camera ID": st.column_config.TextColumn("Camera ID", width="small"),
            "Tên Camera": st.column_config.TextColumn("Tên Camera", width="medium"),
            "Node gốc": st.column_config.TextColumn("Node gốc", width="medium"),
            "Trạng thái": st.column_config.TextColumn("Trạng thái", width="small"),
        }
    )
    
    st.markdown("---")
    
    col_cam1, col_cam2 = st.columns(2)
    
    # ========================================================================
    # ADD CAMERA
    # ========================================================================
    with col_cam1:
        st.markdown("### Thêm Camera Mới")
        
        with st.form("add_camera_form"):
            new_cam_id = st.text_input("Camera ID *", placeholder="ví dụ: CAM_011")
            new_cam_name = st.text_input("Tên Camera *", placeholder="ví dụ: Cam 1")
            
            available_nodes = st.session_state.nodes_df['node_id'].tolist()
            new_cam_node = st.selectbox("Node gốc *", available_nodes)
            
            new_cam_status = st.selectbox("Trạng thái *", ["online", "offline"])
            
            submit_add_cam = st.form_submit_button("Thêm Camera", use_container_width=True)
            
            if submit_add_cam:
                if not new_cam_id or not new_cam_name:
                    st.error("Vui lòng điền đầy đủ các trường bắt buộc")
                elif new_cam_id in st.session_state.cameras['camera_id'].values:
                    st.error(f"Camera ID '{new_cam_id}' đã tồn tại!")
                else:
                    # Add new camera
                    new_camera = pd.DataFrame([{
                        'camera_id': new_cam_id,
                        'node_id': new_cam_node,
                        'camera_name': new_cam_name,
                        'status': new_cam_status
                    }])
                    
                    st.session_state.cameras = pd.concat(
                        [st.session_state.cameras, new_camera],
                        ignore_index=True
                    )
                    
                    log_info(f"Added new camera: {new_cam_id}")
                    st.success(f"Camera '{new_cam_name}' đã được thêm thành công!")
                    st.rerun()
    
    # ========================================================================
    # DELETE CAMERA
    # ========================================================================
    with col_cam2:
        st.markdown("### Xóa Camera")
        
        if len(st.session_state.cameras) == 0:
            st.warning("Không có camera nào để xóa")
        else:
            cam_to_delete = st.selectbox(
                "Chọn Camera để xóa",
                st.session_state.cameras['camera_id'].tolist(),
                key="delete_cam_select"
            )
            
            cam_info = st.session_state.cameras[
                st.session_state.cameras['camera_id'] == cam_to_delete
            ].iloc[0]
            
            st.info(f"**Camera:** {cam_info['camera_name']}\n\n**Node:** {cam_info['node_id']}")
            
            if st.button("Xác nhận Xóa", use_container_width=True, type="primary"):
                # Delete camera
                st.session_state.cameras = st.session_state.cameras[
                    st.session_state.cameras['camera_id'] != cam_to_delete
                ]
                
                log_warning(f"Deleted camera: {cam_to_delete}")
                st.warning(f"Camera '{cam_info['camera_name']}' đã được xóa!")
                st.rerun()


# ============================================================================
# TAB 3: DISPLAY SETTINGS
# ============================================================================

with tab3:
    st.subheader("Tùy chọn Hiển thị")
    st.markdown("Tùy chỉnh giao diện và hành vi của dashboard")
    
    st.markdown("### Hiển thị Sự kiện")
    
    col_disp1, col_disp2 = st.columns(2)
    
    with col_disp1:
        max_events = st.slider(
            "Số lượng Sự kiện Hiển thị Tối đa",
            min_value=5,
            max_value=50,
            value=st.session_state.config.get('max_events_display', 10),
            step=5,
            help="Số lượng sự kiện hiển thị trong nguồn cấp sự kiện"
        )
        st.session_state.config['max_events_display'] = max_events
    
    with col_disp2:
        refresh_options = {
            "30 giây": 30,
            "1 phút": 60,
            "2 phút": 120,
            "5 phút": 300
        }
        
        current_interval = st.session_state.config.get('refresh_interval', 30)
        current_label = next(
            (k for k, v in refresh_options.items() if v == current_interval),
            "30 giây"
        )
        
        refresh_interval = st.selectbox(
            "Khoảng thời gian Tự động Làm mới",
            list(refresh_options.keys()),
            index=list(refresh_options.keys()).index(current_label),
            help="Tần suất dashboard tự động làm mới"
        )
        st.session_state.config['refresh_interval'] = refresh_options[refresh_interval]
    
    st.markdown("---")
    
    st.markdown("### Tùy chọn Nâng cao")
    
    auto_refresh = st.checkbox(
        "Bật Tự động Làm mới",
        value=st.session_state.config.get('auto_refresh_enabled', True),
        help="Tự động làm mới nguồn cấp sự kiện theo khoảng thời gian đã chỉ định"
    )
    st.session_state.config['auto_refresh_enabled'] = auto_refresh
    
    st.markdown("---")
    
    # Save confirmation
    st.success("Cài đặt được tự động lưu")
    
    # Display current config
    with st.expander("Xem Cấu hình Hiện tại"):
        st.json(st.session_state.config)


# ============================================================================
# FOOTER
# ============================================================================

render_footer(f"**Cập nhật lần cuối:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

log_info("Settings page rendered successfully")
