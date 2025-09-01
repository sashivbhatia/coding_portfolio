# Bowls!  

This project explores computer vision techniques for detecting and tracking bowls in video footage.  
The program identifies moving bowls, assigns each one a unique ID, and visualizes their paths with trails and labels.  

---

## Background
The idea for this project came on a visit to Bourse de Commerce in Paris, France where I got to see Céleste Boursier- Mougenot's clinamen exhibit. I thought to myself,"Wouldn't it be cool if I could track the path these bowls take while floating?" 

---

## 📖 Overview  
The goal of this project is to build a robust object tracker that can follow bowls across frames in a video.  
By combining detection, motion prediction, and assignment algorithms, the tracker maintains consistent IDs for each bowl even when objects move, overlap, or temporarily disappear.  

---

## ⚙️ Methods  
- **Preprocessing:**  
  - Converted video frames to HSV color space for more reliable color-based filtering.  
  - Applied morphological operations (opening/closing) and Gaussian blur to reduce noise.  

- **Object Detection:**  
  - Used contour detection to find bowl-shaped regions.  
  - Filtered out small contours by applying an area threshold.  

- **Tracking and Prediction:**  
  - Implemented a **Kalman Filter** for each bowl to predict its motion across frames.  
  - Matched predictions to new detections using the **Hungarian Algorithm**.  
  - Managed object lifecycles, handling new bowls, missed detections, and disappearing objects.  

- **Visualization:**  
  - Drew circles around detected bowls.  
  - Assigned unique IDs and displayed them alongside tracked positions.  
  - Rendered red trails showing the movement history of each bowl.  

---

## 🎥 Output  
The program processes the input video and generates a new video with:  
- Green circles highlighting tracked bowls  
- Red trails indicating movement paths  
- Unique IDs labeling each object  

This creates a clear, dynamic visualization of how the bowls move across the scene that I think looks pretty cool.

---

## 🛠️ Tech Stack   
- **OpenCV** (image processing, drawing, video handling)  
- **NumPy** (mathematical operations)  
- **SciPy** (Hungarian algorithm for optimal assignment)  
