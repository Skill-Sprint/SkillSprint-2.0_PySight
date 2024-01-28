import cv2
import os
import numpy as np
from datetime import datetime
import csv

haar_file='C:/Users/Shipr/PycharmProjects/python project/project/haarcascade_frontalface_default.xml'
datasets="C:/Users/Shipr/PycharmProjects/python project/project/dataset"
(images,labels,names,id)=([],[],{},0)
for (subdirs,dirs,files) in os.walk(datasets):
    for subdir in dirs:
        names[id]=subdir
        subjectpath=os.path.join(datasets,subdir)
        for filename in os.listdir(subjectpath):
            path=os.path.join(subjectpath,filename)
            label=id
            images.append(cv2.imread(path,0))
            labels.append(int(label))
        id=id+1

(images,labels)=[np.array(lists) for lists in [images,labels]]
model=cv2.face.LBPHFaceRecognizer_create()
model.train(images,labels)

face_cascade=cv2.CascadeClassifier(haar_file)
cap=cv2.VideoCapture(0)



now=datetime.now()
current_date=now.strftime("%Y-%m-%d")
f=open(current_date+'.csv','w+',newline='')
inwriter=csv.writer(f)





while True:
    ret,frame=cap.read()
    if ret==True:
        img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(img_gray,1.3,4)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            face=img_gray[y:y+h,x:x+h]
            face_resize=cv2.resize(face,(640,480))
            prediction=model.predict(face_resize)
            if prediction[1]<74:
                cv2.putText(frame,'%s'%(names[prediction[0]].strip()),(x+5,(y+25+h)),
                            cv2.FONT_HERSHEY_PLAIN,1.5,(20,185,20),2)
                datet=str(datetime.now())
                frame=cv2.putText(frame,datet,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
                current_time=now.strftime("%H-%M-%S")
                inwriter.writerow([names[prediction[0]],current_time])
            else:
                cv2.putText(frame,"Unknown",(x+5,(y+25+h)),cv2.FONT_HERSHEY_PLAIN,
                            1.5,(65,65,255),2)
                
        cv2.imshow("Face Recognition",frame)
        if cv2.waitKey(1)==ord("q"):
            break
cap.release()
cv2.destroyAllWindows()
f.close()