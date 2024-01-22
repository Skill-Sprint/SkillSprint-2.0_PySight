import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
ret = True
while ret:
    ret,frame = cap.read()
    if ret==True:
        result = model.track(frame, persist=True)
        frame_ = result[0].plot()
        cv2.imshow('frame',frame_)
        if cv2.waitKey(5)==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()