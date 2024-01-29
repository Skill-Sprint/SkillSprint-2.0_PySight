import cv2
import os
import time

import numpy as np

harfile = "haarcascade_frontalface_default.xml"
datasets = "D:\python\pythonProject1\datset"
(images,labels,names,id) = ([],[],{},0)
for (subdirs,dirs,files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath=os.path.join(datasets,subdir)
        for filename in os.listdir(subjectpath):
            path=os.path.join(subjectpath,filename)
            label=id
            images.append(cv2.imread(path,0))
            labels.append(int(label))
        id=id+1
(images,labels) = [np.array(lists) for lists in [images,labels]]
model=cv2.face.LBPHFaceRecognizer_create()
model.train(images,labels)
facecascade = cv2.CascadeClassifier(harfile)
cap=cv2.VideoCapture(0)
print("webcam open?",cap.isOpened())
time.sleep(2)
count = 1
while True:
    ret,frame = cap.read()
    imggrey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(imggrey,1.3,4)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        face = imggrey[y:y+h,x:x+h]
        faceresize = cv2.resize(face,(640,488))
        prediction = model.predict(faceresize)
        if prediction[1] < 50:
            cv2.putText(frame, '%s' % (names[prediction[0]].strip()), (x + 5, (y + 25 + h)),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
        else:
            cv2.putText(frame, "Unknown", (x + 5, (y + 25 + h)), cv2.FONT_HERSHEY_PLAIN,
                        1.5, (65, 65, 255), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()

