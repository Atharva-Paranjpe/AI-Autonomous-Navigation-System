# 🚗 AI-Based Autonomous Navigation System

## 📌 Overview

This project is an AI-based autonomous navigation system that detects obstacles and determines a safe path using computer vision and real-time video processing.

It combines:

* Object detection (YOLOv8)
* Real-time video processing (OpenCV)
* Safety-based decision logic
* Path planning using grid-based analysis

---

## 🚀 Features

* 🚗 Real-time vehicle detection
* 🚶 Pedestrian detection with high safety priority
* 🛑 Automatic stop when pedestrians are present
* ⏱️ Timer-based delay before movement resumes
* 🟢 Dynamic path generation using dotted navigation path
* 🚫 Collision avoidance with safe distance from vehicles
* 🚴 Correct handling of cyclists (not treated as pedestrians)
* 🎥 Works on recorded video input

---

## 🧠 Tech Stack

* Python
* OpenCV
* NumPy
* Ultralytics YOLOv8

---

## 📂 Project Structure

```text
AI-Autonomous-Navigation-System/
│
├── main.py
├── data/
│   └── sample.mp4
│
├── models/
│   └── yolov8s.pt
│
├── output/
│   └── autonomous_navigation_demo.mp4
│
├── screenshots/
│   ├── normal_navigation.png
│   ├── pedestrian_detection.png
│   └── post_pedestrian_resume.png
```

---

## 📸 Screenshots

### 🚗 Normal Navigation

Shows safe path generation when the road is clear.

### 🚶 Pedestrian Detection

System detects pedestrian and stops immediately.

### ⏱️ After Pedestrian Walk

System resumes movement after safety delay.

---

## ▶️ How to Run

```bash
# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install ultralytics opencv-python numpy

# Run the system
python main.py
```

---

## 📊 Results

* Accurate real-time object detection
* Safe stopping behavior when pedestrians are detected
* Smooth recovery after delay (1 second timer)
* Stable path generation avoiding obstacles

---

## 🧠 Future Improvements

* Lane detection for better path alignment
* Integration with real-time camera input
* Advanced path planning (A*, reinforcement learning)
* Improved pedestrian intention prediction

---

## 👨‍💻 Author

Atharva Amol Paranjpe
