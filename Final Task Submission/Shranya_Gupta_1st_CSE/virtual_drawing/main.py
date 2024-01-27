import cv2
import numpy as np
#Using pre-downloaded images for stacking and comparing
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')
#Resizing the images
img1 = cv2.resize(img1, (640,640))
img2 = cv2.resize(img2, (640,640))
#Stacking the images
img_stacked = np.hstack([img1, img2])

#Answer image
img3 = cv2.imread('image3.jpg')
img4 = cv2.resize(img3,(640,640))
cv2.putText(img1,'Press "A" to reveal the answer' , (50,600),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2,0)
cv2.putText(img2,'Press "Q" to quit the window' , (100,600),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2,0)

# Defining global variables
drawing = False #Creating a flag named drawing
start_point = (-1, -1)
color = (0 , 0 , 0)  #Initial color of rectangle is black

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global start_point, drawing, color
    #Changing the flag value and start_point
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    # Draw a rectangle while pressing and moving the mouse button
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img1.copy()
            cv2.rectangle(img_copy, start_point, (x, y), color , 3)
            cv2.imshow('image', img_stacked)
    #Releasing the left button
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img1, start_point, (x, y), color , 3)
        cv2.imshow('image', img_stacked)

#Creating and resizing a window
cv2.namedWindow('image')
cv2.resizeWindow('image',640,480)

#Calling function
cv2.setMouseCallback('image', draw_rectangle)

# Trackbar callback function
def nothing(x):
    pass

# Create trackbars for color selection
cv2.createTrackbar('Red', 'image', 0, 255, nothing)
cv2.createTrackbar('Green', 'image', 0, 255, nothing)
cv2.createTrackbar('Blue', 'image', 0, 255, nothing)

while True:
    # Get current positions of trackbars
    r = cv2.getTrackbarPos('Red', 'image')
    g = cv2.getTrackbarPos('Green', 'image')
    b = cv2.getTrackbarPos('Blue', 'image')
    color = (b, g, r)
    #Stacking and displaying images
    img_stacked = np.hstack([img1, img2])
    cv2.imshow('image', img_stacked)
    key = cv2.waitKey(1) & 0xFF
    #Displaying answer window
    if key == ord('A'):
        cv2.imshow('image3.jpg', img4)
    #Quitting from running program
    elif key == ord('Q'):
        break


cv2.destroyAllWindows()