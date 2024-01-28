import cv2, os, time
# change the paths below to the location where these files are on your machine
haar_file = 'C:/Users/Asus/Desktop/Coding/Pycharm/main.py/Face detect/haarcascade_frontalface_default.xml'
# All of the faces data (images) will be stored here
datasets = "C:/Users/Asus/Desktop/Coding/Pycharm/main.py/Face detect/Dataset"
# change the name below when creating a new dataset for a new person
name = 'Harsh'

path = os.path.join(datasets, name)
# if sub_dataset folder doesn't already exist, make the folder with the name defined above
if not os.path.isdir(path):
    os.mkdir(path)

# defining the size of images
(width, height) = (640, 480)

face_cascade = cv2.CascadeClassifier(haar_file)
cap = cv2.VideoCapture(0)
# returns true or false (if the camera is on or not)
print("Webcam is open? ", cap.isOpened())
# wait for the camera to turn on (just to be safe, in case the camera needs time to load up)
time.sleep(2)
#Takes pictures of detected face and saves them
count = 1
print("Taking pictures...")
# this takes 100 pictures of your face. Change this number if you want.
# Having too many images, however, might slow down the program
while count < 101:
    # im = camera stream
    ret, frame= cap.read()
    # if it recieves something from the webcam...
    if ret == True:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect face using the haar cascade file
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)  #(source,scale,min_neighbours)
        for (x,y,w,h) in faces:
            # draws a rectangle around your face when taking pictures
            # this is to create a ROI (region of interest) so it only takes pictures of your face
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            # define 'face' as the inside of the rectangle we made above and make it grayscale
            face = img_gray[y:y + h, x:x + w]
            # resize the face images to the size of the 'face' variable above (i.e: area captured inside of the rectangle)
            face_resize = cv2.resize(face, (width, height))
            # save images with their corresponding number
            cv2.imwrite('%s/%s.png' % (path,count), face_resize)
        count += 1
        cv2.imshow('Face Capturing', frame)
        if cv2.waitKey(1) == ord("q"):
            break
print("Your face has been created.")
cap.release()
cv2.destroyAllWindows()