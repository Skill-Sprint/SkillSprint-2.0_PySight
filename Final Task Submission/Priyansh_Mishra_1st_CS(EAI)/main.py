import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

video = cv2.VideoCapture(0)

def is_finger_up(hand_landmarks, index):
    if index == 0:  # Thumb
        return hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y
    else:
        return hand_landmarks.landmark[index * 2 + 2].y > hand_landmarks.landmark[index * 2 + 1].y and \
               hand_landmarks.landmark[index * 2 + 2].y > hand_landmarks.landmark[index * 2].y

while True:
    ret, frame = video.read()
    if not ret:
        continue

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(rgb_frame)

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Count the number of fingers raised
            finger_count = 0

            # Thumb
            if is_finger_up(hand_landmarks, 0):
                finger_count += 1
            # Index finger
            if is_finger_up(hand_landmarks, 1):
                finger_count += 1
            # Middle finger
            if is_finger_up(hand_landmarks, 2):
                finger_count += 1
            # Ring finger
            if is_finger_up(hand_landmarks, 3):
                finger_count += 1
            # Little finger
            if is_finger_up(hand_landmarks, 4):
                finger_count += 1

            # Display the number of fingers
            cv2.putText(frame, f'Finger Count: {finger_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Finger Count', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()