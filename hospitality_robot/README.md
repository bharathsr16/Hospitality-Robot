# Hospitality Robot

This project contains the software for a multifunctional hospitality robot designed for a college campus setting.

## Features

- **Event Location Guidance:** Provides directions to ongoing events.
- **Campus Navigation:** Uses the A* algorithm for pathfinding.
- **Guest Greeting:** Detects guests and provides a voice greeting.
- **Voice Assistant:** Answers frequently asked questions about events.
- **Web UI:** A web-based interface to view the campus map and get directions.

## How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   You may also need to install `ffmpeg` for the audio features:
   ```bash
   sudo apt-get update && sudo apt-get install -y ffmpeg
   ```

2. **Run the Main Application (Command-Line):**
   ```bash
   python3 main.py
   ```

3. **Run the Web UI:**
   ```bash
   python3 ui/app.py
   ```
   The web interface will be available at `http://127.0.0.1:8080`.

## Project Structure

- `database/`: Contains the SQLite database for events and a management script.
- `navigation/`: Implements the pathfinding logic.
- `vision/`: Contains the face detection and greeting functionality.
- `voice/`: Implements the voice assistant for FAQs.
- `ui/`: Contains the Flask web application for the map and directions.
- `main.py`: The main script to run the integrated robot application.
