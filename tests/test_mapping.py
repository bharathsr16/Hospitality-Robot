import unittest
import os
from hospitality_robot.mapping import load_map, find_location, get_location_details

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

    def test_get_location_details(self):
        location = find_location(self.map_data, "event_hall")
        description, events = get_location_details(location)
        self.assertEqual(description, "The main event hall.")
        self.assertEqual(events, ["Tech Conference 2025", "Annual College Fest"])

        location = find_location(self.map_data, "restroom")
        description, events = get_location_details(location)
        self.assertEqual(description, "The restroom near the entrance.")
        self.assertEqual(events, [])


if __name__ == '__main__':
    unittest.main()
