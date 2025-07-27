import cv2
import os
import numpy as np
from gtts import gTTS
from playsound import playsound


def detect_faces(image_path):
    """
    Detects faces in an image.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None

    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return faces


def greet_guest():
    """
    Greets the guest.
    """
    greeting_text = "Hello! Welcome to the event. How can I help you?"
    print(greeting_text)
    tts = gTTS(text=greeting_text, lang='en')
    # Use a path that is guaranteed to be writable
    audio_path = "/tmp/greeting.mp3"
    tts.save(audio_path)
    try:
        playsound(audio_path)
    except Exception as e:
        print(f"Error playing sound: {e}")
        print("Please ensure you have a display environment for playsound to work, or install pygobject.")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == '__main__':
    # We'll assume a test image is present in the same directory
    test_image_path = 'hospitality_robot/vision/test_image.jpg'

    # To make this runnable, let's create a dummy image file.
    # In a real scenario, this image would be provided by the user.
    if not os.path.exists(test_image_path):
        dummy_image = np.zeros((200, 200, 3), dtype=np.uint8)
        dummy_image[:] = (128, 128, 128)  # Gray background
        cv2.imwrite(test_image_path, dummy_image)

    faces = detect_faces(test_image_path)

    if faces is not None and len(faces) > 0:
        print(f"Found {len(faces)} faces.")
        greet_guest()
    elif faces is not None:
        print("Found 0 faces.")
    else:
        print("No faces detected or error in processing.")
