import cv2 as cv
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:
        result = model.track(frame, persist=True)
        frame_ = result[0].plot()
        cv.imshow('Frame', frame_)
        if cv.waitKey(1) == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
