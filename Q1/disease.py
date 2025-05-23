import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections
import matplotlib
matplotlib.use('TkAgg')


with open('Q1/disease.in', 'r') as file:
    lines = [line.strip() for line in file if line.strip()]

# print("Lines read from file:")
# for line in lines:
#     print(line)

# Step 1: Read n and m
n, m = map(int, lines[0].split())
# print(f"Number of villages (n) = {n}, Number of edges (m) = {m}")

# Step 2: Read the m edges
edges = []
for i in range(1, 1 + m):
    u, v = map(int, lines[i].split())
    edges.append((u, v))
# print(f"Edges read: {edges}")

nodes = set()
for node in range(1, n + 1):
    nodes.add(node)
# print(f"Nodes: {nodes}")

# print(lines[m+1])

# Step 3: Read p and q
p, q = map(int, lines[m+1].split())
# print(f"p = {p}, q = {q}")

# Step 4: Read the mountains
mountain_nodes = list(map(int, lines[2 + m].split()))
# print(f"Mountains: {mountain_nodes}")

# Step 5: Read the initially infected villages
infected_nodes = list(map(int, lines[3 + m].split()))
# print(f"Infected villages: {infected_nodes}")

total_villages = set()
for i in range(1, n + 1):
    if i not in mountain_nodes:
        total_villages.add(i)
# print(f"Total villages excluding mountains: {total_villages}")

# Create graph
G = nx.Graph()
G.add_nodes_from(range(1, n+1))  # Add all villages as nodes
G.add_edges_from(edges)
infected_villages = set(infected_nodes)

# Print all neighbors for each village
# print("Neighbors for each village:")
for village in G.nodes:
    neighbors = list(G.neighbors(village))
    # print(f"Village {village}: {neighbors}")

# print()

        
def infection_bfs(graph, infected_villages, total_villages, mountain_nodes):
    visited = set(infected_villages)
    day_to_villages = collections.defaultdict(list)
    day = 0

    queue = collections.deque(infected_villages)
    # print(f"Initial infected villages: {queue}")
    print()

    # Visualization setup
    pos = nx.spring_layout(graph, seed=42)  # Layout for consistent graph visualization
    fig, ax = plt.subplots(figsize=(8, 6))

    while queue:
        next_queue = collections.deque()
        # Process the current day's infections
        for village in queue:
            for neighbor in sorted(graph[village]):
                if neighbor in mountain_nodes:
                    continue
                if neighbor not in visited and neighbor not in mountain_nodes:
                    visited.add(neighbor)
                    next_queue.append(neighbor)
                    day_to_villages[day].append(neighbor)
    
        # Visualize the current state of the graph
        ax.clear()
        node_colors = []
        for node in graph.nodes:
            if node in mountain_nodes:
                node_colors.append('green')  # Mountains
            elif node in visited:
                node_colors.append('red')  # Infected
            else:
                node_colors.append('blue')  # Healthy villages
    
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='white',
            edge_color='gray',
            ax=ax
        )
        ax.set_title(f"Disease Spread - Day {day+1}")
        plt.pause(2)  # Pause to visualize each step
    
        # If there are no more villages to infect, stop
        if not next_queue:
            break
    
        queue = next_queue  # Move to the next day's infections
        day += 1  # Increment the day only if there are villages left to infect
    uninfected_villages = total_villages.difference(visited)

    ax.text(
        0.0, 0.9,  # Position (relative to the plot)
        f"Days taken to infect all villages: {day}\nUninfected villages: {uninfected_villages}",
        transform=ax.transAxes,  # Use axes coordinates
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
    )


    plt.title(f"Disease Spread Complete - Day {day}")
    plt.show()

    return day, uninfected_villages

# min_days, uninfected_villages = infection_bfs(G, infected_nodes[0], days, total_villages, infected_villages, mountain_nodes)
min_days, uninfected_villages = infection_bfs(G, infected_villages, total_villages, mountain_nodes)

print(f"Days taken to infect all villages: {min_days}")
print(f"Uninfected villages: {uninfected_villages}")