import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import numpy as np
import csv
import openpyxl
import pyarrow


video_capture = cv2.VideoCapture(0)
anoushka_image = face_recognition.load_image_file('C:/Users/anous/PycharmProjects/attendance_project/Snapchat-1042236764.jpg')
anoushka_encode = face_recognition.face_encodings(anoushka_image)[0]

ian_image = face_recognition.load_image_file('C:/Users/anous/PycharmProjects/attendance_project/intro-1696883311.jpg')
ian_encode = face_recognition.face_encodings(ian_image)[0]

chandler_image = face_recognition.load_image_file('C:/Users/anous/PycharmProjects/attendance_project/download.jpg')
chandler_encode = face_recognition.face_encodings(chandler_image)[0]

known_encode = [anoushka_encode, ian_encode, chandler_encode]
known_names = ["Anoushka", "Ian", "Chandler"]

students = known_names.copy()

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        # Set canvas background color
        self.canvas = tk.Canvas(root, width=800, height=600, bg="orange")
        self.canvas.pack()

        # Make buttons rounded and change background color
        self.start_button = ttk.Button(root, text="Start Recognition", command=self.start_recognition, style='Rounded.TButton')
        self.start_button.pack(pady=10)

        self.new_user_button = ttk.Button(root, text="Add New User", command=self.add_new_user, style='Rounded.TButton')
        self.new_user_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit_app, style='Rounded.TButton')
        self.quit_button.pack(pady=10)

        # Create a custom style for rounded buttons
        self.style = ttk.Style()
        self.style.configure('Rounded.TButton', borderwidth=1, relief="flat", background="yellow", foreground="green")
        self.style.map('Rounded.TButton', background=[('active', 'red')])

        # Create or load the Excel sheet
        self.excel_file_path = 'C:/Users/anous/PycharmProjects/attendance_project/Attendance.xlsx'
        try:
            self.attendance_df = pd.read_excel(self.excel_file_path)
        except FileNotFoundError:
            # If the file does not exist, create a new one with columns
            self.attendance_df = pd.DataFrame(columns=['Name', 'Status', current_date])
            self.attendance_df.to_excel(self.excel_file_path, index=False)

    def start_recognition(self):
        while True:
            ret, frame = video_capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_encode, face_encoding)
                face_distance = face_recognition.face_distance(known_encode, face_encoding)
                best_match_index = np.argmin(face_distance)

                if matches[best_match_index]:
                    name = known_names[best_match_index]

                    if name in known_names:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        bottom_left_corner_of_text = (10, 100)
                        font_scale = 1.5
                        font_color = (255, 0, 0)
                        thickness = 3
                        line_type = 2
                        cv2.putText(frame, name + " present", bottom_left_corner_of_text, font, font_scale, font_color,
                                    thickness, line_type)

                        if name in students:
                            students.remove(name)
                            self.update_attendance(name, "P")

            self.display_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.root.update()

    def add_new_user(self):
        name = simpledialog.askstring("Input", "Enter user name:")
        if name is not None:
            images = self.take_images()
            if images:
                students.append(name)
                status = self.update_attendance(name, "A")  # Mark as absent for the current date
                messagebox.showinfo("Update Status", status)

    def take_images(self):
        images = []
        try:
            num_images = int(simpledialog.askstring("Input", "Enter the number of images to capture (at least 2):"))
            if num_images < 2:
                messagebox.showwarning("Warning", "Please capture at least 2 images.")
                return None

            for i in range(num_images):
                ret, frame = video_capture.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                if len(face_encodings) == 1:
                    images.append(face_encodings[0])

                cv2.imshow("Capture Image", cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))
                cv2.waitKey(1000)  # 1-second delay between captures

            return images

        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number.")
            return None

    def update_attendance(self, name, status):
        success = False

        if name not in self.attendance_df['Name'].values:
            # If the student is not in the DataFrame, add a new row
            new_row = pd.DataFrame([[name, status, ""]], columns=['Name', 'Status', current_date])
            self.attendance_df = pd.concat([self.attendance_df, new_row], ignore_index=True)
            success = True  # Changes were made
        else:
            # If the student is already in the DataFrame, update the status
            idx = self.attendance_df.index[self.attendance_df['Name'] == name].tolist()[0]
            self.attendance_df.at[idx, 'Status'] = status

        # Save the DataFrame to the Excel file
        self.attendance_df.to_excel(self.excel_file_path, index=False)

        # Check if any changes were made
        if success or self.attendance_df.at[name, 'Status'] == status:
            return "Success: Attendance updated."
        else:
            return "Failed: No changes made."

    def quit_app(self):
        video_capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
