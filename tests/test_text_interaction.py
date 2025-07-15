import unittest
from hospitality_robot.text_interaction import handle_text_input

class TestTextInteraction(unittest.TestCase):
    def test_handle_text_input(self):
        self.assertEqual(handle_text_input("hello"), "Hello! How can I help you today?")
        self.assertEqual(handle_text_input("goodbye"), "I'm sorry, I don't understand. Please try again.")

if __name__ == '__main__':
    unittest.main()
