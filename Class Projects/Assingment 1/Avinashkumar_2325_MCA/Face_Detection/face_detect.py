import cv2
import os
import numpy as np
import time
import datetime as dt

# data for the face recognition
haar_file = "haarcascade_frontalface_default.xml"
datasets = 'C:\\Users\\sa319\\OneDrive\\Desktop\\coding\\python\\workshop\\Face_Detection\\Dataset\\'
(images, labels, names, id) = ([], [], {}, 0)

# check if any datasets are available
if not os.path.isdir(datasets):
    print("Please run the dataset.py file first")
    exit()


# walk through all the datasets and load them in images, labels, names and id
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id = id + 1

(images, labels) = [np.array(lists) for lists in [images, labels]]

# create the model using LBPHFaceRecognizer 
model = cv2.face.LBPHFaceRecognizer.create()
# train the model with the images and respective names
model.train(images, labels)

# set the classifier for the face with the xml file
face_cascade = cv2.CascadeClassifier(haar_file)

# webcam
cap = cv2.VideoCapture(0)

print("Web cam is open?", cap.isOpened())

time.sleep(2)
count = 1


while True:
    ret, frame = cap.read()
    if ret is True:
        # change color to gray
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the captured frame
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)
        # detectMultiScale(source, scaleFactor, minNeighbors)
        
        for (x, y, w, h) in faces:
            # create rectangles around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            
            # seperate face from the image
            face = img_gray[y:y+h, x:x+h]
            
            # resize the face
            face_resize = cv2.resize(face, (640, 400))
            
            # using the model, check for the face in the datasets
            predictions = model.predict(face_resize)
            
            # set a threshold for the difference between captured image and image in dataset (30)
            if predictions[1] < 30:
                # show name if face found in dataset
                cv2.putText(frame, '%s' % (names[predictions[0]].strip()), (x + 5, y + 25 + h), cv2.FONT_HERSHEY_COMPLEX,
                            1.5, (20, 185, 20), 2)
            else:
                # show Unknown otherwise
                cv2.putText(frame, "Unknown", (x + 5, y + 25 + h), cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (0, 0, 255), 2)
        
        # Date and Time on top left
        cv2.putText(frame, dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), (20, 20), cv2.FONT_HERSHEY_DUPLEX,
                    0.7, (255, 0, 0), 2)
        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

