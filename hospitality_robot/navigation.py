class RobotNavigator:
    def __init__(self, map_data):
        self.map_data = map_data
        self.current_position = map_data["entrance"]

    def move_to(self, location_name):
        """
        Moves the robot to a new location.
        """
        location = self.map_data.get(location_name)
        if location:
            self.current_position = location
            return f"Moved to {location_name}."
        else:
            return f"Could not find {location_name}."

    def get_current_position(self):
        """
        Gets the robot's current position.
        """
        for name, location in self.map_data.items():
            if location == self.current_position:
                return name, location
        return "Unknown", self.current_position
