import cv2
import numpy as np
import datetime as dt
"""
img=cv2.imread("wha.jpeg")
cv2.imshow("Image",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
print(img.shape)
print(type(img))
"""

"""
cap=cv2.VideoCapture(0)
while True:
    ret,frame =cap.read()

    cv2.imshow("webcam",frame)
    if cv2.waitKey(1) ==ord("q"):
        break
"""
"""
img=cv2.imread("wha.jpeg")
img2=cv2.resize(img,(540,480))
#cv2.imshow("image",img2)
print(img2.shape)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
'''
img=cv2.imread("wha.jpeg")
img2=cv2.resize(img,(540,480))
img3=cv2.rotate(img2,cv2.ROTATE_90_CLOCKWISE)
# cv2.imshow("Image",img2)
cv2.imshow("Image_resize",img2)
# cv2.imshow("Image",img2)
cv2.imshow("Image_rotate",img3)
print(img2.shape)
imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Image_resize",img2)
cv2.imshow("Image_grayscale",imggray)
cv2.waitKey(0)
'''

'''
img = cv2.imread("wha.jpeg")
img=cv2.resize(img,(480,480))

imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgblur=cv2.GaussianBlur(imggray,(9,9),0)
# imgblur3=cv2.GaussianBlur(imggray,(3,3),0)
imgcanny=cv2.Canny(imggray,100,100)

cv2.imshow("Image Gray",imggray)
cv2.imshow("Image Blur 3",imgblur)
# cv2.imshow("Image Blur 9",imgblur) # increasing number will increase blurness
cv2.imshow("Canny Image",imgcanny)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
img=np.zeros((512,512,3),np.uint8)
cv2.line(img,(0,0),(512,512),(255,0,0),2)
#cv2.line((source image), (starting coordinate), (ending coordinate), (color of line), (thickness of line))
cv2.line(img,(0,512),(512,0),(0,0,255),40)
cv2.rectangle(img,(100,100),(300,300),(0,255,0),cv2.FILLED)
cv2.rectangle(img,(200,200),(300,300),(0,255,0),2)

cv2.circle(img,(400,400),50,(203, 192, 255),-1)
cv2.putText(img,"OPENCV",(200,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
#putText(source,Text,Starting coordinate,font,font_scale,color,thickness)


cv2.imshow("Image",img)
cv2.waitKey(0)
'''

'''
cap=cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    date_time=str(dt.datetime.now())
    frame=cv2.putText(frame,date_time,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(1,0,0),1,cv2.LINE_AA)
    cv2.imshow("Video",frame)
    if cv2.waitKey(1)==ord("q"):
        break
'''

'''
# Read two images
image1 = cv2.imread('wha.jpeg')
image2 = cv2.imread('meloni.jpg')

# Ensure that both images have the same height
rows, cols, channels = image1.shape
image2 = cv2.resize(image2, (int(image2.shape[1] * rows / image2.shape[0]), rows))

# Resize the first image to match the width of the second image
image1 = cv2.resize(image1, (image2.shape[1], rows))

# Merge images
merged_image = np.concatenate((image1, image2), axis=1)

# Display the merged image
cv2.imshow('Merged Image', merged_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''

'''
cap=cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    date_time=str(dt.datetime.now())
    frame=cv2.putText(frame,date_time,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(1,0,0),1,cv2.LINE_AA)
    cv2.putText(frame, "Sahil yadav", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Video",frame)
    if cv2.waitKey(1)==ord("q"):
        break

'''


# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video from the default camera (usually 0)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detectiongg
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Get the current date and time
        current_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add text with the date and time on the frame
        cv2.putText(frame,  f"Sahil yadav Date & Time: {current_time}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
























cap.release()
cv2.destroyAllWindows()