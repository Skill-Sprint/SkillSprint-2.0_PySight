import cv2
import os

# locate the images and assign them to a list
folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header = overlayList[0]

draw = False


# mouse event function to define the use of mouse event
def click_event(event, x, y, flags, param):
    global header, draw
    if event == cv2.EVENT_LBUTTONDOWN:
        if draw is False:  # condition that the left button of the mouse is clicked and pen is on
            draw = True
        else:
            draw = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if draw:  # if left button is clicked than perform these task accordingly
            if y <= 125:  # if the cursor is in the selection area
                if 250 < x < 450:  # if the cursor is on the blue color area
                    header = overlayList[0]  # display the first image in the header folder
                elif 550 < x < 750:  # if the cursor is on the red color area
                    header = overlayList[1]  # display the second image in the header folder
                elif 800 < x < 950:  # if the cursor is on the green color area
                    header = overlayList[2]  # display the third image in the header folder
                elif 1050 < x < 1200:  # if the cursor is on the delete area
                    header = overlayList[3]  # display the  fourth image in the header folder
            lines.append((x, y))  # append the points on which cursor moving


# capture the video and set width and height
img = cv2.VideoCapture(0)
img.set(3, 1280)
img.set(4, 720)

# name the window and call the mouse event function in that window
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', click_event)  # mouse event function

flag = 0
lines = []
ret = True
while ret: # loop to display the images captured
    ret, frame = img.read()
    frame[0:125, 0:1280] = header  # to overlay image over the video captured
    for a, b in lines:  # loop until the mouse function returns the points
        if draw:  # to display the current value of pen
            cv2.putText(frame, "PEN ON", (30, 145), cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
        if draw is False:
            cv2.putText(frame, "PEN OFF", (30, 145), cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
        if b < 125:  # conditions to select the color and paint or delete
            if 250 < a < 450:
                flag = 1
            elif 550 < a < 750:
                flag = 2
            elif 800 < a < 950:
                flag = 3
            elif 1050 < a < 1200:  # if the cursor is over the delete box then assign a new list with no points
                flag = 4
                lines = []
        elif flag != 4:  # if the cursor is not over the delete box then only display the content
            if flag == 0:  # for default color
                cv2.line(frame, (a, b), (a, b), (255, 0, 0), 18)
            elif flag == 1: # for blue color
                cv2.line(frame, (a, b), (a, b), (255, 0, 0), 18)
            elif flag == 2:  # for red color
                cv2.line(frame, (a, b), (a, b), (0, 0, 255), 18)
            elif flag == 3:  # for green color
                cv2.line(frame, (a, b), (a, b), (0, 255, 0), 18)

    cv2.imshow('Image', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
