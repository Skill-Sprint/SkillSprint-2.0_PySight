import cv2
import numpy as np
from collections import deque
import pyautogui

global colorIndex

# Global variables
drawing = False
start_point = (-1, -1)


p=pyautogui.position()
mouse_x=p.x
mouse_y=p.y


# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0




# Callback function for mouse events
def draw(event, x, y, flags, param):
    global drawing, start_point, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(img, start_point, (x, y), colors[mouse_click(mouse_x,mouse_y)],2)
            start_point = (x, y)
            print(colors[colorIndex])

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Create a black image
img = np.ones((800, 1200, 3), np.uint8) * 255
# Create a window and set the callback function
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# = np.zeros((471,636,3)) + 255
img = cv2.rectangle(img, (40,1), (140,65), (0,0,0), 2)
img = cv2.rectangle(img, (160,1), (255,65), colors[0], -1)
img = cv2.rectangle(img, (275,1), (370,65), colors[1], -1)
img = cv2.rectangle(img, (390,1), (485,65), colors[2], -1)
img = cv2.rectangle(img, (505,1), (600,65), colors[3], -1)
#cv2.imshow("Paint", paintWindow)


cv2.putText(img, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
# Now checking if the user wants to click on any button above the screen

def mouse_click(mouse_x,mouse_y):
        if 40 <= mouse_x <= 140 and 1 <= mouse_y <= 65:  # Clear Button
            bpoints = [deque(maxlen=512)]
            gpoints = [deque(maxlen=512)]
            rpoints = [deque(maxlen=512)]
            ypoints = [deque(maxlen=512)]
            blue_index = 0
            green_index = 0
            red_index = 0
            yellow_index = 0
            img[67:, :, :] = 255
        elif 160 <= mouse_x <= 255 and 1 <= mouse_y <= 65:
            pyautogui.click(colorIndex=0)   # Blue
        elif 275 <= mouse_x <= 370 and 1 <= mouse_y <= 65:
            pyautogui.click(colorIndex=1)  # Blue
        elif 390 <= mouse_x <= 485 and 1 <= mouse_x <=65:
            pyautogui.click(colorIndex=2)  # Blue
        elif 505 <= mouse_y <= 600 and 1 <= mouse_y <=65:
            pyautogui.click(colorIndex=3)  # Blue
        return colorIndex

cv2.namedWindow('Canvas Drawing')
cv2.setMouseCallback('Canvas Drawing', draw)

while True:
    cv2.imshow('Canvas Drawing', img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Clear the canvas when 'c' is pressed
        img = np.ones((800, 1200, 3), np.uint8) * 255
        cv2.imshow('Canvas Drawing', img)

    elif key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()
