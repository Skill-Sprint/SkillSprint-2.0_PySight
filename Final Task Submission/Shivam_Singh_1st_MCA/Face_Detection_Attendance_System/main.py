import face_recognition as ftr
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
from datetime import datetime


class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")

        self.video_capture = cv2.VideoCapture(0)

        self.label = ttk.Label(root, text="Face Recognition Attendance")
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.start_button = ttk.Button(root, text="Start Taking Attendance", command=self.start_recognition)
        self.start_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack(pady=10)

        self.known_face_encodings = []
        self.known_face_names = ["modi_ji", "elon_musk", "srk"]

        for name in self.known_face_names:
            image = ftr.load_image_file(f"known_faces/{name}.jpg")
            encoding = ftr.face_encodings(image)[0]
            self.known_face_encodings.append(encoding)

        self.recognizing = False
        self.attendance = {}
        self.known_person_attendance = {}

        self.update()

    def start_recognition(self):
        self.recognizing = not self.recognizing
        if not self.recognizing:
            self.save_attendance()

    def save_attendance(self):
        today = datetime.now().strftime("%d-%m-%y")
        filename = f"attendance_{today}.csv"

        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write known person attendance
            for name, time in self.known_person_attendance.items():
                writer.writerow([name, time])

    def quit_app(self):
        self.video_capture.release()
        self.root.destroy()

    def update(self):
        ret, frame = self.video_capture.read()

        if self.recognizing:
            face_locations = ftr.face_locations(frame)
            face_encodings = ftr.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = ftr.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown Person"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                    # Record attendance for known persons
                    if name in self.known_face_names:
                        if name not in self.known_person_attendance:
                            self.known_person_attendance[name] = datetime.now().strftime("%H:%M:%S")

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 255), 1)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)

            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

        if self.recognizing:
            self.root.after(10, self.update)
        else:
            self.canvas.delete("all")
            self.root.after(100, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()
