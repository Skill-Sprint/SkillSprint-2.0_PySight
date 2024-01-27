import cv2
import os
import time

haar_file = "haarcascade_frontalface_default.xml"
datasets = "dataset/"
name = "ankur"
path = os.path.join(datasets, name)
if not os.path.exists(path):
    os.mkdir(path)
face_cascade = cv2.CascadeClassifier(haar_file)
cap = cv2.VideoCapture(0)
print("Web cam is open", cap.isOpened())
time.sleep(2)
count = 1

while count < 201:
    ret, frame = cap.read()
    if ret == True:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face = img_gray[y : y + h, x : x + w]
            face_resize = cv2.resize(face, (640, 480))
            cv2.imwrite("%s/%s.png" % (path, count), face_resize)
        count += 1
        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) == ord("e"):
            break

print("Your face has been captured")
cap.release()
cv2.destroyAllWindows()
