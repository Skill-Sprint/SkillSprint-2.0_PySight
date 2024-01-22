import cv2
import numpy as np
framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
def empty(x):
    pass
cv2.namedWindow('parameters')
cv2.resizeWindow('parameters',640,480)
cv2.createTrackbar('threshold1','parameters',100,255,empty)
cv2.createTrackbar('threshold2','parameters',200,255,empty)
cv2.createTrackbar('Area','parameters',1000,20000,empty)
def getContours(imgDiale,imgContours):
    """

    :param imgDiale: we are getting the cordinates of edges to draw the countors
    :param imgCountors: After getting cordinates we draw the countors to orginaal image
    :return:
    """
    contour,hie = cv2.findContours(cv2.cvtColor(imgDilate, cv2.COLOR_BGR2GRAY),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contour:
        area_min = cv2.getTrackbarPos('Area','parameters')
        area = cv2.contourArea(cnt)
        print(area)
        if area > area_min:
            # print(area)
            cv2.drawContours(imgContours,cnt,-1,(0,255,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContours,(x,y),(x+w,y+h),(255,0,255),3)
            cv2.putText(imgContours,"Points"+str(len(approx)),(x+w+20,y+h+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2,0)
            cv2.putText(imgContours,'Area: '+str(int(area)),(x+w+45,y+h+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2,0)


while True:
    ret,img = cap.read()
    imgContours = img.copy()
    # preprocessing of image
    imgblur = cv2.GaussianBlur(img,(7,7),1)
    # why bluring the image?
    # it is beacuse if we not blur the image we get more noises and unwanted edges so to prevent this we preprocess(blur) the input image
    #converting image in to gray
    imgGray = cv2.cvtColor(imgblur,cv2.COLOR_BGR2GRAY)
    # why converting into gray?

    # Because canny edge detector in works on gray channel image
    imgGray = cv2.cvtColor(imgGray,cv2.COLOR_GRAY2BGR)


    # converting img into cany for edge detection
    t1 = cv2.getTrackbarPos('threshold1','parameters')
    t2 = cv2.getTrackbarPos('threshold2','parameters')
    imgCanny = cv2.Canny(imgGray,t1,t2)
    # it also required to be converted
    imgCanny = cv2.cvtColor(imgCanny,cv2.COLOR_GRAY2BGR)
    # to find the correct threesold valus we need to creat trackbar to get optimal threesold vales

    # width of image is very small so we have to dilate the image

    kernal = np.ones((5,5),np.uint8)

    imgDilate = cv2.dilate(imgCanny,kernal,iterations=1)
    # imgDilate = cv2.cvtColor(imgDilate,cv2.COLOR_GRAY2BGR)

    getContours(imgDilate,imgContours=imgContours)


    output = np.hstack([imgDilate,imgContours])
    cv2.imshow('output',output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()