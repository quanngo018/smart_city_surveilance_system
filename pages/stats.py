"""
Analytics Page - Smart City Monitoring System
Statistical analysis and reporting of event data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta

# Force Plotly to use default template (prevents Streamlit theme interference)
pio.templates.default = "plotly"

# UI Components
from ui.theme_manager import apply_page_config, get_chart_colors
from ui.components import (
    render_page_header,
    render_section_header,
    render_styled_dataframe,
    render_columns,
    render_divider,
    render_selectbox,
)

# Config and Utils
from config.settings import EVENT_TYPES
from utils.data_loader import initialize_data
from utils.helpers import init_session_state
from utils.logger import log_info, LogOperation


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

apply_page_config(page_title="Smart City Monitoring System - Phân tích")
# Note: apply_theme() is disabled to prevent chart visibility issues


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_stats_state() -> None:
    """Initialize stats session state."""
    
    # Load data
    init_session_state('nodes_df', None)
    init_session_state('events_df', None)
    
    if st.session_state.nodes_df is None or st.session_state.events_df is None:
        with LogOperation("Loading data for Analytics page"):
            nodes_df, events_df = initialize_data()
            st.session_state.nodes_df = nodes_df
            st.session_state.events_df = events_df


initialize_stats_state()


# ============================================================================
# HEADER
# ============================================================================

render_page_header(
    title="Bảng Thống Kê",
    description="Phân tích thống kê và thông tin chi tiết từ dữ liệu giám sát"
)


# ============================================================================
# FILTERS
# ============================================================================

render_section_header("Bộ lọc")

# Event type names in Vietnamese - from config
event_type_names = EVENT_TYPES

col_filter1, col_filter2 = render_columns(2)

with col_filter1:
    # Time range filter
    time_range = st.selectbox(
        "Khoảng thời gian",
        ["12 giờ qua", "24 giờ qua", "7 ngày qua", "30 ngày qua", "Tất cả"],
        index=0
    )

with col_filter2:
    # Event type filter - only valid types from config
    valid_event_types = list(EVENT_TYPES.keys())
    unique_types = st.session_state.events_df['event_type'].unique().tolist()
    filtered_types = [t for t in unique_types if t in valid_event_types]
    
    event_options = ['Tất cả'] + [event_type_names.get(t, t) for t in sorted(filtered_types)]
    selected_type_display = st.selectbox("Loại sự kiện", event_options)
    
    # Map back to English key
    if selected_type_display == 'Tất cả':
        selected_type = 'All'
    else:
        selected_type = next((k for k, v in event_type_names.items() if v == selected_type_display), 'All')


# Apply filters
filtered_df = st.session_state.events_df.copy()

# Filter to only show valid event types
valid_event_types = list(EVENT_TYPES.keys())
filtered_df = filtered_df[filtered_df['event_type'].isin(valid_event_types)]

# Time range filter
if time_range == "12 giờ qua":
    cutoff = datetime.now() - timedelta(hours=12)
    filtered_df = filtered_df[filtered_df['timestamp'] >= cutoff]
elif time_range == "24 giờ qua":
    cutoff = datetime.now() - timedelta(hours=24)
    filtered_df = filtered_df[filtered_df['timestamp'] >= cutoff]
elif time_range == "7 ngày qua":
    cutoff = datetime.now() - timedelta(days=7)
    filtered_df = filtered_df[filtered_df['timestamp'] >= cutoff]
elif time_range == "30 ngày qua":
    cutoff = datetime.now() - timedelta(days=30)
    filtered_df = filtered_df[filtered_df['timestamp'] >= cutoff]


# Event type filter
if selected_type != 'All':
    filtered_df = filtered_df[filtered_df['event_type'] == selected_type]

st.markdown("---")


# ============================================================================
# SUMMARY METRICS
# ============================================================================

col1, col2, col3 = st.columns(3)

with col1:
    total_events = len(filtered_df)
    st.metric("Tổng số sự kiện", total_events)

with col2:
    pending_count = len(filtered_df[filtered_df['status'] == 'pending'])
    st.metric("Đang chờ xử lý", pending_count)

with col3:
    resolved_count = len(filtered_df[filtered_df['status'] == 'resolved'])
    st.metric("Đã xử lý", resolved_count)

render_divider()


# ============================================================================
# CHART 1: EVENTS OVER TIME
# ============================================================================

render_section_header("Sự kiện theo thời gian")

if len(filtered_df) == 0:
    st.info("Không có dữ liệu cho bộ lọc đã chọn")
else:
    # Prepare data for time series
    events_by_time = filtered_df.copy()
    events_by_time['date'] = events_by_time['timestamp'].dt.date
    events_by_time['hour'] = events_by_time['timestamp'].dt.hour
    
    # Aggregate by date
    time_series = events_by_time.groupby('date').size().reset_index(name='count')
    
    # Create line chart
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['count'],
        mode='lines+markers',
        name='Số lượng sự kiện',
        line=dict(color=get_chart_colors()[1], width=3),
        marker=dict(
            color=get_chart_colors()[1],
            size=8,
            line=dict(color='#000000', width=1)
        )
    ))
    
    fig_time.update_layout(
        title='Số lượng sự kiện theo ngày',
        xaxis_title='Ngày',
        yaxis_title='Số lượng sự kiện',
        height=400,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#000000', size=12),
        xaxis=dict(gridcolor='#e5e7eb'),
        yaxis=dict(gridcolor='#e5e7eb')
    )
    
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Hourly distribution
    st.markdown("#### Sự kiện theo giờ trong ngày")
    
    hourly_dist = events_by_time.groupby('hour').size().reset_index(name='count')
    
    fig_hourly = px.bar(
        hourly_dist,
        x='hour',
        y='count',
        title='Phân bố sự kiện theo giờ',
        labels={'hour': 'Giờ trong ngày', 'count': 'Số lượng sự kiện'},
        color_discrete_sequence=[get_chart_colors()[3]]
    )
    
    fig_hourly.update_traces(
        marker=dict(color=get_chart_colors()[3], line=dict(color='#000000', width=1))
    )
    
    fig_hourly.update_layout(
        height=350,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        xaxis=dict(gridcolor='#e5e7eb'),
        yaxis=dict(gridcolor='#e5e7eb')
    )
    
    st.plotly_chart(fig_hourly, use_container_width=True)


render_divider()


# ============================================================================
# CHART 2: EVENTS BY LOCATION
# ============================================================================

col_chart1, col_chart2 = render_columns(2)

with col_chart1:
    render_section_header("Sự kiện theo vị trí")
    
    if len(filtered_df) == 0:
        st.info("Không có dữ liệu")
    else:
        location_counts = filtered_df['location'].value_counts().reset_index()
        location_counts.columns = ['location', 'count']
        
        fig_location = px.bar(
            location_counts,
            x='location',
            y='count',
            title='Vị trí có nhiều sự kiện nhất',
            labels={'location': 'Vị trí', 'count': 'Số lượng sự kiện'},
            color_discrete_sequence=[get_chart_colors()[0]]
        )
        
        fig_location.update_traces(
            marker=dict(color=get_chart_colors()[0], line=dict(color='#000000', width=1))
        )
        
        fig_location.update_layout(
            height=400,
            xaxis_tickangle=-45,
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        
        st.plotly_chart(fig_location, use_container_width=True)


# ============================================================================
# CHART 3: EVENT TYPE DISTRIBUTION
# ============================================================================

with col_chart2:
    render_section_header("Phân bố loại sự kiện")
    
    if len(filtered_df) == 0:
        st.info("Không có dữ liệu")
    else:
        type_counts = filtered_df['event_type'].value_counts().reset_index()
        type_counts.columns = ['event_type', 'count']
        
        # Use Vietnamese names
        type_counts['event_type_display'] = type_counts['event_type'].map(
            lambda x: event_type_names.get(x, x.replace('_', ' ').title())
        )
        
        fig_types = px.pie(
            type_counts,
            values='count',
            names='event_type_display',
            title='Phân bố theo loại',
            color_discrete_sequence=get_chart_colors()
        )
        
        fig_types.update_traces(
            textfont=dict(size=12),
            marker=dict(line=dict(color='#FFFFFF', width=2)),
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig_types.update_layout(
            height=400,
            paper_bgcolor='#ffffff',
            showlegend=True
        )
        
        st.plotly_chart(fig_types, use_container_width=True)


render_divider()


# ============================================================================
# DETAILED EVENT TABLE
# ============================================================================

render_section_header("Nhật ký sự kiện chi tiết")

if len(filtered_df) == 0:
    st.info("Không có sự kiện nào phù hợp với bộ lọc đã chọn")
else:
    # Prepare display dataframe
    display_df = filtered_df[[
        'event_id', 'timestamp', 'location', 'event_type', 'status'
    ]].copy()
    
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Map to Vietnamese names with emoji
    event_type_emoji = {
        'suspicious_gathering': 'Phát hiện có náo loạn, xô xát',
        'person_fall': 'Phát hiện có người ngã',
        'suspicious_person': 'Phát hiện có người khả nghi'
    }
    display_df['event_type'] = display_df['event_type'].map(
        lambda x: event_type_emoji.get(x, event_type_names.get(x, x.replace('_', ' ').title()))
    )
    
    # Map status to Vietnamese with emoji
    status_vn_map = {
        'pending': 'Đang chờ',
        'resolved': 'Đã xử lý',
        'false_alarm': 'Báo động giả'
    }
    display_df['status'] = display_df['status'].map(status_vn_map)
    
    display_df.columns = ['ID Sự kiện', 'Thời gian', 'Vị trí', 'Loại sự kiện', 'Trạng thái']
    
    # Display with styled dataframe component
    render_styled_dataframe(
        display_df,
        column_config={
            "ID Sự kiện": st.column_config.TextColumn("ID Sự kiện", width="small"),
            "Thời gian": st.column_config.TextColumn("Thời gian", width="medium"),
            "Vị trí": st.column_config.TextColumn("Vị trí", width="large"),
            "Loại sự kiện": st.column_config.TextColumn("Loại sự kiện", width="large"),
            "Trạng thái": st.column_config.TextColumn("Trạng thái", width="small"),
        }
    )

    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Tải xuống dữ liệu đã lọc (CSV)",
        data=csv,
        file_name=f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption(f"**Dữ liệu tính đến:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Tổng số bản ghi:** {len(st.session_state.events_df)}")

log_info("Analytics page rendered successfully")
