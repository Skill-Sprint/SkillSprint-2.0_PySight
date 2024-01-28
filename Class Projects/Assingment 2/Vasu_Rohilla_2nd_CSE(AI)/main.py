from ultralytics import YOLO
import cv2


model = YOLO('yolov8n.pt')
path = 'D:/vasu/object_detection/vd 2.mp4'

cap = cv2.VideoCapture(path)
ret = True
while ret:
    ret, frame = cap.read()
    if ret == True:
        result = model.track(frame, persist=True)
        frame = result[0].plot()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()