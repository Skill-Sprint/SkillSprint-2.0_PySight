import cv2
import datetime as dt

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    date_time = str(dt.datetime.now())
    name = "Harsh"
    text = date_time +" " +name

    frame = cv2.putText(frame, text, (10, 420), cv2.FONT_HERSHEY_COMPLEX, 1, (30, 255, 255), 3, cv2.LINE_AA)
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
