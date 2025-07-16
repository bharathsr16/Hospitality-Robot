from hospitality_robot.text_interaction import handle_text_input, get_intent
from hospitality_robot.voice_interaction import listen, speak
from hospitality_robot.visual_capture import capture_and_detect_faces
from hospitality_robot.mapping import load_map, find_location, get_location_details
from hospitality_robot.navigation import RobotNavigator
import os
import nltk

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
    except LookupError:
        nltk.download('maxent_ne_chunker')
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words')

def main():
    download_nltk_data()
    """
    Main function for the hospitality robot.
    """
    # Get the absolute path to the map file
    map_file = os.path.join(os.path.dirname(__file__), "..", "tests", "test_map.yaml")

    # Load the map
    map_data = load_map(map_file)
    navigator = RobotNavigator(map_data)


    while True:
        # Get user input
        user_input = input("Choose an interaction type (text, voice, visual, move, or quit): ")

        if user_input == "text":
            text = input("Enter text: ")
            intent, data = get_intent(text)
            if intent == "find_location":
                location = find_location(map_data, data)
                if location:
                    description, events = get_location_details(location)
                    response = f"Found {data} at ({location['x']}, {location['y']}). {description}"
                    if events:
                        response += f" Events: {', '.join(events)}"
                    print(response)
                else:
                    print(f"Could not find {data}")
            else:
                response = handle_text_input(text)
                print(response)
        elif user_input == "voice":
            text = listen()
            if text:
                intent, data = get_intent(text)
                if intent == "find_location":
                    location = find_location(map_data, data)
                    if location:
                        description, events = get_location_details(location)
                        response = f"Found {data} at ({location['x']}, {location['y']}). {description}"
                        if events:
                            response += f" Events: {', '.join(events)}"
                        speak(response)
                    else:
                        speak(f"Could not find {data}")
                else:
                    response = handle_text_input(text)
                    speak(response)
        elif user_input == "visual":
            response = capture_and_detect_faces()
            print(response)
        elif user_input == "move":
            location_name = input("Enter a location to move to: ")
            response = navigator.move_to(location_name)
            print(response)
            name, position = navigator.get_current_position()
            print(f"Current Position: {name} ({position['x']}, {position['y']})")
        elif user_input == "quit":
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
