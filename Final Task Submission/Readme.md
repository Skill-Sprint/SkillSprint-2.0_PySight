## FINAL PROJECT SUBMISSION ##
## FACE RECOGNITION ATTENDANCE SYSTEM ##

In this project I have cretaed an Attendance System using Face Recognition Techniques.While making this project ,I researched about Convolutional Neural Networks which helped in gaining some knowledge regarding this project.
I used the face_recognition library while creating this project.While installing this package,I faced some difficulty as the dlib package was not getting installed on my system.To resolve this ,I took help from my mentor.
I first created a Face recognition model ,to detect people faces while the web cam is running.
Firslty I uploaded some pictures into the Faces folder so that it can be loaded into face recognition library.
I made a different file for face encoding.In this file we encode the people faces present in the web cam and compare it with the face encoding of the images we added in the Faces folder.If the threshold values comes close to 0 then the faces are similar and person is marked present.
I created a GUI and put my web cam frame on it.I resized my frame accrodingly.
I put rectangular contours on the face detected in the web cam.
I tried to link my Excel sheet "ATTENDANCE.xlsx" with my project using pandas library ,but I am facing some issue in linking it using the file path.
I have used open-cv,face_recognition,pandas,pickle library to create my project.

## THIS IS THE OVERALL PROGRESS OF MY PROJECT ##
