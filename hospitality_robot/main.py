import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from vision.face_detector import greet_guest
from navigation.pathfinder import Graph, a_star_search, reconstruct_path
from database.event_manager import get_event_details

def setup_campus_map():
    # Create a sample campus map
    campus_map = Graph()
    locations = {
        'Entrance': (0, 0),
        'Auditorium': (10, 10),
        'Block A': (5, 5),
        'Block B': (20, 5),
        'Exhibition Hall': (15, 15),
        'Open Air Theatre': (25, 0)
    }
    for loc in locations:
        campus_map.add_node(loc)

    campus_map.add_edge('Entrance', 'Block A', 10)
    campus_map.add_edge('Block A', 'Auditorium', 5)
    campus_map.add_edge('Block A', 'Block B', 15)
    campus_map.add_edge('Block B', 'Exhibition Hall', 5)
    campus_map.add_edge('Block B', 'Open Air Theatre', 20)
    campus_map.add_edge('Auditorium', 'Exhibition Hall', 10)

    return campus_map, locations

def main():
    print("Hospitality Robot Activated.")

    # Setup campus map
    campus_map, locations = setup_campus_map()

    # 1. Simulate guest detection
    print("Guest detected.")

    # 2. Greet the guest
    greet_guest()

    # 3. Simulate a voice command
    command = "where is the tech talk"
    print(f"\nSimulated command: '{command}'")

    # 4. Process the command
    if "where is the" in command:
        event_name = command.split("where is the")[-1].strip()
        event = get_event_details(event_name)
        if event:
            destination = event[2] # Location of the event
            start_location = 'Entrance' # Assuming the robot is at the entrance

            if destination in locations:
                came_from, cost_so_far = a_star_search(campus_map, start_location, destination, locations)
                path = reconstruct_path(came_from, start_location, destination)
                directions = " -> ".join(path)
                response = f"To get to the {event[1]}, you can follow this path: {directions}"
                print(response)
                # speak(response) # Audio playback is disabled for now
            else:
                response = f"I know about the {event_name}, but I don't have its location on my map."
                print(response)
        else:
            response = f"Sorry, I couldn't find any event named {event_name}."
            print(response)
    else:
        print("No guest detected.")

if __name__ == '__main__':
    main()
