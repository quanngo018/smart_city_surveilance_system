# Smart City Surveillance System 🏙️

A web-based surveillance system demo built with Streamlit for smart city monitoring. This application provides real-time object detection and tracking capabilities using computer vision.

## Features

- 📷 **Image Analysis**: Upload and analyze static images for object detection
- 🎥 **Video Processing**: Process video files with real-time object tracking
- 📊 **Analytics Dashboard**: View detection statistics and history
- ⚙️ **Configurable Detection**: Adjust sensitivity for different scenarios
- 📈 **Visual Analytics**: Interactive charts showing detection trends

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/quanngo018/smart_city_surveilance_system.git
cd smart_city_surveilance_system
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

Start the Streamlit web application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Using the Application

#### Image Analysis Mode
1. Select "📷 Image Analysis" from the sidebar
2. Upload an image (PNG, JPG, or JPEG)
3. View the detection results with bounding boxes
4. Adjust detection sensitivity using the slider

#### Video Analysis Mode
1. Select "🎥 Video Analysis" from the sidebar
2. Upload a video file (MP4, AVI, or MOV)
3. Set the maximum number of frames to process
4. Click "▶️ Process Video" to start analysis
5. Watch real-time detection results

#### Dashboard Mode
1. Select "📊 Dashboard" from the sidebar
2. View detection statistics (current, average, max, min)
3. Analyze detection history with interactive charts
4. Review recent detection data in table format

## Technology Stack

- **Streamlit**: Web application framework
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computing
- **Pillow**: Image handling
- **Pandas**: Data analysis
- **Plotly**: Interactive visualizations

## How It Works

The system uses background subtraction (MOG2 algorithm) combined with contour detection to identify moving objects in surveillance footage:

1. **Background Subtraction**: Separates foreground objects from background
2. **Morphological Operations**: Reduces noise and improves detection quality
3. **Contour Detection**: Identifies object boundaries
4. **Bounding Box Extraction**: Draws boxes around detected objects
5. **Statistics Tracking**: Maintains history for analytics

## Configuration

Adjust detection parameters in the sidebar:

- **Detection Sensitivity**: Lower values detect smaller objects but may include more noise (100-2000 range)
- **Max Frames**: Limit video processing for faster results (10-300 frames)

## Project Structure

```
smart_city_surveilance_system/
├── app.py              # Main Streamlit application
├── detector.py         # Object detection and analysis modules
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Streamlit for rapid web app development
- Uses OpenCV for computer vision capabilities
- Designed for smart city surveillance applications