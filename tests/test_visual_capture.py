import unittest
from unittest.mock import patch, MagicMock
from hospitality_robot.visual_capture import capture_and_detect_faces
import cv2
import numpy as np
import os

class TestVisualCapture(unittest.TestCase):

    def setUp(self):
        # Create a dummy image with a face
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Draw a "face"
        cv2.rectangle(self.test_image, (20, 20), (80, 80), (255, 255, 255), -1)
        cv2.imwrite("tests/test_image.png", self.test_image)


    @patch('hospitality_robot.visual_capture.cv2.VideoCapture')
    def test_capture_and_detect_faces(self, mock_videocapture):
        # Mock the VideoCapture object
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, self.test_image)
        mock_videocapture.return_value = mock_cap

        # Run the function
        result = capture_and_detect_faces()

        # Check the result
        self.assertTrue(result.startswith("Detected"))
        self.assertTrue(os.path.exists("detected_faces.jpg"))

    def tearDown(self):
        if os.path.exists("tests/test_image.png"):
            os.remove("tests/test_image.png")
        if os.path.exists("detected_faces.jpg"):
            os.remove("detected_faces.jpg")


if __name__ == '__main__':
    unittest.main()
