import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video_path = r'C:\Users\harsh\PycharmProjects\pythonProject1\people.mp4'
cap = cv2.VideoCapture(video_path)

ret = True

while True:
    ret, frame = cap.read()
    if ret is True:
        result = model.track(frame, persist=True)
        frame_ = result[0].plot()

        cv2.imshow("Web Camera", frame_)

        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
