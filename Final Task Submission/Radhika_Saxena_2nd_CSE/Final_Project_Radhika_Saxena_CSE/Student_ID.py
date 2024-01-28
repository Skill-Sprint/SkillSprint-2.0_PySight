import cv2
import face_recognition
import os
import pickle

path='Person_Faces'
images=os.listdir(path)
print(images)
image_list = []
student_Id=[]
for im in images:
    image__path=os.path.join(path,im)
    a=cv2.imread(image__path)
    image_list.append(a)
    # print(os.path.splitext(im)[0])
    student_Id.append(os.path.splitext(im)[0])
print(student_Id)
print(image_list)

def Encoded_Images(images):
    encoded_images_list=[]
    for im in images:
        im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        img_encoded=face_recognition.face_encodings(im)[0]
        encoded_images_list.append(img_encoded)

    return encoded_images_list

EncodeListknown = Encoded_Images(image_list)
Encoded_List_with_Id=[EncodeListknown,student_Id]
print("Encode Completed")

file=open("Encoded_File.p",'wb')
pickle.dump(Encoded_List_with_Id,file)
file.close()
print("file saved")


