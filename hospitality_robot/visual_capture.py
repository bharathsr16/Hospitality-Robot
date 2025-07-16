import cv2
import os

def capture_and_detect_faces():
    """
    Captures an image from the camera and detects faces.
    """
    # Load the Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Capture an image from the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Cannot open camera"
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Cannot read frame"

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Save the image with the detected faces
    image_path = "detected_faces.jpg"
    cv2.imwrite(image_path, frame)

    return f"Detected {len(faces)} faces. Image saved to {image_path}"
