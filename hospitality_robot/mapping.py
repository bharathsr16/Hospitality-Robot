import yaml

def load_map(map_file):
    """
    Loads a map from a YAML file.
    """
    with open(map_file, 'r') as f:
        map_data = yaml.safe_load(f)
    return map_data

def find_location(map_data, location_name):
    """
    Finds a location in the map data.
    """
    return map_data.get(location_name)

def get_location_details(location_data):
    """
    Gets the description and events for a location.
    """
    description = location_data.get("description", "No description available.")
    events = location_data.get("events", [])
    return description, events
