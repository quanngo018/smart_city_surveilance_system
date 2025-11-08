"""
Smart City Monitoring System - Main Application Entry Point (Intro Page)
A Streamlit-based web application for monitoring smart city infrastructure.
"""

import streamlit as st
from pathlib import Path

# UI Components
from ui.theme_manager import apply_page_config, apply_theme
from ui.components import (
    render_page_header,
    render_metric_card,
    render_columns,
    render_expander,
    render_divider,
)

# Config and Utils
from config.settings import APP_CONFIG
from utils.logger import setup_logger, log_info, LogOperation
from utils.helpers import init_session_state


# ============================================================================
# LOGGER SETUP
# ============================================================================

logger = setup_logger(
    name="smart_city_app",
    log_level="INFO",
    log_file=Path(__file__).parent / "logs" / "app.log"
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

apply_page_config()
apply_theme()


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_app_state() -> None:
    """Initialize all session state variables."""
    
    # Navigation state
    init_session_state('current_page', 'Giới thiệu')
    
    # Map click coordinates
    init_session_state('selected_lat', None)
    init_session_state('selected_lon', None)
    
    # Settings state
    init_session_state('settings_changed', False)
    
    # Data refresh timestamp
    init_session_state('last_refresh', None)
    
    log_info("Session state initialized")


initialize_app_state()


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.title(APP_CONFIG['title'])
    st.caption(f"Version {APP_CONFIG['version']}")
    st.caption("Built with Streamlit")
    
    render_divider()
    
    # Navigation info
    st.markdown("""
    ### Điều hướng
    
    Sử dụng menu bên trái để chuyển đổi giữa các trang:
    
    - **Giới thiệu**: Tổng quan hệ thống (trang này)
    - **Bảng điều khiển**: Theo dõi sự kiện thời gian thực
    - **Phân tích**: Xem thống kê và báo cáo
    - **Cài đặt**: Quản lý cấu hình hệ thống
    """)
    
    render_divider()
    
    # System information
    st.markdown("### Thông tin hệ thống")
    st.info(f"""
    **Tên hệ thống:** {APP_CONFIG['system_name']}  
    **Ngôn ngữ:** Tiếng Việt
    """)
    
    render_divider()
    
    # Footer
    st.caption("© EDABK-AIOT - Smart City Monitoring System")


# ============================================================================
# MAIN CONTENT
# ============================================================================

with LogOperation("Rendering Introduction page"):
    
    # Page header
    render_page_header(
        title="Hệ thống Giám sát Thành phố Thông minh",
        description="Giải pháp giám sát và quản lý cơ sở hạ tầng thành phố thông minh"
    )
    
    st.markdown("""
    ### Hướng dẫn sử dụng
    
    Hệ thống này cung cấp giao diện web để giám sát và quản lý cơ sở hạ tầng thành phố thông minh.
    
    #### Các tính năng chính:
    
    1. **Bảng điều khiển** 
       - Theo dõi sự kiện thời gian thực trên bản đồ
       - Xem vị trí các node và camera
       - Nhận thông báo về các sự kiện quan trọng
    
    2. **Phân tích** 
       - Xem biểu đồ thống kê
       - Phân tích xu hướng sự kiện
       - Báo cáo theo địa điểm và loại sự kiện
    
    3. **Cài đặt** 
       - Quản lý cấu hình node
       - Cấu hình camera
       - Tùy chỉnh hiển thị giao diện
    
    ---
    
    ### Bắt đầu
    
    Sử dụng menu điều hướng ở phía bên trái để truy cập các tính năng khác nhau của hệ thống.
    
    Mỗi trang được thiết kế để cung cấp thông tin và công cụ cụ thể cho nhiệm vụ giám sát và quản lý.
    """)
    
    # Display quick stats
    render_divider()
    
    col1, col2, col3 = render_columns(3)
    
    with col1:
        render_metric_card(
            label="Tổng số Node",
            value="5",
            help_text="Tổng số node đang được giám sát"
        )
    
    with col2:
        render_metric_card(
            label="Node trực tuyến",
            value="4",
            delta="+1",
            help_text="Số node đang hoạt động"
        )
    
    with col3:
        render_metric_card(
            label="Sự kiện hôm nay",
            value="10",
            delta="+3",
            help_text="Số sự kiện được ghi nhận trong ngày"
        )
    
    render_divider()
    
    # Tips section
    with render_expander("Mẹo sử dụng", expanded=False):
        st.markdown("""
        - **Bản đồ tương tác**: Click vào các điểm đánh dấu trên bản đồ để xem thông tin chi tiết
        - **Lọc dữ liệu**: Sử dụng các bộ lọc để thu hẹp dữ liệu hiển thị
        - **Tự động làm mới**: Một số trang tự động làm mới để hiển thị dữ liệu mới nhất
        - **Chọn tọa độ**: Trong trang Cài đặt, click trên bản đồ để chọn tọa độ chính xác
        - **Xuất dữ liệu**: Sử dụng nút xuất để tải dữ liệu dưới dạng CSV
        """)
    
    log_info("Introduction page rendered successfully")
