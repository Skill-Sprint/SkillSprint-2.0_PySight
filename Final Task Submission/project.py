import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

INDEX_FINGER_TIP = 8
THUMB_TIP = 4
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16
PINKY_TIP = 20

ERASE_DISTANCE_THRESHOLD = 20  # Adjust as needed
ERASE_GESTURE = [THUMB_TIP, INDEX_FINGER_TIP, MIDDLE_FINGER_TIP, RING_FINGER_TIP, PINKY_TIP]

cap = cv2.VideoCapture(0)
canvas_width, canvas_height = 640, 480

canvas = np.zeros((480, 640, 3), dtype=np.uint8)
drawing = False  # Flag to indicate whether drawing is active
last_point = None  # Last point to connect lines

drawing = False  # Flag to indicate whether drawing is active
eraser_mode = False  # Flag to indicate whether the eraser mode is active

while True:
    ret, frame = cap.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:    # If hands are detected, draw landmarks on the frame
        for landmarks in results.multi_hand_landmarks:
            for point in landmarks.landmark:
                x, y, _ = int(point.x * frame.shape[1]), int(point.y * frame.shape[0]), int(point.z * frame.shape[1])
                cv2.circle(frame, (x, y), 10,(156, 100, 231), -1)

    if not ret:
        print("Error: Couldn't read frame from the camera.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        index_finger_tip = landmarks[INDEX_FINGER_TIP]

        thumb_tip = landmarks[THUMB_TIP]
        middle_finger_tip = landmarks[MIDDLE_FINGER_TIP]
        thumb_to_middle_distance = int((thumb_tip.x - middle_finger_tip.x) * frame.shape[1])

        if thumb_to_middle_distance < ERASE_DISTANCE_THRESHOLD:
            drawing = not drawing

        if drawing:
            if last_point:
                current_point = (int(index_finger_tip.x * canvas_width), int(index_finger_tip.y * canvas_height))
                cv2.line(canvas, last_point, current_point, (255, 255, 255), 5)
                last_point = current_point
            else:
                last_point = (int(index_finger_tip.x * canvas_width), int(index_finger_tip.y * canvas_height))
        else:
            last_point = None
    if eraser_mode:
        # Check if all specified fingertips are close together
        erase_gesture_distance = sum(
            int((landmarks[i].x - landmarks[j].x) * frame.shape[1]) for i, j in
            zip(ERASE_GESTURE[:-1], ERASE_GESTURE[1:]))
        if erase_gesture_distance < ERASE_DISTANCE_THRESHOLD:
            cv2.putText(frame, "Eraser Mode", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # Update the canvas based on the drawing flag
    if drawing:
        cv2.circle(canvas, (int(index_finger_tip.x * canvas_width), int(index_finger_tip.y * canvas_height)), 10,(156, 100, 231), -1)

    combined_frame = np.hstack((frame, canvas))

    cv2.imshow("Combined Frame", combined_frame)
    if cv2.waitKey(1) == ord("q"):
         break

cap.release()
cv2.destroyAllWindows()
