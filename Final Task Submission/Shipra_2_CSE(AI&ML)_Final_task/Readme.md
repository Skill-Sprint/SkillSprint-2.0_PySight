# Face Recognition Attendance System

## Overview

This project is a face recognition attendance system using OpenCV and the LBPH face recognizer. It captures faces through the webcam, recognizes the faces, and logs attendance information to a CSV file.

## Prerequisites

- Python 3.x
- OpenCV
- NumPy

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/shipraa18/SkillSprint-2.0_PySight.git
    cd Shipra_2_CSE(AI&ML)_Final_task
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```bash
    python face_detect.py
    ```

2. The script will use the webcam to capture faces, recognize them, and log attendance information to a CSV file.

3. Press 'q' to exit the application.

## Configuration

- Modify the `datasets` variable in `face_detect.py` to point to the directory containing your training datasets.

- Adjust the recognition threshold (`if prediction[1] < 74`) in the script based on your needs.

## File Structure

- `face_detect.py`: Main script for face recognition and attendance logging.
- `haarcascade_frontalface_default.xml`: Haar cascade file for face detection.
- `dataset/`: Directory containing training datasets for face recognition.

## Acknowledgments

- [OpenCV](https://opencv.org/): Open Source Computer Vision Library

