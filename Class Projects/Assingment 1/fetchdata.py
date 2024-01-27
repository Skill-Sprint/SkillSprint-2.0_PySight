import cv2
import os
import time
harfile = "haarcascade_frontalface_default.xml"
datasets = "D:\python\pythonProject1\datset"
name = "vinay"
path = os.path.join(datasets,name)
if not os.path.isdir(path):
    os.mkdir(path)
facecascade = cv2.CascadeClassifier(harfile)
cap = cv2.VideoCapture(0)
print("webcam open?",cap.isOpened())
time.sleep(2)
count = 1
while count<101:
    ret,frame = cap.read()
    imggrey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(imggrey,1.3,4)
    for (x, y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        face = imggrey[y:y+h,x:x+h]
        faceresize = cv2.resize(face,(640,488))
        cv2.imwrite('%s/%s.png'%(path,count),faceresize)
        count = count+1
        cv2.imshow("face capturing",frame)
        if cv2.waitKey(1)== ord("q"):
            break
print("face has been created")
cap.release()
cv2.destroyAllWindows()
