import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from haversine import haversine
import ast
# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('noaa_satellite_data.csv')

# Select a specific timestamp (row)
selected_timestamp = "2023-10-10 21:13:41.946527"
selected_row = df[df['Time'] == selected_timestamp]

# Create an empty NetworkX graph
G = nx.Graph()

# Add nodes for each satellite
satellite_columns = selected_row.columns[1:]  # Exclude the timestamp column
for satellite in satellite_columns:
    G.add_node(satellite)

# Calculate distances and add edges for the selected row
for i in range(len(satellite_columns)):
    for j in range(i + 1, len(satellite_columns)):
        satellite1 = satellite_columns[i]
        satellite2 = satellite_columns[j]
        # Extract the latitude and longitude for both satellites and parse them
        coord1 = ast.literal_eval(selected_row[satellite1].values[0])
        coord2 = ast.literal_eval(selected_row[satellite2].values[0])
        lat1, lon1 = coord1['Latitude'], coord1['Longitude']
        lat2, lon2 = coord2['Latitude'], coord2['Longitude']
        # Calculate the distance using the haversine formula
        distance = haversine((lat1, lon1), (lat2, lon2))
        G.add_edge(satellite1, satellite2, weight=distance)

# Create a layout for the nodes
layout = nx.spring_layout(G)

# Draw the nodes and labels
nx.draw(G, layout, with_labels=True, node_size=300, node_color='lightblue', font_size=10)

# # Draw the edges with labels
# edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges}
# nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels, font_size=8)

# Display the graph
plt.title(f"Satellite Network Graph for Timestamp: {selected_timestamp}")
plt.show()
