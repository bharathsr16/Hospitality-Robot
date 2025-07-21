import unittest
from hospitality_robot.navigation import RobotNavigator
from hospitality_robot.mapping import load_map

class TestNavigation(unittest.TestCase):
    def setUp(self):
        self.map_data = load_map("tests/test_map.yaml")
        self.navigator = RobotNavigator(self.map_data)

    def test_move_to(self):
        response = self.navigator.move_to("event_hall")
        self.assertEqual(response, "Moved to event_hall.")
        name, position = self.navigator.get_current_position()
        self.assertEqual(name, "event_hall")

    def test_move_to_non_existent_location(self):
        response = self.navigator.move_to("non_existent_location")
        self.assertEqual(response, "Could not find non_existent_location.")
        name, position = self.navigator.get_current_position()
        self.assertEqual(name, "entrance")

if __name__ == '__main__':
    unittest.main()
