import heapq
import math
import random

#heuristic
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#A* give the first and goal state
def a_star(start_pos, goal_pos, get_neighbours_fn, get_cost_fn):
    current = [(0, start_pos)]
    came_from = {}
    g_scores = {start_pos: 0}

    while current:
        curr_f_score, curr_pos = heapq.heappop(current)

        if curr_pos == goal_pos:
            path = []
            while curr_pos in came_from:
                path.append(curr_pos)
                curr_pos = came_from[curr_pos]
            path.append(start_pos)
            path.reverse()
            return path

        for neighbour_pos in get_neighbours_fn(curr_pos):
            tentative_g_score = g_scores[curr_pos] + get_cost_fn(curr_pos, neighbour_pos)
            if neighbour_pos not in g_scores or tentative_g_score < g_scores[neighbour_pos]:
                g_scores[neighbour_pos] = tentative_g_score
                f_score = tentative_g_score + euclidean_distance(goal_pos, neighbour_pos)
                heapq.heappush(current, (f_score, neighbour_pos))
                came_from[neighbour_pos] = curr_pos

    return None

def test_a_star():
    num_nodes = 100
    nodes = [(random.randint(0, num_nodes), random.randint(0, num_nodes)) for _ in range(num_nodes)]
    edges = {node: [] for node in nodes}
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes[i+1:], i+1):
            if random.random() < 0.5:
                edges[node1].append(node2)
                edges[node2].append(node1)
    #returns the neighbouring nodes
    def get_neighbours(node_pos):
        return edges[node_pos]
    #returns the cost of moving from one node to another
    def get_cost(node_pos1, node_pos2):
        return euclidean_distance(node_pos1, node_pos2)

    start_pos = nodes[0]
    goal_pos = nodes[-1]
    path = a_star(start_pos, goal_pos, get_neighbours, get_cost)

    if path:
        print(f"Path from {start_pos} to {goal_pos}: {' -> '.join(str(node_pos) for node_pos in path)}")
    else:
        print(f"No path found from {start_pos} to {goal_pos}")

test_a_star()
