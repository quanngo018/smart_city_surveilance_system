"""
Smart City Surveillance System - Streamlit Web Demo
A web-based interface for smart city surveillance using Streamlit.
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
from detector import ObjectDetector, SurveillanceAnalyzer, draw_detections
import time


# Page configuration
st.set_page_config(
    page_title="Smart City Surveillance System",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'detector' not in st.session_state:
        st.session_state.detector = ObjectDetector(min_contour_area=500)
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = SurveillanceAnalyzer()
    if 'processed_frames' not in st.session_state:
        st.session_state.processed_frames = 0


def process_image(image: Image.Image, min_contour_area: int) -> tuple:
    """
    Process a single image for object detection.
    
    Args:
        image: PIL Image
        min_contour_area: Minimum contour area for detection
        
    Returns:
        Tuple of (processed image, statistics)
    """
    # Convert PIL to OpenCV format
    img_array = np.array(image)
    if len(img_array.shape) == 2:  # Grayscale
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
    else:  # RGB
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Create detector with custom settings
    detector = ObjectDetector(min_contour_area=min_contour_area)
    
    # Detect objects
    bboxes, _ = detector.detect_objects(img_array)
    
    # Draw detections
    output = draw_detections(img_array, bboxes)
    
    # Convert back to RGB for display
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    
    # Update analyzer
    st.session_state.analyzer.update(len(bboxes))
    
    return output, len(bboxes)


def process_video(video_file, min_contour_area: int, max_frames: int = 100):
    """
    Process video file for object detection.
    
    Args:
        video_file: Uploaded video file
        min_contour_area: Minimum contour area for detection
        max_frames: Maximum number of frames to process
    """
    # Save uploaded file temporarily
    with open("/tmp/temp_video.mp4", "wb") as f:
        f.write(video_file.read())
    
    # Open video
    cap = cv2.VideoCapture("/tmp/temp_video.mp4")
    
    # Create detector
    detector = ObjectDetector(min_contour_area=min_contour_area)
    
    # UI elements
    video_placeholder = st.empty()
    stats_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    frame_count = 0
    total_frames = min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), max_frames)
    
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect objects
        bboxes, _ = detector.detect_objects(frame)
        
        # Draw detections
        output = draw_detections(frame, bboxes)
        
        # Convert to RGB
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        
        # Update analyzer
        st.session_state.analyzer.update(len(bboxes))
        st.session_state.processed_frames += 1
        
        # Display frame
        video_placeholder.image(output, channels="RGB", use_container_width=True)
        
        # Display stats
        stats = st.session_state.analyzer.get_statistics()
        stats_placeholder.metric("Objects Detected", f"{stats['current']}")
        
        # Update progress
        frame_count += 1
        progress_bar.progress(frame_count / total_frames)
        
        # Small delay to make visualization visible
        time.sleep(0.03)
    
    cap.release()
    progress_bar.empty()


def create_statistics_chart():
    """Create a line chart showing detection history."""
    history = st.session_state.analyzer.get_history()
    
    if not history:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=history,
        mode='lines+markers',
        name='Objects Detected',
        line=dict(color='#1E88E5', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Detection History",
        xaxis_title="Frame",
        yaxis_title="Number of Objects",
        hovermode='x unified',
        template='plotly_white',
        height=300
    )
    
    return fig


def main():
    """Main application function."""
    # Initialize
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🏙️ Smart City Surveillance System</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to the Smart City Surveillance System demo! This application uses computer vision 
    to detect and track objects in images and videos, providing real-time analytics for 
    smart city monitoring.
    """)
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    
    mode = st.sidebar.radio(
        "Select Mode",
        ["📷 Image Analysis", "🎥 Video Analysis", "📊 Dashboard"],
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # Detection sensitivity
    min_contour_area = st.sidebar.slider(
        "Detection Sensitivity",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
        help="Lower values = more sensitive (may detect more noise)"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    This system uses background subtraction and contour detection 
    to identify moving objects in surveillance footage.
    
    **Features:**
    - Real-time object detection
    - Video processing
    - Statistical analysis
    - Detection history tracking
    """)
    
    # Main content area
    if mode == "📷 Image Analysis":
        st.header("Image Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Upload Image")
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['png', 'jpg', 'jpeg'],
                help="Upload an image for object detection"
            )
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Original Image", use_container_width=True)
        
        with col2:
            st.subheader("Detection Results")
            if uploaded_file is not None:
                with st.spinner("Processing image..."):
                    processed_img, num_objects = process_image(image, min_contour_area)
                    st.image(processed_img, caption="Processed Image", use_container_width=True)
                    
                    st.success(f"✅ Detected {num_objects} object(s)")
            else:
                st.info("👆 Upload an image to start detection")
    
    elif mode == "🎥 Video Analysis":
        st.header("Video Analysis")
        
        uploaded_video = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov'],
            help="Upload a video for object detection"
        )
        
        max_frames = st.slider(
            "Max Frames to Process",
            min_value=10,
            max_value=300,
            value=100,
            step=10,
            help="Limit processing for faster results"
        )
        
        if uploaded_video is not None:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button("▶️ Process Video", type="primary"):
                    with st.spinner("Processing video..."):
                        process_video(uploaded_video, min_contour_area, max_frames)
                        st.success("✅ Video processing complete!")
            
            with col2:
                st.metric("Frames Processed", st.session_state.processed_frames)
        else:
            st.info("👆 Upload a video to start detection")
    
    else:  # Dashboard
        st.header("Analytics Dashboard")
        
        stats = st.session_state.analyzer.get_statistics()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Objects", int(stats['current']))
        with col2:
            st.metric("Average Objects", f"{stats['average']:.1f}")
        with col3:
            st.metric("Maximum Objects", int(stats['max']))
        with col4:
            st.metric("Minimum Objects", int(stats['min']))
        
        st.markdown("---")
        
        # Chart
        chart = create_statistics_chart()
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("📊 Process images or videos to see detection history")
        
        # Detection history table
        if st.session_state.analyzer.get_history():
            st.subheader("Recent Detections")
            history = st.session_state.analyzer.get_history()
            df = pd.DataFrame({
                'Frame': range(1, len(history) + 1),
                'Objects Detected': history
            })
            st.dataframe(df.tail(20), use_container_width=True)


if __name__ == "__main__":
    main()
