# bucket_mst_visualization.py

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.patches as patches
import time

# Build your sample weighted graph
G = nx.Graph()

# Add weighted edges
G.add_edge('a', 'b', weight=4)
G.add_edge('a', 'c', weight=2)
G.add_edge('b', 'c', weight=1)
G.add_edge('b', 'd', weight=5)
G.add_edge('c', 'd', weight=8)
G.add_edge('c', 'e', weight=10)
G.add_edge('d', 'e', weight=2)

# Layout for drawing
pos = nx.spring_layout(G, seed=42)  # consistent layout

def draw_with_bucket(G, T, bucket, step):
    plt.figure(figsize=(8, 6))
    
    # Draw full graph lightly
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color='lightgray', node_size=500)
    
    # Draw the bucket bubble
    bucket_pos = np.array([pos[node] for node in bucket])
    if len(bucket) >= 3:  # Convex Hull needs at least 3 points
        hull = ConvexHull(bucket_pos)
        vertices = bucket_pos[hull.vertices]
        polygon = patches.Polygon(vertices, closed=True, fill=True, color='violet', alpha=0.3)
        plt.gca().add_patch(polygon)
    else:
        # 1 or 2 points - draw small circles
        for p in bucket_pos:
            circle = plt.Circle(p, radius=0.08, color='violet', alpha=0.3)
            plt.gca().add_patch(circle)

    # Highlight bucket nodes
    nx.draw_networkx_nodes(G, pos, nodelist=bucket, node_color='violet', node_size=600)
    
    # Highlight tree edges
    nx.draw_networkx_edges(T, pos, edge_color='orange', width=3)
    
    # Draw labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.title(f"Step {step}")
    plt.axis('off')
    plt.show()

# Initialize
bucket = set()
T = nx.Graph()

# Start from a node (e.g., 'a')
start_node = 'a'
bucket.add(start_node)

# Visualization - step 0
draw_with_bucket(G, T, bucket, step=0)

step = 1

# Algorithm C - Minimum Spanning Tree
while True:
    min_edge = None
    min_weight = float('inf')

    for u in bucket:
        for v in G.neighbors(u):
            if v not in bucket:
                w = G[u][v]['weight']
                if w < min_weight:
                    min_weight = w
                    min_edge = (u, v, w)

    if min_edge is None:
        break  # No more edges to expand

    u, v, w = min_edge
    bucket.add(v)
    T.add_edge(u, v, weight=w)

    draw_with_bucket(G, T, bucket, step)
    step += 1

print("Finished! Minimum Spanning Tree edges:")
print(list(T.edges(data=True)))
