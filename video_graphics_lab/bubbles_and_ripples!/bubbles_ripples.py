import cv2
import numpy as np
import os
from datetime import datetime

# ----------------------------
# Ripple model
# ----------------------------
class Ripple:
    def __init__(self, x, y, max_radius=200, growth_rate=0.2, edge_tol=4):
        self.x = int(x)
        self.y = int(y)
        self.radius = 0.0
        self.max_radius = float(max_radius)
        self.growth_rate = float(growth_rate)
        self.edge_tol = float(edge_tol)  # tolerance for "edge touching"
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.radius += self.growth_rate
        if self.radius >= self.max_radius:
            self.alive = False

    def draw(self, frame):
        if self.alive:
            cv2.circle(frame, (self.x, self.y), int(self.radius), (255, 0, 0), 2)

    def collides_with(self, other):
        """
        Option B: Only treat as collision when the two ripple *edges* meet externally:
            distance(center1, center2) ≈ r1 + r2 (within a small tolerance).
        If one ripple is entirely inside the other (internal overlap), we ignore it.
        """
        if not (self.alive and other.alive):
            return False

        dist = np.hypot(self.x - other.x, self.y - other.y)

        # External tangency (edge-to-edge from outside)
        external_touch = abs(dist - (self.radius + other.radius)) <= self.edge_tol

        # Internal overlap or internal tangency should NOT count as a collision here
        # (dist <= |r1 - r2|), so we explicitly ignore those.
        internal_overlap = dist <= abs(self.radius - other.radius) + self.edge_tol

        return external_touch and not internal_overlap


# ----------------------------
# Video processing
# ----------------------------
def process_video(input_path, scale=0.5):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    out_name = f"{timestamp}_{base_name}_ripples.mp4"

    writer = cv2.VideoWriter(out_name, fourcc, fps, (width, height))

    ripples = []

    # Short-term memory so we don't spawn the same ripple every frame
    # Each entry: {"x": int, "y": int, "ttl": int}
    recent_bubbles = []
    recent_ttl = 10          # frames to suppress duplicates
    suppress_radius = 12     # pixels within which a new detection is considered "same bubble"

    # Hough & filter tuning
    dp = 1.15
    minDist = 8
    param1 = 70      # Canny high threshold (edge detector)
    param2 = 20      # Accumulator threshold (lower -> more circles)
    minRadius = 1    # << detect very small bubbles
    maxRadius = 26

    # intensity (area) filter tuning
    intensity_delta = 8      # inner must be at least this much darker than outer
    ring_scale = 1.6         # outer ring radius = r * ring_scale (for background sampling)
    min_valid_r = 1          # skip degenerate 0-radius circles

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- Downscale for speed
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        # --- Grayscale + local contrast boost (helps tiny bubbles)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray_eq = clahe.apply(gray)

        # --- Light denoising
        blur = cv2.medianBlur(gray_eq, 5)

        # --- Circle detection
        circles = cv2.HoughCircles(
            blur, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist,
            param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius
        )

        # --- Update & age-out bubble memory
        for b in recent_bubbles:
            b["ttl"] -= 1
        recent_bubbles = [b for b in recent_bubbles if b["ttl"] > 0]

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for (x, y, r) in circles[0, :]:
                if r < min_valid_r:
                    continue

                # ----- Intensity (area) filter: bubble interior darker than surroundings
                # Build inner mask and a thin outer ring
                r_out = max(r + 1, int(r * ring_scale))
                mask_inner = np.zeros_like(gray, dtype=np.uint8)
                mask_outer = np.zeros_like(gray, dtype=np.uint8)
                cv2.circle(mask_inner, (x, y), int(r), 255, -1)
                cv2.circle(mask_outer, (x, y), int(r_out), 255, -1)
                mask_ring = cv2.subtract(mask_outer, mask_inner)

                inner_mean = cv2.mean(gray, mask=mask_inner)[0]
                outer_mean = cv2.mean(gray, mask=mask_ring)[0]

                # keep only if inner is significantly darker
                if not (outer_mean - inner_mean >= intensity_delta):
                    continue

                # ----- Suppress duplicates across nearby frames
                if any(np.hypot(x - b["x"], y - b["y"]) < suppress_radius for b in recent_bubbles):
                    continue

                # New bubble → spawn a ripple and remember it briefly
                ripples.append(Ripple(x, y, max_radius=200, growth_rate=3, edge_tol=4))
                recent_bubbles.append({"x": int(x), "y": int(y), "ttl": recent_ttl})

        # --- Update ripples
        for ripple in ripples:
            ripple.update()

        # --- Handle collisions (Option B: external edge contact only)
        # Note: operate on indices to avoid modifying the list while iterating
        alive_indices = [i for i, r in enumerate(ripples) if r.alive]
        for idx_i in range(len(alive_indices)):
            i = alive_indices[idx_i]
            ri = ripples[i]
            if not ri.alive:
                continue
            for idx_j in range(idx_i + 1, len(alive_indices)):
                j = alive_indices[idx_j]
                rj = ripples[j]
                if not rj.alive:
                    continue
                if ri.collides_with(rj):
                    ri.alive = False
                    rj.alive = False

        # --- Draw ripples
        for ripple in ripples:
            ripple.draw(frame)

        # --- Keep only alive ripples
        ripples = [r for r in ripples if r.alive]

        writer.write(frame)

    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print(f"✅ Done! Saved ripple-clash video to {out_name}")


if __name__ == "__main__":
    input_file = "C:\GoProFootage\iced_latte.mp4"
    process_video(input_file, scale=0.5)
