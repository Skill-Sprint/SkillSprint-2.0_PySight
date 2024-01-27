import cv2
import os
import numpy as np
import datetime as dt

haar_file = "C:/Users/HP/PycharmProjects/facedetect/haarcascade.xml"
# All of the faces data (images) will be stored here
datasets = 'C:/Users/HP/PycharmProjects/facedetect/dataset/'
# change the name below when creating a new dataset for a new person
name = 'Shranya'
(images,labels,names,id)=([],[],{},0)
for(subdirs,dirs,files) in os.walk(datasets):
    for subdirs in dirs:
        names[id]=subdirs
        subjectpath=os.path.join(datasets,subdirs)
        for filename in os.listdir(subjectpath):
            path=os.path.join(subjectpath,filename)
            label=id
            images.append(cv2.imread(path,0))
            labels.append(int(label))
        id=id+1

(images,labels)=[np.array(lists) for lists in [images,labels]]
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images,labels)

face_cascade = cv2.CascadeClassifier(haar_file)
cap = cv2.VideoCapture(0)

while True:
    ret, frame=cap.read()
    if ret==True:
        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(img_gray,1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            face = img_gray[y:y+h,x:x+w]
            face_resize = cv2.resize(face,(640,480))
            prediction=model.predict(face_resize)
            date_time=str(dt.datetime.now())
            if prediction[1]<74:

                cv2.putText(frame,'%s'%(names[prediction[0]].strip()),(x+5,y+25+h),cv2.FONT_HERSHEY_PLAIN,1.5,(20,185,20),2)
                frame = cv2.putText(frame, date_time, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 0), 2)
            else:

                cv2.putText(frame,"SHRANYA",(x+5,(y+25+h)),cv2.FONT_HERSHEY_PLAIN,1.5,(65,65,255),2)
                frame = cv2.putText(frame, date_time, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 0), 2)
                print("Predicted person: SHRANYA")


        cv2.imshow("OpenCV Face Recognition",frame)
        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()