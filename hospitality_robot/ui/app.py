import sys
import os
from flask import Flask, render_template, request, g
import json
import logging

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from robot_core import RobotCore
from navigation.pathfinder import a_star_search, reconstruct_path

# Setup logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Explicitly define the template and static folders relative to this script's location
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

def get_robot():
    """
    Gets the RobotCore instance, creating one if it doesn't exist for the current request.
    """
    if 'robot' not in g:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'main_campus.json')
        app.logger.info(f"Loading robot configuration from: {config_path}")
        g.robot = RobotCore(config_path)
    return g.robot

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        robot = get_robot()
        path = None
        start_location = 'Entrance'
        goal_location = 'Exhibition Hall'

        if request.method == 'POST':
            start_location = request.form['start']
            goal_location = request.form['goal']

            came_from, _ = a_star_search(robot.graph, start_location, goal_location, robot.locations)

            if came_from:
                path = reconstruct_path(came_from, start_location, goal_location)

        return render_template('map.html',
                               locations=robot.locations.keys(),
                               robot_locations=robot.locations,
                               path=path,
                               start=start_location,
                               goal=goal_location,
                               campus_name=robot.campus_name)
    except Exception as e:
        app.logger.error(f"An error occurred in the index route: {e}", exc_info=True)
        return "An internal error occurred. Please check the application log.", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
