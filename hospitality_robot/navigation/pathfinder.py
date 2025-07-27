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
    # A simple heuristic for A* (Manhattan distance, assuming a grid)
    # In a real scenario, this would be based on actual coordinates.
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

        if current == goal:
            break

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

if __name__ == '__main__':
    # Create a sample campus map
    campus_map = Graph()
    campus_map.add_node('Entrance')
    campus_map.add_node('Auditorium')
    campus_map.add_node('Block A')
    campus_map.add_node('Block B')
    campus_map.add_node('Exhibition Hall')
    campus_map.add_node('Open Air Theatre')

    campus_map.add_edge('Entrance', 'Block A', 10)
    campus_map.add_edge('Block A', 'Auditorium', 5)
    campus_map.add_edge('Block A', 'Block B', 15)
    campus_map.add_edge('Block B', 'Exhibition Hall', 5)
    campus_map.add_edge('Block B', 'Open Air Theatre', 20)
    campus_map.add_edge('Auditorium', 'Exhibition Hall', 10)

    # Add dummy coordinates for the heuristic
    locations = {
        'Entrance': (0, 0),
        'Auditorium': (10, 10),
        'Block A': (5, 5),
        'Block B': (20, 5),
        'Exhibition Hall': (15, 15),
        'Open Air Theatre': (25, 0)
    }

    start_location = 'Entrance'
    goal_location = 'Exhibition Hall'

    came_from, cost_so_far = a_star_search(campus_map, start_location, goal_location, locations)
    path = reconstruct_path(came_from, start_location, goal_location)

    print(f"Path from {start_location} to {goal_location}:")
    print(" -> ".join(path))
    print(f"Total cost: {cost_so_far[goal_location]}")
