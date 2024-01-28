import cv2
import face_recognition
import os
from datetime import datetime

known_faces = []
known_names = []
directory = 'known_faces'

for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        img_path = os.path.join(directory, filename)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)[0]
        known_faces.append(encoding)
        known_names.append(os.path.splitext(filename)[0])

face_locations = []
face_encodings = []
face_names = []
attendance = {}


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        if True in matches:
            matchindex = matches.index(True)
            name = known_names[matchindex]

            if name not in attendance:
                attendance[name] = datetime.now()

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 2)

    cv2.imshow('Attendance System', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

