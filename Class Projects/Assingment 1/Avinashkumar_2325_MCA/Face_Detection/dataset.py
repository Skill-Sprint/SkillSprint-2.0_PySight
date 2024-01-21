import cv2
import os
import time

# data for face recognition
haar_file = "haarcascade_frontalface_default.xml"
# path to the folder
datasets = 'C:\\Users\\sa319\\OneDrive\\Desktop\\coding\\python\\workshop\\Face_Detection\\'

# input custom name to save face data
name = input("Enter your name: ")

# if the Dataset folder is not created then create it
if not os.path.isdir(datasets + "Dataset"):
    os.mkdir(datasets + "Dataset")

datasets += "Dataset\\"

# Create a dataset folder for the person
path = os.path.join(datasets, name)
if not os.path.isdir(path):
    os.mkdir(path)
    
# set the classifier for the face with the xml file
face_cascade = cv2.CascadeClassifier(haar_file)

# webcam
cap = cv2.VideoCapture(0)

print("Web cam is open?", cap.isOpened())

# wait 2 seconds before opening
time.sleep(2)
count = 1

# 100 images for dataset, increase count to make dataset bigger and accurate
while count < 101:
    ret, frame = cap.read()
    if ret is True:
        # convert frame to gray
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the captured frame
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)
        # detectMultiScale(source, scaleFactor, minNeighbors)
        for (x, y, w, h) in faces:
            # draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            
            # crop out the face
            face = img_gray[y:y+h, x:x+h]

            # resize the face image so that all images match
            face_resize = cv2.resize(face, (640, 400))
            cv2.imwrite("%s/%s.png" % (path, count), face_resize)
        count = count + 1
        cv2.imshow("Face Capturing", frame)
        if cv2.waitKey(1) == ord("q"):
            break

print("Your face has been created")
cap.release()
cv2.destroyAllWindows()
