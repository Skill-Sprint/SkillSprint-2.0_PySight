import cv2
def draw(event,x,y,flags,param):
    if event==1:
        print(x,y)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame',draw)
img = cv2.imread("C:/Users/HP/PycharmProjects/attendance_project/resources/BACKGROUND/Add a subheading_page-0001.jpg",1)
new_size=(640,480)
img1=cv2.resize(img,new_size)
cv2.imshow('frame',img1)
while True:
    if cv2.waitKey(1)==ord("m"):
        break
cv2.destroyAllWindows()

