import cv2
import mediapipe as mp

import math


def calculate_distance(point1, point2):
    distance = math.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
        + (point1.z - point2.z) ** 2
    )
    return distance
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            middle_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP
            ]
            middle_mcp = hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_MCP
            ]

            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]

            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

            thumb_tip_to_mcp_distance = calculate_distance(thumb_tip, thumb_mcp)

            if calculate_distance(thumb_tip, thumb_mcp) > 0.16:
                finger_count += 1
            if calculate_distance(index_tip, index_mcp) > 0.18:
                finger_count += 1
            if calculate_distance(middle_tip, middle_mcp) > 0.18:
                finger_count += 1
            if calculate_distance(ring_tip, ring_mcp) > 0.18:
                finger_count += 1
            if calculate_distance(pinky_tip, pinky_mcp) > 0.18:
                finger_count += 1

    cv2.putText(
        image,
        f"Finger Count: {finger_count}",
        (10, 30),
        cv2.FONT_HERSHEY_DUPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("Finger Counting", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()