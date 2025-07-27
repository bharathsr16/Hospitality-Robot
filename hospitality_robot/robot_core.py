import json
import os

# --- Navigation Classes (kept from the original main.py) ---
import heapq

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, []).append(to_node)
        self.edges.setdefault(to_node, []).append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

# --- Main Robot Core Class ---

class RobotCore:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        if not self.config:
            raise ValueError(f"Failed to load or validate config: {config_path}")

        self.campus_name = self.config.get("name", "Unnamed Campus")
        self.locations = self.config.get("locations", {})
        self.events = self.config.get("events", [])
        self.graph = self._build_graph()

    def _load_config(self, config_path):
        """Loads and validates the JSON configuration file."""
        if not os.path.exists(config_path):
            print(f"Error: Configuration file not found at {config_path}")
            return None
        with open(config_path, 'r') as f:
            return json.load(f)

    def _build_graph(self):
        """Builds the graph from the config data."""
        graph = Graph()
        if "locations" in self.config:
            for loc in self.config["locations"]:
                graph.add_node(loc)

        if "graph" in self.config and "edges" in self.config["graph"]:
            for edge in self.config["graph"]["edges"]:
                graph.add_edge(edge["from"], edge["to"], edge["distance"])
        return graph

    def get_event_details(self, event_name):
        """Finds an event by its name."""
        for event in self.events:
            if event_name.lower() in event["name"].lower():
                return event
        return None

# Example of how to use it (for testing)
if __name__ == '__main__':
    # Assume we are in the root directory of the project for this test
    config_file = os.path.join('hospitality_robot', 'configs', 'main_campus.json')

    print(f"Loading configuration from: {config_file}")
    try:
        robot = RobotCore(config_file)
        print(f"Successfully loaded configuration for: {robot.campus_name}")

        print("\nAvailable Locations:")
        for loc in robot.locations:
            print(f"- {loc}")

        print("\nFetching event details for 'Tech Talk':")
        tech_talk = robot.get_event_details("Tech Talk")
        if tech_talk:
            print(f"Found: {tech_talk['name']} at {tech_talk['location']}")
        else:
            print("Could not find the event.")

    except ValueError as e:
        print(e)
