from hospitality_robot.text_interaction import handle_text_input
from hospitality_robot.voice_interaction import listen, speak
from hospitality_robot.visual_capture import capture_image, process_image
from hospitality_robot.mapping import load_map, find_location

import os

def main():
    """
    Main function for the hospitality robot.
    """
    # Get the absolute path to the map file
    map_file = os.path.join(os.path.dirname(__file__), "..", "tests", "test_map.yaml")


    # Load the map
    map_data = load_map(map_file)

    while True:
        # Get user input
        user_input = input("Choose an interaction type (text, voice, visual, map, or quit): ")

        if user_input == "text":
            text = input("Enter text: ")
            response = handle_text_input(text)
            print(response)
        elif user_input == "voice":
            text = listen()
            if text:
                response = handle_text_input(text)
                speak(response)
        elif user_input == "visual":
            image_path = capture_image()
            processed_image = process_image(image_path)
            print(processed_image)
        elif user_input == "map":
            location_name = input("Enter a location to find: ")
            location = find_location(map_data, location_name)
            if location:
                print(f"Found {location_name} at ({location['x']}, {location['y']})")
            else:
                print(f"Could not find {location_name}")
        elif user_input == "quit":
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
