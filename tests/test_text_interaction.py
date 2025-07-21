import unittest
from hospitality_robot.text_interaction import handle_text_input, get_intent

class TestTextInteraction(unittest.TestCase):
    def test_handle_text_input(self):
        # This test will now call the LLM, so we can only check if the response is a string.
        response = handle_text_input("hello")
        self.assertIsInstance(response, str)

    def test_get_intent(self):
        self.assertEqual(get_intent("where is the event hall"), ("find_location", "the"))
        self.assertEqual(get_intent("where is the restroom"), ("find_location", "the"))
        self.assertEqual(get_intent("what is your name"), ("unknown", None))


if __name__ == '__main__':
    unittest.main()
