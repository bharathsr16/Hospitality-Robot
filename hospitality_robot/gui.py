import sys
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from hospitality_robot.text_interaction import get_intent, handle_text_input
from hospitality_robot.voice_interaction import listen, speak
from hospitality_robot.visual_capture import capture_and_detect_faces
from hospitality_robot.mapping import load_map, find_location, get_location_details
from hospitality_robot.navigation import RobotNavigator
import os

class RobotGui(QWidget):
    def __init__(self):
        super().__init__()
        # Get the absolute path to the map file
        map_file = os.path.join(os.path.dirname(__file__), "..", "tests", "test_map.yaml")
        self.map_data = load_map(map_file)
        self.navigator = RobotNavigator(self.map_data)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Hospitality Robot')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.position_label = QLabel()
        self.update_position_label()
        self.layout.addWidget(self.position_label)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.layout.addWidget(self.output_area)

        self.input_area = QLineEdit()
        self.input_area.returnPressed.connect(self.handle_text_input_gui)
        self.layout.addWidget(self.input_area)

        self.voice_button = QPushButton("Speak")
        self.voice_button.clicked.connect(self.handle_voice_input)
        self.layout.addWidget(self.voice_button)

        self.visual_button = QPushButton("Capture Image")
        self.visual_button.clicked.connect(self.handle_visual_input)
        self.layout.addWidget(self.visual_button)

    def update_position_label(self):
        name, position = self.navigator.get_current_position()
        self.position_label.setText(f"Current Position: {name} ({position['x']}, {position['y']})")

    def handle_text_input_gui(self):
        user_input = self.input_area.text()
        self.input_area.clear()
        self.output_area.append(f"You: {user_input}")

        intent, data = get_intent(user_input)
        if intent == "find_location":
            location = find_location(self.map_data, data)
            if location:
                description, events = get_location_details(location)
                response = f"Found {data} at ({location['x']}, {location['y']}). {description}"
                if events:
                    response += f" Events: {', '.join(events)}"
                self.output_area.append(f"Robot: {response}")
            else:
                self.output_area.append(f"Robot: Could not find {data}")
        elif "go to" in user_input.lower():
            location_name = user_input.lower().replace("go to", "").strip()
            response = self.navigator.move_to(location_name)
            self.output_area.append(f"Robot: {response}")
            self.update_position_label()
        else:
            response = handle_text_input(user_input)
            self.output_area.append(f"Robot: {response}")


    def handle_voice_input(self):
        user_input = listen()
        if user_input:
            self.output_area.append(f"You: {user_input}")
            intent, data = get_intent(user_input)
            if intent == "find_location":
                location = find_location(self.map_data, data)
                if location:
                    description, events = get_location_details(location)
                    response = f"Found {data} at ({location['x']}, {location['y']}). {description}"
                    if events:
                        response += f" Events: {', '.join(events)}"
                    self.output_area.append(f"Robot: {response}")
                    speak(response)
                else:
                    response = f"Could not find {data}"
                    self.output_area.append(f"Robot: {response}")
                    speak(response)
            elif "go to" in user_input.lower():
                location_name = user_input.lower().replace("go to", "").strip()
                response = self.navigator.move_to(location_name)
                self.output_area.append(f"Robot: {response}")
                self.update_position_label()
                speak(response)
            else:
                response = handle_text_input(user_input)
                self.output_area.append(f"Robot: {response}")
                speak(response)

    def handle_visual_input(self):
        response = capture_and_detect_faces()
        self.output_area.append(f"Robot: {response}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = RobotGui()
    gui.show()
    sys.exit(app.exec_())
