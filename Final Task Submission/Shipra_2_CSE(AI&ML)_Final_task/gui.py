import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
from PIL import Image, ImageTk

def capture_image():
    subprocess.run(["python", "dataset/dataset.py"])

def detect_face():
    subprocess.run(["python", "dataset/face_detect.py"])

def open_file_dialog():
    filename = filedialog.askopenfilename()
    print("Selected File:", filename)
root = tk.Tk()
root.title("Attendance System")
root.geometry("500x400")
root.configure(bg="#FFA07A")
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(expand=True)
logo_image = Image.open("images.png") 
logo_image = logo_image.resize((150, 150))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(frame, image=logo_photo, bg="#f0f0f0")
logo_label.image = logo_photo 
logo_label.pack(pady=10)
heading_label = tk.Label(frame, text="Face Attendance System", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
heading_label.pack(pady=10)
style = ttk.Style()
style.configure("TButton", font=("ARIAL", 20), padding=10, background="#3498db", foreground="#A52A2A")
capture_button = ttk.Button(frame, text="Register Name", command=capture_image)
detect_button = ttk.Button(frame, text="Give Attendance", command=detect_face)
file_dialog_button = ttk.Button(frame, text="Open File Dialog", command=open_file_dialog)
capture_button.pack(pady=10, padx=20, fill=tk.X)
detect_button.pack(pady=10, padx=20, fill=tk.X)
file_dialog_button.pack(pady=10, padx=20, fill=tk.X)
root.mainloop()

