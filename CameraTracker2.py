import cv2
from ultralytics import YOLO

model = YOLO(r"C:\Users\ajaxs\Desktop\Hentai\Sauce Codes\School\Group Project\Post Git\yolov8m-hand2\weights\best.pt")  # lightweight model
cap = cv2.VideoCapture(1) # Use 0 for webcam, or provide video file path

# uses while true loop to make sure window stays up until user presses q to quit
while True:
# reads a frame from the video capture object and stores it in the variable 'frame'. The 'ret' variable is a boolean that indicates whether the frame was successfully read. 
# If 'ret' is False, it means there are no more frames to read (e.g., end of video), and the loop will break, exiting the program.
    ret, frame = cap.read() 
    if not ret:
        break

    results = model(frame)
#Uses r to loop through the results of the models predictions which is then relayed to results then creates boxes around the detected objects and gives them titles based on the predicitons
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
#creates the window and displays video feed of cameras for boxes and such to be placed in
    cv2.imshow("Auto Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#runs code
cap.release()
cv2.destroyAllWindows()