import cv2
import numpy as np

# Load pre-trained people detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Open video capture
cap = cv2.VideoCapture('video.mp4')  # Replace with your video file or camera index

while cap.isOpened():
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame to speed up processing
    frame = cv2.resize(frame, (640, 480))

    # Detect people in the frame
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(4, 4), scale=1.05)

    # Draw bounding boxes around detected people
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the current frame with people bounding boxes
    cv2.imshow('People Counting', frame)

    # Count the number of people
    people_count = len(boxes)
    print(f"People Count: {people_count}")

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
