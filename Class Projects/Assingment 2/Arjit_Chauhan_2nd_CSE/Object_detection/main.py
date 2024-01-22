from ultralytics import YOLO
import cv2

# loading model
model = YOLO('yolov8n.pt')

# open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # detecting objects from frame
    # track object
    result = model.track(frame, persist=True)

    # plot results
    frame_ = result[0].plot()

    # visualize
    cv2.imshow('frame', frame_)

    # break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
