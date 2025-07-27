import os
import sys
import tempfile
from gtts import gTTS
from playsound import playsound

# --- Add hospitality_robot to Python Path ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'hospitality_robot'))

# --- Copied and corrected code from all modules ---

# from database.event_manager
import sqlite3

def get_event_details(event_name):
    db_path = os.path.join('hospitality_robot', 'database', 'events.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM events WHERE name LIKE ?", ('%' + event_name + '%',))
    event = c.fetchone()
    conn.close()
    return event

# from navigation.pathfinder
import heapq

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

def heuristic(a, b):
    (x1, y1) = b
    (x2, y2) = a
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal, locations):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]
        if current == goal: break
        for next_node in graph.edges[current]:
            new_cost = cost_so_far[current] + graph.distances[(current, next_node)]
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(locations[goal], locations[next_node])
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# from vision.face_detector (corrected)
def greet_guest():
    greeting_text = "Hello! Welcome to the event. How can I help you?"
    print(greeting_text)
    tts = gTTS(text=greeting_text, lang='en')
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
            tts.save(fp.name)
            playsound(fp.name)
    except Exception as e:
        print(f"Error playing sound: {e}")

# from main (integrated)
def setup_campus_map():
    campus_map = Graph()
    locations = {
        'Entrance': (0, 0), 'Auditorium': (10, 10), 'Block A': (5, 5),
        'Block B': (20, 5), 'Exhibition Hall': (15, 15), 'Open Air Theatre': (25, 0)
    }
    for loc in locations: campus_map.add_node(loc)
    campus_map.add_edge('Entrance', 'Block A', 10)
    campus_map.add_edge('Block A', 'Auditorium', 5)
    campus_map.add_edge('Block A', 'Block B', 15)
    campus_map.add_edge('Block B', 'Exhibition Hall', 5)
    campus_map.add_edge('Block B', 'Open Air Theatre', 20)
    campus_map.add_edge('Auditorium', 'Exhibition Hall', 10)
    return campus_map, locations

def main_windows():
    print("Hospitality Robot Activated (Windows Version).")
    campus_map, locations = setup_campus_map()
    print("Guest detected.")
    greet_guest()
    command = "where is the tech talk"
    print(f"\nSimulated command: '{command}'")
    if "where is the" in command:
        event_name = command.split("where is the")[-1].strip()
        event = get_event_details(event_name)
        if event:
            destination = event[2]
            start_location = 'Entrance'
            if destination in locations:
                came_from, cost_so_far = a_star_search(campus_map, start_location, destination, locations)
                path = reconstruct_path(came_from, start_location, destination)
                directions = " -> ".join(path)
                response = f"To get to the {event[1]}, you can follow this path: {directions}"
                print(response)
            else:
                print(f"I know about the {event_name}, but I don't have its location on my map.")
        else:
            print(f"Sorry, I couldn't find any event named {event_name}.")

if __name__ == '__main__':
    main_windows()
