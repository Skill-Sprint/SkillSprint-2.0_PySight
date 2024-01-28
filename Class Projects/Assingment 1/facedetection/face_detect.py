import cv2
import os
import numpy as np

haar_file = 'haarcascade_frontalface_default.xml'
datasets ='C:/Users/HP/PycharmProjects/facedetection/dataset/'
(images, labels, names, id) = ([], [], {}, 0)
for (subdir, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] =subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id = id + 1

(images, labels) = [np.array(lists) for lists in [images, labels]]
# Load the face recognizer from the 'face' submodule
model =  cv2.face.LBPHFaceRecognizer_create()

# Rest of your code...

model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret == True:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)
        # detectMultiscale(source_image,scale,min_neighbours)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face = img_gray[y:y + h, x:x + h]
            face_resize = cv2.resize(face, (640, 480))
            prediction = model.predict(face_resize)
            if prediction[1] < 25:
                person_name=names[prediction[0]]
                cv2.putText(frame, '%s' % (person_name), (x + 5, (y + 25 + h)),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
            else:
                cv2.putText(frame, "Unknown", (x + 5, (y + 25 + h)), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (65, 65, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == ord("q"):
             break
cap.release()
cv2.destroyAllWindows()