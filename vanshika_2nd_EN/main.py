import cv2
import numpy as np

# Load pre-trained Haar Cascade classifier for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in a frame
def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Function to count people from detected faces
def count_people(faces):
    return len(faces)

# Main function to process video stream
def main():
    # Open video capture device (webcam or video file)
    cap = cv2.VideoCapture(0)  # Change to your video file path if you want to process a video file

    # Check if the capture is opened successfully
    if not cap.isOpened():
        print("Error: Failed to open video capture.")
        return

    # Loop to process frames
    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break

        # Detect faces in the frame
        faces = detect_faces(frame)

        # Count people
        num_people = count_people(faces)

        # Display the number of people in the frame
        cv2.putText(frame, f'People Count: {num_people}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Frame', frame)

        # Check for key press
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break

    # Release the video capture device and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
