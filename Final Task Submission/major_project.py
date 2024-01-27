import cv2 as cv
import numpy as np
import mediapipe as mp
frame_shape=(720,1280,3)

# def nothing(x):
#     pass
#
# blank=np.zeros((300,512,3),np.uint8)
# window_name='Paint It'
# cv.namedWindow(window_name)
# cv.createTrackbar('B',window_name,0,255,nothing)
# cv.createTrackbar('G',window_name,0,255,nothing)
# cv.createTrackbar('R',window_name,0,255,nothing)
#
# switch='0: OFF\n 1:ON'
# cv.createTrackbar(switch,window_name,0,1,nothing)
#
#
# while(1):
#     cv.imshow(window_name,blank)
#     k=cv.waitKey(1) & 0xFF
#     if k==27:
#         break
#
#     b = cv.getTrackbarPos('B', window_name)
#     g = cv.getTrackbarPos('G', window_name)
#     r = cv.getTrackbarPos('R', window_name)
#     s = cv.getTrackbarPos(switch, window_name)
#
#     if s==0:
#       blank[:]=0
#     else:
#       blank[:]=[b,g,r]
# cv.destroyAllWindows()
cap=cv.VideoCapture(0)
#Loading the model
hands=mp.solutions.hands
hand_landmark=hands.Hands(max_num_hands=1)
draw=mp.solutions.drawing_utils
cap.set(3,1280)
cap.set(4,720)
colour=(230,216,173)
prevxy=None
mask=np.zeros(frame_shape,dtype='uint8')

while True:
  ret,frame=cap.read()
  rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
  op=hand_landmark.process(rgb)
  if op.multi_hand_landmarks:
      for all_landmarks in op.multi_hand_landmarks:
          draw.draw_landmarks(frame,all_landmarks,hands.HAND_CONNECTIONS)
          x=int(all_landmarks.landmark[8].x*frame.shape[1])
          y=int(all_landmarks.landmark[8].y*frame.shape[0])

          # cv.circle(frame,(x,y),30,(0,0,0),-1)
          # cv.circle(mask, (x, y), 30, (0, 0, 0), -1)

      if prevxy!=None:
          cv.line(mask,prevxy,(x,y),colour,3)
      prevxy=(x,y)
#Merge Frame and Mask
  frame=np.where(mask,mask,frame)
  cv.imshow('Live',frame)
  if cv.waitKey(1)==27:
      break
#Drawing
#1.Locate index finger
#2draw line

cap.release()
cv.destroyAllWindows()
