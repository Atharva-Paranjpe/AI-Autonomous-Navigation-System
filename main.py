import cv2
import numpy as np
import time
from ultralytics import YOLO

model = YOLO("models/yolov8s.pt")
cap = cv2.VideoCapture("data/sample.mp4")

# -----------------------------
# TIMER (2 seconds)
# -----------------------------
pedestrian_timer = 0
STOP_DURATION = 1.0

def overlap_ratio(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b

    inter_w = max(0, min(ax2, bx2) - max(ax1, bx1))
    inter_h = max(0, min(ay2, by2) - max(ay1, by1))
    inter_area = inter_w * inter_h

    a_area = (ax2 - ax1) * (ay2 - ay1)
    if a_area <= 0:
        return 0.0

    return inter_area / a_area


while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    results = model(frame, conf=0.35)

    vehicles = []
    bicycles = []
    persons = []

    obstacle_mask = np.zeros((h, w), dtype=np.uint8)

    # -----------------------------
    # DETECTION
    # -----------------------------
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if conf < 0.35:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if cls in [2, 3, 5, 7]:
                vehicles.append((x1, y1, x2, y2))
            elif cls == 1:
                bicycles.append((x1, y1, x2, y2))
            elif cls == 0:
                persons.append((x1, y1, x2, y2))

    # -----------------------------
    # VEHICLE MASK (SAFE DISTANCE)
    # -----------------------------
    for (x1, y1, x2, y2) in vehicles + bicycles:
        expand = 30
        x1e = max(0, x1 - expand)
        y1e = max(0, y1 - expand)
        x2e = min(w, x2 + expand)
        y2e = min(h, y2 + expand)

        cv2.rectangle(frame, (x1e, y1e), (x2e, y2e), (0, 255, 0), 2)

        cx = (x1e + x2e) // 2

        # ignore own vehicle area
        if not (h * 0.75 < y2e < h and abs(cx - w // 2) < w * 0.2):
            obstacle_mask[y1e:y2e, x1e:x2e] = 255

    # -----------------------------
    # PEDESTRIAN DETECTION (ROBUST)
    # -----------------------------
    car_center = (w // 2, int(h * 0.8))
    safety_radius = int(min(w, h) * 0.45)

    pedestrian_now = False

    for (px1, py1, px2, py2) in persons:

        person_box = (px1, py1, px2, py2)

        # -----------------------------
        # RIDER FILTER (STRONG)
        # -----------------------------
        is_rider = False
        for vb in vehicles + bicycles:
            if overlap_ratio(person_box, vb) > 0.25:
                is_rider = True
                break

        if is_rider:
            continue

        # Draw pedestrian clearly
        cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 0, 255), 3)

        cx = (px1 + px2) // 2
        cy = (py1 + py2) // 2

        # -----------------------------
        # DUAL SAFETY CONDITION
        # -----------------------------
        dist = np.sqrt((cx - car_center[0]) ** 2 + (cy - car_center[1]) ** 2)

        in_radius = dist < safety_radius
        in_front_band = (
            cy > h * 0.35 and
            abs(cx - w // 2) < w * 0.45
        )

        # Must also be near road (bottom area)
        near_road = cy > h * 0.3

        if near_road and (in_radius or in_front_band):
            pedestrian_now = True

    # -----------------------------
    # TIMER LOGIC
    # -----------------------------
    current_time = time.time()

    if pedestrian_now:
        pedestrian_timer = current_time

    time_since = current_time - pedestrian_timer

    # -----------------------------
    # PATH GENERATION
    # -----------------------------
    lane_left = int(w * 0.2)
    lane_right = int(w * 0.5)
    lane_width = lane_right - lane_left

    path_x = lane_left + lane_width // 2
    path_points = []

    if time_since < STOP_DURATION:
        cv2.putText(frame, "STOP",
                    (50, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 0, 255), 3)
    else:
        for y in range(int(h * 0.8), int(h * 0.3), -8):

            region = obstacle_mask[y - 6:y + 6, path_x - 6:path_x + 6]

            if np.sum(region) > 0:
                break

            path_points.append((path_x, y))

        for (x, y) in path_points:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    cv2.imshow("Autonomous Navigation", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()