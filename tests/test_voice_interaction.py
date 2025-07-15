import unittest
from unittest.mock import patch, MagicMock
from hospitality_robot.voice_interaction import listen, speak

class TestVoiceInteraction(unittest.TestCase):

    @patch('hospitality_robot.voice_interaction.sr.Recognizer')
    @patch('hospitality_robot.voice_interaction.sr.Microphone')
    def test_listen(self, mock_microphone, mock_recognizer):
        # Mock the audio input
        mock_audio = MagicMock()
        mock_recognizer.return_value.listen.return_value = mock_audio
        mock_recognizer.return_value.recognize_google.return_value = "hello"

        # Test the listen function
        self.assertEqual(listen(), "hello")

    @patch('hospitality_robot.voice_interaction.pyttsx3.init')
    def test_speak(self, mock_init):
        # Mock the speech engine
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine

        # Test the speak function
        speak("hello")
        mock_engine.say.assert_called_once_with("hello")
        mock_engine.runAndWait.assert_called_once()

if __name__ == '__main__':
    unittest.main()
