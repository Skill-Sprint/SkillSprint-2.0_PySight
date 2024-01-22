import cv2
import os
import numpy as np
import datetime as dt

haar_file = "haarcascade_frontalface_default.xml"

datasets = 'C:/Users/shiva/OneDrive/Desktop/Python Bootcamp/assignment_1/Dataset'

(images,labels,name,id) = ([],[],{},0)
for(subdirs,dirs,files) in os.walk(datasets):
    for subdir in dirs:
        name[id] = subdir
        subjectpath = os.path.join(datasets,subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath,filename)
            label = id
            images.append(cv2.imread(path,0))
            labels.append(int(label))
        id += 1

(images, labels) = [np.array(lists) for lists in [images,labels]]
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images,labels)

face_cascade = cv2.CascadeClassifier(haar_file)

cap = cv2.VideoCapture(0)


while True:
    ret,frame = cap.read()
    date_time = str(dt.datetime.now())
    if ret == True:
        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray,2,5,4)

        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),8)
            face = img_gray[y:y+h,x:x+h]
            face_resize = cv2.resize(face,(640,480))
            prediction = model.predict(face_resize)
            if prediction[1]<74:
                cv2.putText(frame, date_time, (x + 5, (y + 45 + h)), cv2.FONT_HERSHEY_PLAIN,1.5, (20, 185, 20), 2)
                cv2.putText(frame,'%s'%(name[prediction[0]].strip()),(x+5,(y+25+h)),cv2.FONT_HERSHEY_PLAIN,1.5,(20,185,20),2)
            else:
                cv2.putText(frame,"Unknown",(x+5,(y+25+h)),cv2.FONT_HERSHEY_PLAIN,1.5,(65,65,255),2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()