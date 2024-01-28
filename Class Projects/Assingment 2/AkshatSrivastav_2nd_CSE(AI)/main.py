from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)
ret = True
while ret:
    ret, frame = cap.read()
    if ret == True:
        result = model.track(frame, persist=True)

        frame_ = result[0].plot()

        cv2.imshow('Object Detection', frame_)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()