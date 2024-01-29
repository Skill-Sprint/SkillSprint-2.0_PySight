import cv2
import numpy as np

canvas = np.zeros((480, 640, 3), dtype=np.uint8)
drawing = False
eraser_mode = False
last_point = None

ERASE_DISTANCE_THRESHOLD = 10  # Adjust as needed

def draw(event, x, y, flags, param):
    global drawing, eraser_mode, last_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing and last_point:
            color = (255, 255, 255) if not eraser_mode else (0, 0, 0)
            thickness = 5 if not eraser_mode else 20
            cv2.line(canvas, last_point, (x, y), color, thickness)
            last_point = (x, y)

# Set up the OpenCV window
cv2.namedWindow("Virtual Drawing System")
cv2.setMouseCallback("Virtual Drawing System", draw)

while True:
    cv2.imshow("Virtual Drawing System", canvas)

    key = cv2.waitKey(1) & 0xFF   #eraser mode
    if key == ord('e'):
        eraser_mode = not eraser_mode
        print("Eraser Mode: ", eraser_mode)

    elif key == ord('q'): #break the loop when key is pressed
        break

cv2.destroyAllWindows()
