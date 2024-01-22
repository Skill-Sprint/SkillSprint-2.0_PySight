import cv2
import numpy as np

framewidth=640
frameheight=480

cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)

def empty(x):
    pass

cv2.namedWindow("parameters")
cv2.createTrackbar("threshold1","parameters",100,225,empty)
cv2.createTrackbar("threshold2","parameters",200,225,empty)

def get_contours(img_dilate,img_contours):
    contours,hierarchy=cv2.findContours(img_dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area_min = cv2.contourArea(cnt)
        cv2.drawContours(img_contours, cnt, -1, (0, 255, 0), 3)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(img_contours, (x, y), (x + w, y + h), (255, 0, 255), 3)
        cv2.putText(img_contours, "Points" + str(len(approx)), (x, y), (x + w, y + h), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    (255, 0, 255), 2, 0)
        cv2.putText(img_contours, 'Area:' + str(int(area_min)), (x + w + 45, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    (0, 0, 255), 2, 0)
while True:
    ret,frame=cap.read()
    img_contours=frame.copy()
    img_blur=cv2.GaussianBlur(frame,(7,7),4)
    img_gray=cv2.cvtColor(img_blur,cv2.COLOR_BGR2GRAY)

    t1 =  cv2.getTrackbarPos("threshold1","parameters")
    t2 = cv2.getTrackbarPos("threshold2", "parameters")

    img_canny=cv2.Canny(img_gray,100,200)
    kernel=np.ones((5,5),np.uint8)
    img_dilate=cv2.dilate(img_canny,kernel,iterations=1)

    output=np.hstack([img_canny,img_dilate])
    cv2.imshow("image", output)

    if cv2.waitKey(1)==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()