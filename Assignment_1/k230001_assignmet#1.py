from collections import deque
import heapq

# Define the graph data
ROMANIA_GRAPH = {
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Arad": {"Zerind": 75, "Timisoara": 118, "Sibiu": 140},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Sibiu": {"Oradea": 151, "Arad": 140, "Rimnicu Vilcea": 80, "Fagaras": 99},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Vaslui": 142, "Hirsova": 98},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86}
}

# Define heuristic values (straight-line distances to Bucharest)
ROMANIA_HEURISTIC = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

class GraphSearch:
    def __init__(self, graph, heuristic=None):
        self.graph = graph
        self.heuristic = heuristic or {}

    def reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def bfs(self, start, goal):
        queue = deque([(start, 0)])
        visited = {start}
        came_from = {start: None}
        
        while queue:
            current, cost = queue.popleft()
            
            if current == goal:
                return self.reconstruct_path(came_from, current), cost
            
            for neighbor, edge_cost in self.graph[current].items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append((neighbor, cost + edge_cost))
        
        return None, float('inf')

    def dfs(self, start, goal):
        stack = [(start, [start], 0)]
        visited = {start}
        
        while stack:
            current, path, cost = stack.pop()
            
            if current == goal:
                return path, cost
            
            for neighbor, edge_cost in self.graph[current].items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor], cost + edge_cost))
        
        return None, float('inf')

    def ucs(self, start, goal):
        frontier = [(0, start)]
        visited = set()
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            current_cost, current = heapq.heappop(frontier)
            
            if current == goal:
                return self.reconstruct_path(came_from, current), current_cost
            
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor, edge_cost in self.graph[current].items():
                new_cost = current_cost + edge_cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(frontier, (new_cost, neighbor))
        
        return None, float('inf')

    def greedy_bfs(self, start, goal):
        if not self.heuristic:
            raise ValueError("Heuristic values required for Greedy Best-First Search")
            
        frontier = [(self.heuristic[start], start, 0)]
        visited = set()
        came_from = {start: None}
        
        while frontier:
            _, current, cost = heapq.heappop(frontier)
            
            if current == goal:
                return self.reconstruct_path(came_from, current), cost
            
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor, edge_cost in self.graph[current].items():
                if neighbor not in visited:
                    came_from[neighbor] = current
                    heapq.heappush(frontier, (self.heuristic[neighbor], neighbor, cost + edge_cost))
        
        return None, float('inf')

def compare_search_algorithms(graph_data, heuristic_data, start, goal):
    searcher = GraphSearch(graph_data, heuristic_data)
    results = {
        "BFS": searcher.bfs(start, goal),
        "DFS": searcher.dfs(start, goal),
        "UCS": searcher.ucs(start, goal),
        "Greedy BFS": searcher.greedy_bfs(start, goal)
    }
    
    return dict(sorted(results.items(), key=lambda x: x[1][1]))

if __name__ == "__main__":
    results = compare_search_algorithms(ROMANIA_GRAPH, ROMANIA_HEURISTIC, "Oradea", "Bucharest")
    print("Paths in Ascending Order of Cost:")
    for algorithm, (path, cost) in results.items():
        print(f"{algorithm}: (Path: {path}, Cost: {cost})")