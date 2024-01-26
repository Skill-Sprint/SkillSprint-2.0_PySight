import cv2
import numpy as np

cap = cv2.VideoCapture(0)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)

drawing = False
prev_point = (0, 0)

def draw_line(img, start, end, color, thickness=5):
    cv2.line(img, start, end, color, thickness)

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (15, 15), 0)

    _, threshold = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        hand_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(hand_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.circle(frame, (cx, cy), 10, (0, 255, 255), -1)

        if drawing:
            draw_line(canvas, prev_point, (cx, cy), (255, 255, 255))

        prev_point = (cx, cy)

    cv2.imshow('Frame', frame)
    cv2.imshow('Canvas', canvas)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    elif key == ord('d'):
        drawing = not drawing

cap.release()
cv2.destroyAllWindows()
