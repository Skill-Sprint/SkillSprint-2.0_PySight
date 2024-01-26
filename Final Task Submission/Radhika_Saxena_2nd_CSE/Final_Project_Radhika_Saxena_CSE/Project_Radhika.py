import cv2
import os
import face_recognition
import pickle
import numpy as np
import pandas as pd

print("Encoded file loading....")
file=open("Encoded_File.p",'rb')
Encoded_List_with_Id=pickle.load(file)
file.close()
EncodeListknown,student_Id=Encoded_List_with_Id
# print(student_Id)
print("Encoded file successfully loaded")

Background_img=cv2.imread('ATTENDANCE.jpg')
Folder_path='Person_Faces'
images=os.listdir(Folder_path)
# print(images)
for im in images:
    image_path=os.path.join(Folder_path,im)
    face_recognition.load_image_file(image_path)
    # Background_img[]

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
while True:
    ret, Frame = cap.read()
    # frame = cv2.resize(Frame, (0, 0), None, 0.25, 0.25)
    frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame)
    Cur_face_Encoding=face_recognition.face_encodings(frame,face_locations)

    Background_img[162:162 + 480, 55:55 + 640] = Frame

    for cur_face,face_loc in zip(Cur_face_Encoding,face_locations):
        matched_face=face_recognition.compare_faces(EncodeListknown,cur_face)
        dis=face_recognition.face_distance(EncodeListknown,cur_face)
        # print("matched",matched_face)
        # print("distance",dis)
        matched_index=np.argmin(dis)
        # print("matchedindex",matched_index)

        def attendance():
            Excel_path = 'Attendance_System.xlsx'
            df = pd.read_excel(Excel_path)
            recognized_id = student_Id[matched_index]
            update = df[df[ID] == recognized_id].index
            df.at[update, 'P-A'] = 'Present'

        if matched_face[matched_index]:
            print("face matched")
            print(student_Id[matched_index])
            stu_id=student_Id[matched_index]
            # top, right, bottom, left = face_loc
            # Background_img=cv2.rectangle(frame,(top,right),(bottom,left), (255, 0, 0), 0, 1)
            attendance(stu_id)

    # cv2.imshow("Video",Frame)
    cv2.imshow("Attendance",Background_img)
    if cv2.waitKey(1)==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()




