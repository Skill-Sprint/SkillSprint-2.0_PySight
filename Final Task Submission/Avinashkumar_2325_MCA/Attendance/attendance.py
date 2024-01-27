import cv2
import os
import numpy as np
import time
import datetime as dt
import streamlit as st
from st_pages import add_page_title,show_pages, Page
import pandas as pd



add_page_title()

show_pages(
    [
        Page("dataset.py", "Create Dataset", "💾"),
        Page("attendance.py", "Attendance", "😀"),
    ]
)

haar_file = "haarcascade_frontalface_default.xml"

datasets = os.getcwd() + "/Dataset"


# check if any datasets are available
if not os.path.isdir(datasets):
    st.write("Please Enter your face in the Dataset")
    exit()

# frame
frame_placeholder = st.empty()

# walk through all the datasets and load them in images, labels, names and id


(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id = id + 1

(images, labels) = [np.array(lists) for lists in [images, labels]]

if len(names) == 0 or len(images) == 0:
    st.write("Please Enter your face in the Dataset")
    exit()


# create the model using LBPHFaceRecognizer
model = cv2.face.LBPHFaceRecognizer.create()
# train the model with the images and respective names
model.train(images, labels)

# set the classifier for the face with the xml file
face_cascade = cv2.CascadeClassifier(haar_file)

# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    stop_button_pressed = st.button("Stop")
with col2:
    start_attendance = st.button("Start Attendance")
with col3:
    st.link_button("Enter a Person", "Create Dataset")

count = 1

attendance = {
    "Name": [name for name in names.values()],
    "Status": ["Absent"] * len(names),
    "Time": [""] * len(names)
}

df = pd.DataFrame(attendance)

attendance_table = st.dataframe(df, width=600)


def update_attendance(attendance):
    df = pd.DataFrame(attendance)
    attendance_table.table(df)
    st.session_state.attendance = df


export_csv = st.button("Export to CSV")
if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame()
if export_csv:
    st.session_state.attendance.to_csv(f"attendance_{dt.date.today()}.csv", index=False, mode="w")

while start_attendance:
    ret, frame = cap.read()
    if ret is True:
        now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # change color to gray
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the captured frame
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 4)
        # detectMultiScale(source, scaleFactor, minNeighbors)

        for (x, y, w, h) in faces:
            # create rectangles around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

            # separate face from the image
            face = img_gray[y:y + h, x:x + h]

            # resize the face
            face_resize = cv2.resize(face, (640, 400))

            # using the model, check for the face in the datasets
            predictions = model.predict(face_resize)

            # set a threshold for the difference between captured image and image in dataset (30)
            if predictions[1] < 30:
                # show name if face found in dataset
                name = names[predictions[0]].strip()
                cv2.putText(frame, '%s' % name, (x + 5, y + 25 + h),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1.5, (20, 185, 20), 2)

                if name in attendance["Name"]:
                    i = attendance["Name"].index(name)
                    if attendance["Status"][i] != "Present":
                        attendance["Status"][i] = "Present"
                        attendance["Time"][i] = now
                        update_attendance(attendance)

            else:
                # show Unknown otherwise
                cv2.putText(frame, "Unknown", (x + 5, y + 25 + h), cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (0, 0, 255), 2)

        # Date and Time on top left
        cv2.putText(frame, now, (20, 20), cv2.FONT_HERSHEY_DUPLEX,
                    0.7, (255, 0, 0), 2)
        frame_placeholder.image(frame, channels="BGR")

        # cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
            frame_placeholder.empty()
            break

cap.release()
