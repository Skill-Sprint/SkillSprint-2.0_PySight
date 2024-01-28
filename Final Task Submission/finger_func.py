import cv2
import mediapipe as mp
import math
import tkinter as tk
from PIL import Image, ImageTk


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


class FingerCountApp:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Finger Counting App")

        self.cap = cv2.VideoCapture(video_source)

        self.large_font = ("Helvetica", 20)

        self.label = tk.Label(root, text="Finger Count:", font=self.large_font)
        self.label.pack()

        self.finger_count_label = tk.Label(root, text="0", font=self.large_font)
        self.finger_count_label.pack()

        self.video_panel = tk.Label(root)
        self.video_panel.pack()

        self.update()

    def update(self):
        success, image = self.cap.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        finger_count = 0

        results = hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

                index_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]
                index_mcp = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_MCP
                ]

                middle_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP
                ]
                middle_mcp = hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_MCP
                ]

                ring_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.RING_FINGER_TIP
                ]
                ring_mcp = hand_landmarks.landmark[
                    mp_hands.HandLandmark.RING_FINGER_MCP
                ]

                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

                thumb_tip_to_mcp_distance = calculate_distance(thumb_tip, thumb_mcp)
                if thumb_tip_to_mcp_distance > 0.16:
                    finger_count += 1
                if calculate_distance(index_tip, index_mcp) > 0.18:
                    finger_count += 1
                if calculate_distance(middle_tip, middle_mcp) > 0.18:
                    finger_count += 1
                if calculate_distance(ring_tip, ring_mcp) > 0.18:
                    finger_count += 1
                if calculate_distance(pinky_tip, pinky_mcp) > 0.18:
                    finger_count += 1

        self.finger_count_label.config(text=str(finger_count))

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(image_rgb)
        img = ImageTk.PhotoImage(img)

        self.video_panel.config(image=img)
        self.video_panel.image = img

        self.root.after(1, self.update)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = FingerCountApp(root)
    app.run()