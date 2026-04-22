import cv2

# Initialize camera and tracker
cap = cv2.VideoCapture(0)
tracker = cv2.legacy.TrackerKCF_create()  # Common trackers: KCF, MIL, CSRT

# Read first frame and let user select ROI with mouse
ret, frame = cap.read()
roi = cv2.selectROI("Tracking Window", frame, fromCenter=False, showCrosshair=True)
tracker.init(frame, roi)

while True:
    ret, frame = cap.read()
    if not ret: break

    # Update tracker and draw result
    success, bbox = tracker.update(frame)
    if success:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.imshow("Tracking Window", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()