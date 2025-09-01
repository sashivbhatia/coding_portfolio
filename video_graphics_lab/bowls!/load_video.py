#new best

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment
import os

# STEP 1: Import video
# Path to your video file
# IMPORTANT: Change this to your actual video file path!
video_path = "C:\GoProFootage\Bowls2.MOV"
#"C:\GoProFootage\Bowls_From_Youtube.mp4"
#"C:\\GoProFootage\\Bowls.MOV"
#"C:\GoProFootage\Bowls2.MOV"


# Create a VideoCapture object
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print(f"Error: Could not open video file at {video_path}. Please check the path.")
    exit()

# Get video properties for saving
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Build output filename
base_name = os.path.basename(video_path)
name_no_ext = os.path.splitext(base_name)[0]
output_path = os.path.join(os.path.dirname(video_path), f"{name_no_ext}_EDITED.mp4")

# Create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Tracker parameters
DIST_THRESHOLD = 80
MAX_MISSING_FRAMES = 30
MAX_TRACKS = 100

# Data structures
tracks = []
track_id_counter = 0

def create_kalman_filter(cx, cy):
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1,0,0,0],
                                     [0,1,0,0]], np.float32)
    kf.transitionMatrix = np.array([[1,0,1,0],
                                    [0,1,0,1],
                                    [0,0,1,0],
                                    [0,0,0,1]], np.float32)
    kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.05
    kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 5
    kf.statePre = np.array([[cx], [cy], [0], [0]], np.float32)
    kf.statePost = np.array([[cx], [cy], [0], [0]], np.float32)
    return kf

# Main video processing loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 120])
    upper_white = np.array([180, 80, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)

    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    kernel = np.ones((7,7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    for c in contours:
        if cv2.contourArea(c) > 600:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                detections.append((cx, cy))

    detections = detections[:MAX_TRACKS]

    predictions = []
    for t in tracks:
        pred = t["kf"].predict()
        predictions.append((int(pred[0]), int(pred[1])))

    if predictions and detections:
        cost_matrix = np.zeros((len(predictions), len(detections)))
        for i, (px, py) in enumerate(predictions):
            for j, (dx, dy) in enumerate(detections):
                cost_matrix[i, j] = np.linalg.norm(np.array([px, py]) - np.array([dx, dy]))
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
    else:
        row_ind, col_ind = np.array([]), np.array([])

    assigned_tracks = set()
    assigned_detections = set()

    for r, c in zip(row_ind, col_ind):
        if cost_matrix[r, c] < DIST_THRESHOLD:
            t = tracks[r]
            t["kf"].correct(np.array([[np.float32(detections[c][0])],
                                      [np.float32(detections[c][1])]]))
            t["trail"].append(detections[c])
            t["missed"] = 0
            assigned_tracks.add(r)
            assigned_detections.add(c)

    for i, t in enumerate(tracks):
        if i not in assigned_tracks:
            t["missed"] += 1

    tracks = [t for t in tracks if t["missed"] <= MAX_MISSING_FRAMES]

    for i, d in enumerate(detections):
        if i not in assigned_detections:
            kf = create_kalman_filter(d[0], d[1])
            tracks.append({
                "id": track_id_counter,
                "kf": kf,
                "trail": [d],
                "missed": 0
            })
            track_id_counter += 1

    for t in tracks:
        cx, cy = int(t["kf"].statePost[0]), int(t["kf"].statePost[1])

        if t["trail"]:
            draw_x, draw_y = t["trail"][-1]
            cv2.circle(frame, (draw_x, draw_y), 30, (0,255,0), 2)

        cv2.circle(frame, (draw_x, draw_y), 3, (0,0,255), -1)

        if len(t["trail"]) > 1:
            for i in range(1, len(t["trail"])):
                cv2.line(frame, t["trail"][i-1], t["trail"][i], (0,0,255), 3)

        cv2.putText(frame, f"ID: {t['id']}", (cx+5, cy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Tracking", frame)
    out.write(frame)   # <-- Write this frame to the output video

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
out.release()   # <-- Properly close the output file
cv2.destroyAllWindows()