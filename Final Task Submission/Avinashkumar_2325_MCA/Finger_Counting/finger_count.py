import cv2
from cvzone.HandTrackingModule import HandDetector
import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

# streamlit
"""
# Finger Counting
using cvzone HandDetector by `Avinash Singh`
"""


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector()


frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")

while True and not stop_button_pressed:
    ret, frame = cap.read()
    if ret is True:
        hands, frame = detector.findHands(frame, draw=True)
        if hands:
            for hand in hands:      
                fingers = detector.fingersUp(hand)
                x, y, w, h = hand["bbox"]
                totalFingers = fingers.count(1)
                cv2.putText(frame, f"Fingers Held Up: {totalFingers}", (x - 20, y + h + 50),
                            cv2.FONT_HERSHEY_DUPLEX, 1.1, (0, 0, 255), 2)
        # else:
        #     points.clear()
        frame_placeholder.image(frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
            frame_placeholder.empty()
            break

cap.release()
cv2.destroyAllWindows()