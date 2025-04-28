from flask import Flask, render_template, request, jsonify
from queue import PriorityQueue

app = Flask(__name__)

# Graph data with effort values and image paths
graph = {
    1: {'connections': {2: 2, 3: 1}, 'image': '1.png'},
    2: {'connections': {1: 2}, 'image': '2.png'},
    3: {'connections': {1: 1, 4: 1}, 'image': '3.png'},
    4: {'connections': {3: 1, 14: 15, 5: 3}, 'image': '4.png'},
    5: {'connections': {4: 3, 6: 2}, 'image': '5.png'},
    6: {'connections': {5: 2, 7: 1, 9: 3, 12: 2}, 'image': '6.png'},
    7: {'connections': {6: 1, 10: 1}, 'image': '7.png'},
    8: {'connections': {10: 1, 9: 1, 11: 2}, 'image': '8.png'},
    9: {'connections': {8: 1, 6: 3}, 'image': '9.png'},
    10: {'connections': {11: 1, 8: 1, 7: 1}, 'image': '10.png'},
    11: {'connections': {8: 2, 10: 1, 13: 1, 12: 2}, 'image': '11.png'},
    12: {'connections': {11: 2, 18: 1, 6: 2}, 'image': '12.png'},
    13: {'connections': {11: 1, 18: 1}, 'image': '13.png'},
    14: {'connections': {15: 10, 4: 15}, 'image': '14.png'},
    15: {'connections': {16: 10, 14: 10}, 'image': '15.png'},
    16: {'connections': {17: 3, 15: 10}, 'image': '16.png'},
    17: {'connections': {16: 3, 18: 1}, 'image': '17.png'},
    18: {'connections': {17: 1, 12: 1, 13: 1}, 'image': '18.png'},
}

# A* Algorithm
def a_star_search(start, goal):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            path.insert(0, start)
            return path

        for neighbor, cost in graph[current]['connections'].items():
            tentative = g_score[current] + cost
            if tentative < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                open_set.put((tentative, neighbor))

    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-path', methods=['POST'])
def get_path():
    data = request.json
    start = int(data['start'])
    end = int(data['end'])

    if start < 1 or start > 18 or end < 1 or end > 18:
        return jsonify({'error': '⚠️ Invalid node numbers. No path found'})

    path = a_star_search(start, end)
    images = [graph[node]['image'] for node in path]
    return jsonify({'path': path, 'images': images})

if __name__ == '__main__':
    app.run(debug=True)
