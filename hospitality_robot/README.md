# Hospitality Robot

This project contains the software for a dynamic, configurable hospitality robot designed for a college campus setting. The robot's knowledge (maps, events, etc.) is loaded from JSON configuration files, making it adaptable to different locations and events.

## Features

- **Dynamic Configuration:** Load different campus maps, events, and settings from `.json` files in the `configs` directory.
- **Interactive CLI:** A user-friendly command-line interface to interact with the robot, ask for directions, and get event information.
- **Web UI with Interactive Map:** A web-based interface that displays a map image with clickable locations, loaded from the configuration.
- **Smarter Assistant Logic:** The robot can answer a variety of questions, such as "Where is...?", "Tell me about...", and "What's happening now?".
- **Pathfinding:** Uses the A* algorithm to find the shortest path between two locations on the map.

## How to Run

### 1. Install Dependencies
First, ensure you have Python installed. Then, install the required packages using pip:
```bash
pip install -r requirements.txt
```
For audio features on Linux, you may also need to install `ffmpeg`:
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

### 2. Run the Interactive Command-Line Interface (Recommended)
This is the main way to interact with the robot's logic.
```bash
python3 hospitality_robot/interactive_robot.py
```
The script will prompt you to choose a configuration file from the `configs` directory and then present a menu of options.

### 3. Run the Web UI
This will start a web server to display the interactive map.
```bash
python3 hospitality_robot/ui/app.py
```
Open your web browser and navigate to `http://127.0.0.1:8080` to see the map.

## Customizing the Robot

To create a new map or event configuration:
1.  Add a new background map image to `hospitality_robot/ui/static/images/`.
2.  Create a new `.json` file in the `hospitality_robot/configs/` directory.
3.  Copy the structure from `main_campus.json` and edit the `name`, `map_image`, `locations` (with their x/y coordinates for the UI), `graph` edges, and `events`.
4.  Run the `interactive_robot.py` or `ui/app.py` script, and your new configuration will be available to load.

## Project Structure

- `configs/`: Contains JSON files for different campus/event configurations.
- `database/`: Contains the SQLite database (legacy, now replaced by JSON configs).
- `navigation/`: Implements the A* pathfinding algorithm.
- `robot_core.py`: The central "brain" that loads and manages configurations.
- `interactive_robot.py`: The main entry point for the interactive CLI.
- `ui/`: Contains the Flask web application for the interactive map.
  - `static/`: For images and other static assets.
  - `templates/`: For HTML templates.
- `main.py`: The original, now legacy, main script.
