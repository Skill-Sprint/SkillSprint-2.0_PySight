import mediapipe as mp
import cv2
import numpy as np
import time

#contants
width = 150
xmax, ymax = 250+width, 50
curr_tool = "select tool"
time_in = True
rad = 40
var_in = False
thick = 4
prevx, prevy = 0,0

#tool bar
img=np.zeros((50,250,3),np.uint8)
cv2.rectangle(img,(0,0),(250,50),(0,255,0),2)
cv2.line(img,(50,0),(50,50),(255,255,255),2)
cv2.line(img,(100,0),(100,50),(255,255,255),2)
cv2.line(img,(150,0),(150,50),(255,255,255),2)
cv2.line(img,(200,0),(200,50),(255,255,255),2)
cv2.putText(img,"LINE",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
cv2.putText(img,"REC",(60,30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
cv2.putText(img,"DRAW",(110,30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
cv2.putText(img,"CIRCLE",(155,30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
cv2.putText(img,"ERASE",(205,30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
cv2.imwrite("image.png", img)

#get tools function
def getTool(x):
	if x < 50 + width:
		return "line"

	elif x < 100 + width:
		return "rectangle"

	elif x < 150 + width:
		return"draw"

	elif x<200 + width:
		return "circle"

	else:
		return "erase"

def indexraise(yi, y9):
	if (y9 - yi) > 40:
		return True

	return False

hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
draw = mp.solutions.drawing_utils

# drawing tools
tools = cv2.imread("image.png")
tools = tools.astype('uint8')

mask = np.ones((480, 640))*255
mask = mask.astype('uint8')

cap = cv2.VideoCapture(0)
while True:
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	op = hand_landmark.process(rgb)

	if op.multi_hand_landmarks:
		for i in op.multi_hand_landmarks:
			draw.draw_landmarks(frame, i, hands.HAND_CONNECTIONS)
			x, y = int(i.landmark[8].x*640), int(i.landmark[8].y*480)

			if x < xmax and y < ymax and x > width:
				if time_in:
					ctime = time.time()
					time_in = False
				ptime = time.time()

				cv2.circle(frame, (x, y), rad, (0,255,255), 2)
				rad -= 1

				if (ptime - ctime) > 0.8:
					curr_tool = getTool(x)
					print("your current tool set to : ", curr_tool)
					time_in = True
					rad = 40

			else:
				time_in = True
				rad = 40

			if curr_tool == "draw":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if indexraise(yi, y9):
					cv2.line(mask, (prevx, prevy), (x, y), 0, thick)
					prevx, prevy = x, y

				else:
					prevx = x
					prevy = y

			elif curr_tool == "line":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if indexraise(yi, y9):
					if not var_in:
						xii, yii = x, y
						var_in = True

					cv2.line(frame, (xii, yii), (x, y), (50,152,255), thick)

				else:
					if var_in:
						cv2.line(mask, (xii, yii), (x, y), 0, thick)
						var_in = False

			elif curr_tool == "rectangle":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if indexraise(yi, y9):
					if not var_in:
						xii, yii = x, y
						var_in = True

					cv2.rectangle(frame, (xii, yii), (x, y), (0,255,255), thick)

				else:
					if var_in:
						cv2.rectangle(mask, (xii, yii), (x, y), 0, thick)
						var_in = False

			elif curr_tool == "circle":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if indexraise(yi, y9):
					if not var_in:
						xii, yii = x, y
						var_in = True

					cv2.circle(frame, (xii, yii), int(((xii-x)**2 + (yii-y)**2)**0.5), (255,255,0), thick)

				else:
					if var_in:
						cv2.circle(mask, (xii, yii), int(((xii-x)**2 + (yii-y)**2)**0.5), (0,255,0), thick)
						var_in = False

			elif curr_tool == "erase":
				xi, yi = int(i.landmark[12].x*640), int(i.landmark[12].y*480)
				y9  = int(i.landmark[9].y*480)

				if indexraise(yi, y9):
					cv2.circle(frame, (x, y), 30, (0,0,0), -1)
					cv2.circle(mask, (x, y), 30, 255, -1)

	op = cv2.bitwise_and(frame, frame, mask=mask)
	frame[:, :, 1] = op[:, :, 1]
	frame[:, :, 2] = op[:, :, 2]

	frame[:ymax, width:xmax] = cv2.addWeighted(tools, 0.7, frame[:ymax, width:xmax], 0.3, 0)
	cv2.putText(frame, curr_tool, (270+width,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
	cv2.imshow("paint app", frame)

	if cv2.waitKey(1) == ord("q"):
		break
cv2.destroyAllWindows()
cap.release()