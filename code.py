
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py
            return True
        return False

def kruskal_mst(edges, n):
    # Sort edges based on weight (index 2 of the tuple)
    edges.sort(key=lambda x: x[2])
    uf = UnionFind(n)
    mst = []
    
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            
    return mst

# Driver Code
edges_list = [(0, 1, 2), (0, 2, 3), (1, 2, 1), (1, 3, 4), (2, 3, 2), (2, 4, 5), (3, 4, 3)]
mst = kruskal_mst(edges_list, 5)

# Calculate total cost
total = sum(w for _, _, w in mst)

print("Kruskal's Mst:", mst)
print("Total cost:", total)








import heapq
from collections import defaultdict

def dijkstra(graph, start):
    # Using defaultdict to initialize distances to infinity
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    pq = [(0, start)]
    prev = {}

    while pq:
        du, u = heapq.heappop(pq) # Corrected from headpq

        if du > dist[u]:
            continue

        for v, w in graph[u].items():
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v)) # Corrected from headpq-headpush

    return dist, prev

# Graph dictionary strictly based on your notebook's drawing
Graph = {
    0: {1: 2, 2: 3},
    1: {0: 2, 2: 1, 4: 5},
    2: {0: 3, 1: 1, 3: 2, 4: 4},
    3: {2: 2, 4: 3},
    4: {1: 5, 2: 4, 3: 3}
}

dist, prev = dijkstra(Graph, 0)

print("Distances from source 0:")
for node in sorted(dist):
    print(f"Node {node} : {dist[node]}")









import math

def floyd_warshall(graph):
    n = len(graph)
    # Initialize matrix with infinity
    dist = [[math.inf] * n for _ in range(n)]

    # Setup initial distances based on the graph
    for i in range(n):
        dist[i][i] = 0
        for j in range(n):
            if graph[i][j] != -1:  # Your notebook uses -1 for "no edge"
                dist[i][j] = graph[i][j]

    # Core Floyd-Warshall DP Logic
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# Input Graph Matrix (-1 means no direct edge)
graph = [
    [0, 5, -1, 6, -1],
    [-1, 0, 1, -1, 7],
    [3, -1, 0, 4, -1],
    [-1, -1, 2, 0, 3],
    [2, -1, -1, 5, 0]
]

result = floyd_warshall(graph)

print("Shortest Path Matrix:")
for row in result:
    # Fixed the math.int mistake here
    print([int(x) if x != math.inf else "INF" for x in row])







# Maximal Clique Problem

def is_clique(vertices, adj):
    m = len(vertices)
    for i in range(m):
        # We only need to check pairs once, so j starts from i + 1
        for j in range(i + 1, m):
            u, v = vertices[i], vertices[j]
            if adj[u][v] == 0:
                return False
    return True

def max_clique_backtrack(n, adj, vertices, i, max_clique):
    # Check if current clique is larger than the maximum found so far
    if len(vertices) > len(max_clique[0]):
        max_clique[0] = vertices[:]
        
    for j in range(i + 1, n + 1):
        vertices.append(j)
        
        # Only backtrack further if it's still a clique
        if is_clique(vertices, adj):
            max_clique_backtrack(n, adj, vertices, j, max_clique)
            
        vertices.pop()

def find_maximum_clique(n, edges):
    # Create an adjacency matrix of size (n+1) x (n+1) initialized to 0
    adj = [[0] * (n + 1) for _ in range(n + 1)]
    
    for u, v in edges:
        adj[u][v] = 1
        adj[v][u] = 1 # Fixed your adj[w][u] typo here
        
    vertices = []
    max_clique = [[]] # Using a list of list to pass by reference
    
    max_clique_backtrack(n, adj, vertices, 0, max_clique)
    
    return max_clique[0]

if __name__ == "__main__":
    n = 5
    edges = [
        [1, 2],
        [2, 3],
        [3, 1],
        [3, 4],
        [4, 5],
        [5, 3]
    ]
    
    maximum = find_maximum_clique(n, edges)
    print(f"maximum clique is {maximum}")









# N-Queens Problem using Backtracking

def print_board(board, N):
    for row in board:
        # Puts 'Q' for Queen and '.' for empty space for better visibility
        print(" ".join("Q" if x == 1 else "." for x in row))
    print()

def is_safe(board, row, col, N):
    # 1. Check this row on left side
    for i in range(col):
        if board[row][i] == 1:
            return False
            
    # 2. Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
            
    # 3. Check lower diagonal on left side
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
            
    return True

def solve_nq_util(board, col, N, solutions):
    # Base case: If all queens are placed, we found a solution
    if col >= N:
        # Save a copy of the current board configuration
        solutions.append([row[:] for row in board])
        return True
        
    res = False
    for i in range(N):
        if is_safe(board, i, col, N):
            # Place this queen in board[i][col]
            board[i][col] = 1
            
            # Recur to place rest of the queens
            solve_nq_util(board, col + 1, N, solutions)
            
            # Backtrack: Remove queen from board[i][col] to try other rows
            board[i][col] = 0
            
    return res

def solve_n_queens(N):
    # Initialize an N x N board with 0s
    board = [[0 for _ in range(N)] for _ in range(N)]
    solutions = []
    
    solve_nq_util(board, 0, N, solutions)
    
    print(f"Total solutions found for {N}-Queens: {len(solutions)}")
    if solutions:
        print(f"Showing the first valid arrangement for {N}x{N}:")
        print_board(solutions[0], N)

if __name__ == "__main__":
    print("=== 4-Queens Problem ===")
    solve_n_queens(4)
    
    print("\n=== 8-Queens Problem ===")
    solve_n_queens(8)
