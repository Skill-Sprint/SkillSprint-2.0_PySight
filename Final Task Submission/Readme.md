## FINAL PROJECT SUBMISSION ##
## FACE RECOGNITION ATTENDANCE SYSTEM ##
In this project I have cretaed an Attendance System using Face Recognition Techniques.While making this project ,I researched about Convolutional Neural Networks which helped in gaining some knowledge regarding this project.
I used the face_recognition library while creating this project.While installing this package,I faced some difficulty as the dlib package was not getting installed on my system.To resolve this ,I took help from my mentor.
I first created a Face recognition model ,to detect people faces while the web cam is running.
Firslty I used uploaded some pictures into the dataset so that it can detect those people mark thier attendance.
I made a different file for face encoding.In this file we encode the people faces present in the web cam and compare it with the face encoding of the images we added in the Faces folder.If the threshold values comes close to 0 then the faces are similar and person is marked present.
I have also used 
