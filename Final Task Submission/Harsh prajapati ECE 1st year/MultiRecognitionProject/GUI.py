import tkinter as tk
from tkinter import messagebox

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")

        self.students = ["1. Abdul Kalam", "2. Bhagat Singh", "3. Bill Gates", "4. Satya Nadela", "5. Steve Jobs", "6. Sundar Pichai"]
        self.attendance_dict = {student: False for student in self.students}

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Mark Attendance", font=("Times New Roman", 16, "bold underline"), fg="blue")
        self.label.pack(pady=10)

        self.student_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=len(self.students), font=("Times New Roman", 12))
        for student in self.students:
            self.student_listbox.insert(tk.END, student)
        self.student_listbox.pack(pady=10)

        self.mark_button = tk.Button(self.root, text="Mark Attendance", command=self.mark_attendance)
        self.mark_button.pack(pady=10)

    def mark_attendance(self):
        selected_indices = self.student_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one student.")
            return

        for index in selected_indices:
            student_name = self.students[index]
            self.attendance_dict[student_name] = True

        self.show_attendance()

    def show_attendance(self):
        attendance_list = [f"{student}: {'Present' if present else 'Absent'}" for student, present in self.attendance_dict.items()]
        attendance_message = "\n".join(attendance_list)

        messagebox.showinfo("Attendance", f"Attendance:\n{attendance_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()
