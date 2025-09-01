# Bubbles and Ripples!  

## Background

I had this idea at brunch with my best friend. As I took a video of my South Delhi style cold coffee, I thought to myself,"There's something in these bubbles. I've got to play around with it."

---

## Overview  
This project overlays interactive **ripple effects** on top of a video of bubbles in an iced latte. The visuals are generated using Python and applied frame-by-frame, creating digital art that merges **motion graphics** with video.  

---

## Methods  
- **OpenCV** – for video loading, frame processing, and export.  
- **Custom Ripple Simulation** – expanding circles that mimic water ripples with collision detection.  
- **Bubble Detection** – Hough Circle Transform with intensity-based filtering for finding bubbles.  
- **Object Lifecycle Management** – recent-bubble memory and edge tolerance to control ripple creation.  

---

## Features  
- Detects bubbles and spawns ripples at their locations.  
- Ripple collisions cause interacting waves to disappear.  
- Adjustable parameters (growth rate, radius, edge tolerance, color).  
- Exports processed video with all visual effects embedded.
- Video transformation for optimized processing.

---

## 🛠️ Tech Stack  
- **OpenCV** (video processing, circle detection, drawing)  
- **NumPy** (distance calculations, matrix operations)  
- **Datetime & OS** (file handling and timestamped output naming)  
