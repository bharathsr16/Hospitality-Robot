import sys
import os
from flask import Flask, render_template, request

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from navigation.pathfinder import Graph, a_star_search, reconstruct_path

app = Flask(__name__, template_folder='templates')

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

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        campus_map, locations = setup_campus_map()
        path = None
        start_location = 'Entrance'
        goal_location = 'Exhibition Hall'

        if request.method == 'POST':
            start_location = request.form['start']
            goal_location = request.form['goal']
            came_from, _ = a_star_search(campus_map, start_location, goal_location, locations)
            path = reconstruct_path(came_from, start_location, goal_location)

        return render_template('index.html', locations=locations.keys(), path=path, start=start_location, goal=goal_location)
    except Exception as e:
        return str(e)

def create_template_file():
    if not os.path.exists('hospitality_robot/ui/templates'):
        os.makedirs('hospitality_robot/ui/templates')

    with open('hospitality_robot/ui/templates/index.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Campus Map</title>
        </head>
        <body>
            <h1>Campus Map</h1>
            <form method="post">
                <label for="start">Start:</label>
                <select name="start" id="start">
                    {% for location in locations %}
                        <option value="{{ location }}" {% if location == start %}selected{% endif %}>{{ location }}</option>
                    {% endfor %}
                </select>
                <label for="goal">Goal:</label>
                <select name="goal" id="goal">
                    {% for location in locations %}
                        <option value="{{ location }}" {% if location == goal %}selected{% endif %}>{{ location }}</option>
                    {% endfor %}
                </select>
                <button type="submit">Find Path</button>
            </form>
            {% if path %}
                <h2>Path:</h2>
                <p>{{ " -> ".join(path) }}</p>
            {% endif %}
        </body>
        </html>
        """)

if __name__ == '__main__':
    create_template_file()
    app.run(host='0.0.0.0', port=8080)
