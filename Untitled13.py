import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering
from scipy.spatial import ConvexHull
from opendssdirect import dss

# Load DSS and solve
dss.Command('ClearAll')
dss.Command(r'Redirect "D:\GridGuard\Codes\IEEE123Bus\IEEE123Master.dss"')
dss.Command('Solve')

# Read bus coordinates
coords = pd.read_csv(
    r"D:\GridGuard\Codes\IEEE123Bus\BusCoords.dat",
    sep=r"[,\s]+", names=["Bus", "X", "Y"], index_col="Bus", engine="python"
)

# Build graph and weights
bus_map, edges, idx = {}, [], 0
ptr = dss.Lines.First()
while ptr:
    b1 = dss.Lines.Bus1().split('.')[0]
    b2 = dss.Lines.Bus2().split('.')[0]
    for b in (b1, b2):
        if b not in bus_map:
            bus_map[b] = idx
            idx += 1
    r = dss.Lines.R1()
    if r > 0:
        edges.append((bus_map[b1], bus_map[b2], 1.0 / r))
    ptr = dss.Lines.Next()

n = len(bus_map)
W = np.zeros((n, n))
for u, v, w in edges:
    W[u, v] = W[v, u] = w

# Perform spectral clustering
k = 7
original_labels = SpectralClustering(n_clusters=k, affinity="precomputed", random_state=42).fit_predict(W)

# Remap cluster IDs to match visual zones
label_remap = {
    0: 3, 1: 2, 2: 1, 3: 5, 4: 4, 5: 6, 6: 0  # computed -> Zone ID (0-based)
}
labels = np.vectorize(label_remap.get)(original_labels)

# Positioning
pos = {}
for bus, i in bus_map.items():
    if bus in coords.index:
        pos[i] = (coords.at[bus, "X"], coords.at[bus, "Y"])
missing = [i for i in range(n) if i not in pos]
if missing:
    tmpG = nx.Graph()
    tmpG.add_edges_from([(u, v) for u, v, _ in edges])
    fallback = nx.spring_layout(tmpG, seed=42)
    for i in missing:
        pos[i] = fallback[i]

# Define fault zones (Zone 5, 6, 7) and colors
fault_zones = {4, 5, 6}
zone_colors = {
    0: "#1f77b4",  # Zone 1
    1: "#ff7f0e",  # Zone 2
    2: "#2ca02c",  # Zone 3
    3: "#9467bd",  # Zone 4
    4: "#7f0000",  # Zone 5 (fault)
    5: "#7f0000",  # Zone 6 (fault)
    6: "#7f0000",  # Zone 7 (fault)
}

# Draw graph
G = nx.Graph()
G.add_nodes_from(range(n))
G.add_weighted_edges_from(edges)

plt.figure(figsize=(12, 9))
nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color="#bbb")

for z in range(k):
    nodes_in_zone = [i for i in range(n) if labels[i] == z]
    color = zone_colors[z]
    size = 130 if z in fault_zones else 35
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_in_zone,
                           node_color=color, node_size=size,
                           edgecolors='black', linewidths=0.5)

# Highlight fault zones
for z in fault_zones:
    pts = np.array([pos[i] for i in range(n) if labels[i] == z])
    if len(pts) >= 3:
        hull = ConvexHull(pts)
        center = pts[hull.vertices].mean(axis=0)
        inflated = center + 1.15 * (pts[hull.vertices] - center)
        plt.fill(*inflated.T, color=zone_colors[z], alpha=0.4)

# Light fill for others
for z in range(k):
    if z in fault_zones:
        continue
    pts = np.array([pos[i] for i in range(n) if labels[i] == z])
    if len(pts) >= 3:
        hull = ConvexHull(pts)
        plt.fill(*pts[hull.vertices].T, color=zone_colors[z], alpha=0.1)

# Zone labels
for z in range(k):
    pts = np.array([pos[i] for i in range(n) if labels[i] == z])
    if len(pts):
        cx, cy = pts.mean(axis=0)
        plt.text(cx, cy, f"Zone {z+1}", fontsize=12, ha="center", va="center",
                 bbox=dict(facecolor="white", edgecolor="black", alpha=0.7))

plt.title("IEEE‑123 Feeder — Zones Matched to Reference Image (Fault Zones 5, 6, 7)", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()
