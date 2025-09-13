# Theft Detection System

Real-time theft detection using optimized YOLO model with email alerts and performance monitoring.

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Yasssh2123/Theft_Detection_System.git
cd Theft_Detection_System
```

### 2. Install Dependencies

```bash
pip install opencv-python ultralytics openvino
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Model Optimization (Required First Step)

```bash
python optimize_model.py
```

### 2. Run Detection System

```bash
python theft_detection.py
```



## Configuration

Before running the system, update these variables:

### optimize_model.py
- **Line 40**: Update model path
  ```python
  model_path = r"C:\your\path\to\best.pt"
  ```
- **Line 18**: Update dataset path
  ```python
  data = r"C:\your\path\to\data.yaml"
  ```

### theft_detection.py
- **Lines 15-17**: Email credentials
  ```python
  sender_email = "your_email@gmail.com"
  sender_password = "your_app_password"
  receiver_email = "recipient@gmail.com"
  ```
- **Line 130**: Optimized model path
  ```python
  detector = TheftDetector(r'C:\path\to\best_int8_openvino_model')
  ```
- **Line 131**: Video source
  ```python
  detector.process_video(0)  # 0=webcam, 'video.mp4', or any URL
  ```

### Optional Settings
- **Line 58**: Alert cooldown (default: 30 seconds)
- **Line 75**: Detection confidence (default: 0.5)

## Features

- INT8 quantized model for 3-5x faster CPU performance
- Real-time webcam processing with FPS monitoring
- **Non-blocking email alerts** with 30-second cooldown
- JSON detection logging with timestamps
- Visual bounding boxes with confidence scores
- Asynchronous alert system (no video freezing)

## File Structure

```
Theft_Detection_System/
├── optimize_model.py           # Model optimization
├── theft_detection.py          # Main detection system
├── samples/                    # Test videos
├── Theft_Detection_e200_smallModel_FYP_Dataset/
│   └── weights/
│       ├── best.pt            # Original model
│       └── best_int8_openvino_model/  # Optimized model
└── detections.json            # Detection log
```

## Usage

### Video Input Sources
```python
# Webcam (default)
detector.process_video(0)

# Local video file
detector.process_video('samples/input1.mp4')

# YouTube/Online video URL
detector.process_video('https://www.youtube.com/watch?v=VIDEO_ID')

# RTSP camera stream
detector.process_video('rtsp://username:password@camera_ip:port/stream')

# HTTP video stream
detector.process_video('http://example.com/video.mp4')

# IP camera
detector.process_video('http://192.168.1.100:8080/video')
```

### Controls
- Press **'q'** to quit

## Detection Classes

- **NORMAL**: Regular activity (green box)
- **THEFT**: Suspicious activity (red box + email alert)

## Performance

| Model Type | FPS | Memory Usage |
|------------|-----|--------------|
| Original   | 5-10 | 100% |
| Optimized  | 15-30 | 60% reduction |

## Troubleshooting

1. Run `optimize_model.py` first
2. Check model paths are correct
3. Use Gmail app password for email
4. Try different camera indices (0, 1, 2)

## Requirements

- Python 3.8+
- OpenCV 4.5+
- Ultralytics YOLO
- OpenVINO toolkit
- Gmail account with app password