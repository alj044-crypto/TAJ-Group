import cv2
from ultralytics import YOLO
from collections import defaultdict
import time
import numpy as np
import os

# =========================
# 🔴 EDIT THESE
# =========================

MODEL_PATH = r"C:\Users\ajaxs\Desktop\Hentai\Sauce Codes\School\Group Project\Post Git\yolov8m-hand2\weights\best.pt"
CAMERA_INDEX = 1 

LOCK_TRIGGER_CLASSES = [4, 5]

CLASS_NAMES = {
    0: "fist",
    1: "hand-1",
    2: "hand-2",
    3: "hand-3",
    4: "hand-4",
    5: "hand-5",
}

# 🟣 MULTIPLE TEMPLATE LIST
# Add as many templates as you want here.
TEMPLATES = [
    {
        "name": "circle",
        "path": r"C:\Users\ajaxs\Desktop\templates\circle.png",
        "result": "Circle gesture detected!"
    },
    {
        "name": "line",
        "path": r"C:\Users\ajaxs\Desktop\templates\line.png",
        "result": "Line gesture detected!"
    },
    {
        "name": "zigzag",
        "path": r"C:\Users\ajaxs\Desktop\templates\zigzag.png",
        "result": "Zigzag gesture detected!"
    }
]

LOCK_TIME = 2.0
ROI_PADDING = 50

NO_TRACE_FRAME_LIMIT = 30
TRACE_IMAGE_SIZE = 300
SIMILARITY_THRESHOLD = 0.20

MAX_TRACE_LENGTH = 200

# =========================

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(CAMERA_INDEX)

lock_start_time = None
roi_box = None
locked = False

trace_points = []
traces_by_id = defaultdict(list)

no_trace_frames = 0


def make_trace_image(points, size=300):
    img = np.zeros((size, size), dtype=np.uint8)

    if len(points) < 2:
        return img

    points = np.array(points, dtype=np.float32)

    min_x, min_y = points.min(axis=0)
    max_x, max_y = points.max(axis=0)

    width = max(max_x - min_x, 1)
    height = max(max_y - min_y, 1)

    normalized = []

    for x, y in points:
        nx = int(((x - min_x) / width) * (size - 40) + 20)
        ny = int(((y - min_y) / height) * (size - 40) + 20)
        normalized.append((nx, ny))

    for i in range(1, len(normalized)):
        cv2.line(img, normalized[i - 1], normalized[i], 255, 4)

    return img


def compare_trace_to_template(trace_img, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if template is None:
        print(f"WARNING: Could not load template: {template_path}")
        return float("inf")

    template = cv2.resize(template, (TRACE_IMAGE_SIZE, TRACE_IMAGE_SIZE))

    _, trace_thresh = cv2.threshold(trace_img, 50, 255, cv2.THRESH_BINARY)
    _, template_thresh = cv2.threshold(template, 50, 255, cv2.THRESH_BINARY)

    trace_contours, _ = cv2.findContours(
        trace_thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    template_contours, _ = cv2.findContours(
        template_thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(trace_contours) == 0 or len(template_contours) == 0:
        return float("inf")

    trace_contour = max(trace_contours, key=cv2.contourArea)
    template_contour = max(template_contours, key=cv2.contourArea)

    score = cv2.matchShapes(
        trace_contour,
        template_contour,
        cv2.CONTOURS_MATCH_I1,
        0.0
    )

    return score


# ==========================================================
# 🟣 COMPARE AGAINST MULTIPLE TEMPLATES
# ==========================================================
def find_best_template_match(trace_img, templates):
    best_template = None
    best_score = float("inf")

    for template in templates:
        score = compare_trace_to_template(trace_img, template["path"])

        print(f"Template '{template['name']}' score: {score:.4f}")

        if score < best_score:
            best_score = score
            best_template = template

    if best_template is None:
        return None, float("inf")

    return best_template, best_score


while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame_h, frame_w = frame.shape[:2]

    results = model.track(frame, persist=True)[0]

    valid_lock_detection = False
    currently_tracing = False

    if results.boxes is not None:
        for box in results.boxes:

            cls = int(box.cls[0])
            class_name = CLASS_NAMES.get(cls, f"class-{cls}")

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # =========================
            # MODE 1: LOCK ROI
            # =========================
            if not locked:

                if cls not in LOCK_TRIGGER_CLASSES:
                    continue

                valid_lock_detection = True

                if lock_start_time is None:
                    lock_start_time = time.time()

                elapsed = time.time() - lock_start_time

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

                cv2.putText(
                    frame,
                    f"{class_name} | Hold: {elapsed:.1f}s",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )

                if elapsed >= LOCK_TIME:
                    roi_box = [
                        max(0, x1 - ROI_PADDING),
                        max(0, y1 - ROI_PADDING),
                        min(frame_w - 1, x2 + ROI_PADDING),
                        min(frame_h - 1, y2 + ROI_PADDING)
                    ]

                    locked = True
                    trace_points.clear()
                    traces_by_id.clear()
                    no_trace_frames = 0

                    print("ROI LOCKED")

            # =========================
            # MODE 2: TRACE ALL HAND SIGNS
            # =========================
            else:
                if roi_box is None:
                    continue

                rx1, ry1, rx2, ry2 = roi_box

                if not (rx1 < cx < rx2 and ry1 < cy < ry2):
                    continue

                currently_tracing = True
                no_trace_frames = 0

                trace_points.append((cx, cy))

                if box.id is not None:
                    obj_id = int(box.id[0])
                else:
                    obj_id = 0

                traces_by_id[obj_id].append((cx, cy))

                if len(traces_by_id[obj_id]) > MAX_TRACE_LENGTH:
                    traces_by_id[obj_id].pop(0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

                label = f"ID {obj_id} | {class_name}"

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                for i in range(1, len(traces_by_id[obj_id])):
                    cv2.line(
                        frame,
                        traces_by_id[obj_id][i - 1],
                        traces_by_id[obj_id][i],
                        (255, 0, 0),
                        2
                    )

    if not locked and not valid_lock_detection:
        lock_start_time = None

    if locked and not currently_tracing:
        no_trace_frames += 1

    # ==========================================================
    # TRACE FINISHED → SAVE → CHECK MULTIPLE TEMPLATES → RESULT
    # ==========================================================
    if locked and no_trace_frames >= NO_TRACE_FRAME_LIMIT:

        print("Tracing finished. Saving and checking templates...")

        drawn_trace_img = make_trace_image(trace_points, TRACE_IMAGE_SIZE)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, "last_trace.png")

        cv2.imwrite(save_path, drawn_trace_img)
        print(f"Saved drawn trace to: {save_path}")

        best_template, best_score = find_best_template_match(
            drawn_trace_img,
            TEMPLATES
        )

        print(f"Best score: {best_score:.4f}")

        if best_template is not None and best_score < SIMILARITY_THRESHOLD:
            print("MATCH FOUND")
            print(f"Matched template: {best_template['name']}")
            print(f"Result: {best_template['result']}")

            # =========================
            # 🟢 PUT ACTIONS HERE
            # =========================
            if best_template["name"] == "circle":
                print("ACTION: circle action runs here")

            elif best_template["name"] == "line":
                print("ACTION: line action runs here")

            elif best_template["name"] == "zigzag":
                print("ACTION: zigzag action runs here")

        else:
            print("NO MATCH FOUND")

        break

    if locked and roi_box is not None:
        rx1, ry1, rx2, ry2 = roi_box

        cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 255, 0), 2)

        cv2.putText(
            frame,
            "LOCKED ROI - tracing all hand signs",
            (rx1, ry1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 0),
            2
        )

    cv2.imshow("YOLO ROI Multi-Template Matcher", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()