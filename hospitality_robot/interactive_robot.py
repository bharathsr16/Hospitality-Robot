import os
import sys
import glob

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from robot_core import RobotCore
from navigation.pathfinder import a_star_search, reconstruct_path

def list_configs(config_dir):
    """Lists available .json configuration files."""
    return glob.glob(os.path.join(config_dir, '*.json'))

def select_config(config_files):
    """Prompts the user to select a configuration file."""
    print("Please select a campus configuration to load:")
    for i, f in enumerate(config_files):
        print(f"[{i + 1}] {os.path.basename(f)}")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(config_files):
                return config_files[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

from datetime import datetime

def parse_time(time_str):
    """Parses time from HH:MM format."""
    return datetime.strptime(time_str, '%H:%M').time()

def voice_assistant(robot):
    """Simulates a more advanced, text-based voice assistant."""
    print("\n--- Voice Assistant Mode ---")
    print("You can ask me things like:")
    print("- 'Where is the Tech Talk?'")
    print("- 'Tell me about the Project Expo.'")
    print("- 'What events are happening now?' (e.g., at 11:00)")
    print("- 'List all locations.'")
    print("Type 'exit' to return to the main menu.")

    while True:
        command = input("Ask me something: ").strip().lower()

        if command == 'exit':
            break

        # Intent: Get directions
        if command.startswith("where is"):
            event_name = command.replace("where is the", "").strip()
            event = robot.get_event_details(event_name)
            if event:
                start, goal = "Entrance", event['location']
                came_from, _ = a_star_search(robot.graph, start, goal, robot.locations)
                path = reconstruct_path(came_from, start, goal)
                if path:
                    print(f"To get to the {event['name']}, you can follow this path: {' -> '.join(path)}")
                else:
                    print(f"I know where the {event['name']} is, but I can't find a path.")
            else:
                print(f"Sorry, I don't know about an event called '{event_name}'.")

        # Intent: Get event description
        elif command.startswith("tell me about"):
            event_name = command.replace("tell me about the", "").strip()
            event = robot.get_event_details(event_name)
            if event:
                print(f"Here's the description for {event['name']}: {event['description']}")
            else:
                print(f"Sorry, I couldn't find an event called '{event_name}'.")

        # Intent: Find current events
        elif "what events are happening now" in command:
            try:
                time_str = input("What time is it now? (e.g., 11:00): ").strip()
                current_time = parse_time(time_str)
                ongoing_events = []
                for event in robot.events:
                    if parse_time(event['start_time']) <= current_time <= parse_time(event['end_time']):
                        ongoing_events.append(event)
                if ongoing_events:
                    print("\n--- Ongoing Events ---")
                    for event in ongoing_events:
                        print(f"- {event['name']} at {event['location']}")
                else:
                    print("There are no events happening at that time.")
            except ValueError:
                print("Invalid time format. Please use HH:MM.")

        # Intent: List all locations
        elif "list all locations" in command:
             print("\n--- All Locations ---")
             for loc in robot.locations:
                print(f"- {loc}")

        else:
            print("I'm sorry, I didn't understand that. Please try again.")


def main_menu(robot):
    """Displays the main interaction menu."""
    while True:
        print(f"\n--- {robot.campus_name} Main Menu ---")
        print("[1] Use Voice Assistant")
        print("[2] Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            voice_assistant(robot)

        elif choice == '2':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

def run_test_mode(robot):
    """Runs a non-interactive test of the main functionalities."""
    print("--- Running in Test Mode ---")

    # Test 1: Get directions
    print("\n--- Test 1: Get directions to 'Tech Talk' ---")
    event = robot.get_event_details("Tech Talk")
    start, goal = "Entrance", event['location']
    came_from, _ = a_star_search(robot.graph, start, goal, robot.locations)
    path = reconstruct_path(came_from, start, goal)
    if path:
        print(f"Path to {event['name']}: {' -> '.join(path)}")
    else:
        print("Path not found.")

    # Test 2: Get event description
    print("\n--- Test 2: Get details for 'Project Expo' ---")
    event = robot.get_event_details("Project Expo")
    if event:
        print(f"Description: {event['description']}")
    else:
        print("Event not found.")

    # Test 3: Find current events at 11:45
    print("\n--- Test 3: Find ongoing events at 11:45 ---")
    current_time = parse_time("11:45")
    ongoing_events = [e for e in robot.events if parse_time(e['start_time']) <= current_time <= parse_time(e['end_time'])]
    if ongoing_events:
        for event in ongoing_events:
            print(f"- {event['name']} is happening now at {event['location']}.")
    else:
        print("No events are happening at this time.")

    # Test 4: List all locations
    print("\n--- Test 4: List all locations ---")
    for loc in robot.locations:
        print(f"- {loc}")

    print("\n--- Test Mode Complete ---")

if __name__ == '__main__':
    config_dir = os.path.join(os.path.dirname(__file__), 'configs')
    configs = list_configs(config_dir)

    if not configs:
        print("No configuration files found. Exiting.")
        sys.exit(1)

    # Check for a command-line argument to run in test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # In test mode, just use the first available config
        selected_config = configs[0]
        try:
            robot = RobotCore(selected_config)
            run_test_mode(robot)
        except ValueError as e:
            print(f"Error loading robot configuration: {e}")
            sys.exit(1)
    else:
        # Run in interactive mode
        selected_config = select_config(configs)
        try:
            robot = RobotCore(selected_config)
            main_menu(robot)
        except ValueError as e:
            print(f"Error loading robot configuration: {e}")
            sys.exit(1)
