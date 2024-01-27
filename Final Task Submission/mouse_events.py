
import numpy as np
import cv2 as cv

events=[i for i in dir(cv) if 'EVENT' in i]
drawing=True
mode_rect=False
ix,iy=-1,-1
def nothing(x):
    pass

cv.namedWindow('Window')
cv.createTrackbar('R','Window',0,255,nothing)
cv.createTrackbar('B','Window',0,255,nothing)
cv.createTrackbar('G','Window',0,255,nothing)
def draw_circle(events,x,y,flags,param):
    global ix,iy
    r=cv.getTrackbarPos('R','Window')
    b=cv.getTrackbarPos('B','Window')
    g=cv.getTrackbarPos('G','Window')
    colour=(b,g,r)
    if drawing:
      if events==cv.EVENT_LBUTTONDBLCLK:
       cv.circle(blank,(x,y),30,colour,-1)
      if mode_rect==False:
        if events==cv.EVENT_LBUTTONDOWN:
          ix,iy=x,y
        elif events==cv.EVENT_LBUTTONUP:
          cv.line(blank,(ix,iy),(x,y),colour,3)
      elif mode_rect==True:
          if events == cv.EVENT_LBUTTONDOWN:
            ix, iy = x, y
          elif events == cv.EVENT_LBUTTONUP:
            cv.rectangle(blank, (ix, iy), (x, y), colour, -1)
    else:
      if events ==cv.EVENT_MOUSEMOVE:
       cv.circle(blank,(x,y),30,0,-1)




blank = np.zeros((512, 512, 3), dtype='uint8')
cv.setMouseCallback('Window',draw_circle)
while True:
  cv.imshow('Window',blank)
  k=cv.waitKey(1) & 0xFF
  if k==ord('r'):
      mode_rect=True
  elif k==ord('e'):
      drawing=False
  elif k==27:
      break
cv.destroyAllWindows()

