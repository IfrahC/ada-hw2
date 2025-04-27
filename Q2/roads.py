import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Define the graph as adjacency dictionary
city_graph = {
    'Islamabad': {'Lahore': 375, 'Quetta': 913, 'Karachi': 1409, 'Peshawar': 155, 'Multan': 542, 'Muzaffarabad': 332, 'Gilgit': 493, 'Gwadar': 2065, 'Rawalpindi': 15, 'Faisalabad': 320},
    'Lahore': {'Islamabad': 375, 'Quetta': 831, 'Karachi': 1221, 'Peshawar': 505, 'Multan': 348, 'Rawalpindi': 360, 'Faisalabad': 180},
    'Quetta': {'Islamabad': 913, 'Lahore': 831, 'Karachi': 685, 'Peshawar': 1000, 'Multan': 687, 'Rawalpindi': 911, 'Faisalabad': 750},
    'Karachi': {'Islamabad': 1409, 'Lahore': 1221, 'Quetta': 685, 'Peshawar': 1470, 'Multan': 1020, 'Gwadar': 623, 'Rawalpindi': 1400, 'Faisalabad': 1210, 'Nawabshah': 270, 'Hyderabad': 165},
    'Peshawar': {'Islamabad': 155, 'Lahore': 505, 'Quetta': 1000, 'Karachi': 1470, 'Multan': 690, 'Rawalpindi': 160, 'Faisalabad': 460},
    'Multan': {'Islamabad': 542, 'Lahore': 348, 'Quetta': 687, 'Karachi': 1020, 'Peshawar': 690, 'Rawalpindi': 540, 'Faisalabad': 180},
    'Muzaffarabad': {'Islamabad': 332, 'Rawalpindi': 340},
    'Gilgit': {'Islamabad': 493, 'Rawalpindi': 500},
    'Gwadar': {'Islamabad': 2065, 'Lahore': 1900, 'Quetta': 912, 'Karachi': 623, 'Peshawar': 2100, 'Multan': 1645, 'Rawalpindi': 2050, 'Faisalabad': 1830, 'Nawabshah': 620, 'Hyderabad': 520},
    'Rawalpindi': {'Islamabad': 15, 'Lahore': 360, 'Quetta': 911, 'Karachi': 1400, 'Peshawar': 160, 'Multan': 540, 'Muzaffarabad': 340, 'Gilgit': 500, 'Gwadar': 2050, 'Faisalabad': 310},
    'Faisalabad': {'Islamabad': 320, 'Lahore': 180, 'Quetta': 750, 'Karachi': 1210, 'Peshawar': 460, 'Multan': 180, 'Rawalpindi': 310},
    'Nawabshah': {'Karachi': 270, 'Gwadar': 620, 'Hyderabad': 90},
    'Hyderabad': {'Karachi': 165, 'Gwadar': 520, 'Nawabshah': 90}
}

# Create graph
G = nx.Graph()
for city, connections in city_graph.items():
    for neighbor, distance in connections.items():
        G.add_edge(city, neighbor, weight=distance)

# Visualization function
def draw_graph():
    pos = nx.spring_layout(G, seed=42, k=1.5)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    plt.title('City Graph Visualization')
    plt.show()

# Floyd-Warshall Algorithm
shortest_paths = dict(nx.floyd_warshall(G, weight='weight'))

# Instead of printing everything, ask user for source and destination
def show_shortest_paths():
    input_window = tk.Toplevel()
    input_window.title("Find Shortest Distance")

    tk.Label(input_window, text="Select Source City:").pack(pady=5)
    source_var = tk.StringVar()
    source_menu = ttk.Combobox(input_window, textvariable=source_var, values=list(city_graph.keys()), state="readonly")
    source_menu.pack(pady=5)

    tk.Label(input_window, text="Select Destination City:").pack(pady=5)
    dest_var = tk.StringVar()
    dest_menu = ttk.Combobox(input_window, textvariable=dest_var, values=list(city_graph.keys()), state="readonly")
    dest_menu.pack(pady=5)

    result_label = tk.Label(input_window, text="", font=("Arial", 12))
    result_label.pack(pady=10)

    def calculate_shortest_distance():
        src = source_var.get()
        dest = dest_var.get()
        if src and dest:
            if src == dest:
                result_label.config(text="Source and Destination are the same!")
            else:
                distance = int(shortest_paths[src][dest])
                result_label.config(text=f"Shortest distance from {src} to {dest}: {distance} km")

    find_button = ttk.Button(input_window, text="Find Shortest Distance", command=calculate_shortest_distance)
    find_button.pack(pady=10)


# Visualize the shortest-path graph
def draw_shortest_path_graph():
    G_shortest = nx.Graph()
    for src in shortest_paths:
        for dest in shortest_paths[src]:
            if src != dest:
                G_shortest.add_edge(src, dest, weight=int(shortest_paths[src][dest]))

    pos = nx.spring_layout(G_shortest, seed=42, k=1.5)
    labels = nx.get_edge_attributes(G_shortest, 'weight')
    nx.draw(G_shortest, pos, with_labels=True, node_color='lightgreen', node_size=1000, font_size=8, edge_color='gray')
    nx.draw_networkx_edge_labels(G_shortest, pos, edge_labels=labels, font_size=6)
    plt.title('City Graph - Shortest Paths (Floyd-Warshall)')
    plt.show()

# Tkinter app
def main():
    root = tk.Tk()
    root.title("City Graph Viewer")

    label = tk.Label(root, text="City Graph Visualization", font=("Arial", 14))
    label.pack(pady=10)

    graph_button = ttk.Button(root, text="Visualize Original Graph", command=draw_graph)
    graph_button.pack(pady=5)

    floyd_button = ttk.Button(root, text="Show All-Pairs Shortest Paths", command=show_shortest_paths)
    floyd_button.pack(pady=5)

    floyd_graph_button = ttk.Button(root, text="Visualize Shortest Path Graph", command=draw_shortest_path_graph)
    floyd_graph_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
