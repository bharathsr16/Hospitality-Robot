import unittest
import os
from hospitality_robot.mapping import load_map, find_location

class TestMapping(unittest.TestCase):

    def setUp(self):
        self.map_file = "tests/test_map.yaml"
        self.map_data = load_map(self.map_file)

    def test_load_map(self):
        self.assertIsNotNone(self.map_data)
        self.assertIn("entrance", self.map_data)

    def test_find_location(self):
        location = find_location(self.map_data, "event_hall")
        self.assertIsNotNone(location)
        self.assertEqual(location["x"], 10)
        self.assertEqual(location["y"], 5)

        location = find_location(self.map_data, "non_existent_location")
        self.assertIsNone(location)

if __name__ == '__main__':
    unittest.main()
