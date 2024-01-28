import cv2
import face_recognition
import pickle
import os

##importing student images
folderpath='images'
pathlist=os.listdir(folderpath)
print(pathlist)
imglist=[]
studentsids=[]
for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    #print(path)
    #print(os.path.splitext(path)[0])
    studentsids.append(os.path.splitext(path)[0])
print(studentsids)


def  findencodings(imageslist):
     encodelist=[]
     for img in imageslist:
         img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
         encode=face_recognition.face_encodings(img)[0]
         encodelist.append(encode)

     return encodelist


print("encoding started ....")
encodelistknown=findencodings(imglist)
encodelistknownwithids=[encodelistknown,studentsids]
print("encoding complete")

file=open("Encodefile.p",'wb')
pickle.dump(encodelistknownwithids,file)
file.close()
print("file save")