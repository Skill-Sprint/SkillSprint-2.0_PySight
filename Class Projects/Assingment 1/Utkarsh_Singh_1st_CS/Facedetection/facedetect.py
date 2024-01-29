import cv2
import os
import numpy as np

haar_file = 'haarcascade_frontalface_default.xml'
datasets = "C:/Users/utkar/PycharmProjects/Facedetection/Dataset"
print('Training classifier...')

(images, labels, names, id) = ([], [], {}, 0)

for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1

(width, height) = (640, 480)

(images, labels) = [np.array(lists) for lists in [images, labels]]

model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)
cap = cv2.VideoCapture(0)

print('Classifier trained!')
print('Attempting to detecting faces...')

while True:
    ret, frame = cap.read()
    if ret==True:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, 1.4, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (20, 185, 20), 2)
            face = img_gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)

            if prediction[1] < 50:
                cv2.putText(frame, '%s' % (names[prediction[0]].strip()), (x + 5, (y + 25) + h),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
                # confidence = (prediction[1]) if prediction[1] <= 100.0 else 100.0
                # print("Predicted person: {}, Confidence: {}%".format(names[prediction[0]].strip(),
                #                                                        round((confidence / 74.5) * 100, 2)))
            else:
                cv2.putText(frame, 'Unknown', (x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN, 1.5, (65, 65, 255), 2)
                print("Predicted person: Unknown")

        cv2.imshow('OpenCV Face Recognition', frame)
        if cv2.waitKey(1) == ord("q"):
            break
cap.release()
cv2.destroyAllWindows()