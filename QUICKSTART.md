# Quick Start Guide

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/quanngo018/smart_city_surveilance_system.git
   cd smart_city_surveilance_system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

### Generate Test Images (Optional)
To create sample images for testing:
```bash
python create_demo_images.py
```

This will create test images in `/tmp/demo_images/`

## Usage Examples

### Example 1: Analyze an Image
1. Click on "📷 Image Analysis" in the sidebar
2. Click "Browse files" and select an image
3. Adjust "Detection Sensitivity" if needed
4. View results with bounding boxes

### Example 2: Process a Video
1. Click on "🎥 Video Analysis" in the sidebar
2. Upload a video file (MP4, AVI, or MOV)
3. Set "Max Frames to Process" (recommended: 100 for quick testing)
4. Click "▶️ Process Video"
5. Watch real-time detection

### Example 3: View Analytics
1. After processing images/videos, click "📊 Dashboard"
2. View detection statistics (current, average, max, min)
3. Examine the detection history chart
4. Review recent detections in the table

## Tips

- **Lower sensitivity** (100-300): Detects smaller objects, may include noise
- **Medium sensitivity** (400-700): Balanced detection
- **Higher sensitivity** (800-2000): Only detects larger, more prominent objects

## Troubleshooting

### Issue: Dependencies not installing
**Solution:** Make sure you have Python 3.8+ and try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: OpenCV errors
**Solution:** If you're on Linux without display, use:
```bash
pip install opencv-python-headless
```

### Issue: Streamlit not starting
**Solution:** Check if port 8501 is available:
```bash
streamlit run app.py --server.port 8502
```

## Features Overview

| Feature | Description |
|---------|-------------|
| Image Analysis | Upload and analyze static images |
| Video Processing | Process video files frame-by-frame |
| Real-time Detection | See detections as they happen |
| Analytics Dashboard | View statistics and trends |
| Configurable Sensitivity | Adjust detection parameters |
| Detection History | Track objects over time |

## System Requirements

- Python 3.8 or higher
- 2GB RAM minimum (4GB recommended)
- Web browser (Chrome, Firefox, Safari, Edge)

## Next Steps

- Try different images and videos
- Experiment with sensitivity settings
- Monitor the analytics dashboard
- Customize detection parameters for your use case
