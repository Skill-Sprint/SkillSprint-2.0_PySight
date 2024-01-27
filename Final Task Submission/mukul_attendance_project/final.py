import cv2
import os
import numpy as np
import pickle
import face_recognition
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk,Image








cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
#importing the images...
# modepath='resources/MODES'
# modepathList=os.listdir(modepath)
# imgmodelist=[]
# for path in modepathList:
#     imgmodelist.append(cv2.imread(os.path.join(modepath,path)))
file=open('Encodefile.p','rb')
encodelistknownwithids=pickle.load(file)
file.close()
encodelistknown,studentsids =encodelistknownwithids


def mark_attendance():
    #flag= True
    while True:
        success, img = cap.read()
        # imgs = cv2.resize(img,(0,0),None,0.25,0.25)
        # imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        facecurframe = face_recognition.face_locations(img)
        encodecurframe = face_recognition.face_encodings(img, facecurframe)

        for encodeface, faceloc in zip(encodecurframe, facecurframe):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            faceDis = face_recognition.face_distance(encodelistknown, encodeface)
            # print("matches",matches)
            # print('faceDis',faceDis)

            matchindex = np.argmin(faceDis)
            # print("MATCH INDEX",matchindex)

            if matches[matchindex]:
                cv2.putText(img,"data matched",(155,170),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
                print("known Face Detected")
                print(studentsids[matchindex])
                # return True
            else:
                cv2.putText(img, "data not matched", (155, 170), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                # flag=False
                # return False
            (top, right, bottom, left) = faceloc
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("faceattendence", img)
        # canvas = Canvas(root, width=640, height=480)
        # canvas.pack(pady=(20, 20))
        if cv2.waitKey(1)==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



def quit_attendance():
    root.destroy()
    cv2.destroyAllWindows()

root = tk.Tk()
root.title('KIET PORTAL')

mark_button = ttk.Button(root, text='MARK ATTENDANCE', command=mark_attendance)
#variable=mark_attendance()
mark_button.pack(pady=(20, 20))
quit_button = ttk.Button(root,text='QUIT', command=quit_attendance)
quit_button.pack(pady=(20,20))

root.configure(background='#0096DC')
img = Image.open('kiet.jpg')
resized_img = img.resize((200, 200))
img = ImageTk.PhotoImage(resized_img)
img_label = Label(root, image=img)
img_label.pack(pady=(20, 20))
text_label = Label(root, text='ATTENDANCE!!!')
text_label.pack()
text_label.config(font=('verdana', 24))


# if flag:
#     detail=Label(root,text="hey")
#     detail.pack()
#     detail.config(font=('verdana',14))



# Handle window closure
root.protocol("WM_DELETE_WINDOW", cap.release)

root.mainloop()