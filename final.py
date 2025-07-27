import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from sklearn.cluster import SpectralClustering
from scipy.spatial import ConvexHull
from opendssdirect import dss
import os

st.set_page_config(page_title="IEEE 123 Bus Dashboard", layout="wide")
st.title(" IEEE 123 Bus Fault Visualization Dashboard")

folder_path = r"C:\\IEEE123Bus"
dss_path = os.path.join(folder_path, "IEEE123Master.dss")
coords_path = os.path.join(folder_path, "BusCoords.dat")

if not os.path.exists(dss_path) or not os.path.exists(coords_path):
    st.error(" Required files not found in C:\\IEEE123Bus.")
    st.stop()

@st.cache_resource
def load_data():
    dss.Basic.ClearAll()
    dss.Text.Command(f'Redirect "{dss_path}"')
    dss.Text.Command("Solve")

    coords = pd.read_csv(coords_path, sep=r"[,\s]+", names=["Bus", "X", "Y"], index_col="Bus", engine="python")
    bus_map, edges, idx = {}, [], 0

    ptr = dss.Lines.First()
    while ptr:
        b1, b2 = dss.Lines.Bus1().split('.')[0], dss.Lines.Bus2().split('.')[0]
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

    labels = SpectralClustering(n_clusters=7, affinity="precomputed", random_state=42).fit_predict(W)

    pos = {}
    for bus, i in bus_map.items():
        if bus in coords.index:
            pos[i] = (coords.at[bus, "X"], coords.at[bus, "Y"])

    
    if len(pos) < len(bus_map):
        G = nx.Graph()
        G.add_edges_from([(u, v) for u, v, _ in edges])
        fallback = nx.spring_layout(G, seed=42)
        for i in range(n):
            if i not in pos:
                pos[i] = fallback[i]

    return bus_map, edges, labels, pos

bus_map, edges, labels, pos = load_data()
n = len(bus_map)
k = 7
fault_zones = {4, 5, 6}
zone_colors = {
    0: "#1f77b4", 1: "#ff7f0e", 2: "#2ca02c",
    3: "#9467bd", 4: "#7f0000", 5: "#7f0000", 6: "#7f0000"
}


zone_data = []
for z in range(k):
    nodes = [i for i in range(n) if labels[i] == z]
    faults = len(nodes) if z in fault_zones else 0
    zone_data.append({
        "Zone": f"Zone {z+1}",
        "Total Nodes": len(nodes),
        "Fault Nodes": faults,
        "Fault %": round((faults / len(nodes)) * 100 if nodes else 0, 2)
    })
df = pd.DataFrame(zone_data)


fault_zones_detected = df[df["Fault Nodes"] > 0]["Zone"].tolist()
if fault_zones_detected:
    st.markdown(f"""<div style="background-color:#ffe6e6;padding:10px;border-left:6px solid red;">
        ⚠️ <strong>Faults detected in:</strong> {', '.join(fault_zones_detected)}</div>""",
        unsafe_allow_html=True)


tabs = st.tabs([f"Zone {i+1}" for i in range(k)])
for i, tab in enumerate(tabs):
    with tab:
        zone_name = f"Zone {i+1}"
        data = df.iloc[i]

        
        pie_data = pd.DataFrame({
            "Status": ["Fault", "Healthy"],
            "Count": [data["Fault Nodes"], data["Total Nodes"] - data["Fault Nodes"]]
        })
        fig_pie = px.pie(pie_data, names="Status", values="Count",
                         color="Status", title="Fault vs Healthy",
                         color_discrete_map={"Fault": "red", "Healthy": "green"})

        
        fig_bar = px.bar(data_frame=data.drop("Zone").to_frame().T.melt(),
                         x="variable", y="value", color="variable",
                         title="Zone Metrics", color_discrete_sequence=["red", "green", "orange"])

        
        x_vals, y_vals, zones = [], [], []
        for idx in range(n):
            x, y = pos[idx]
            x_vals.append(x)
            y_vals.append(y)
            zones.append(f"Zone {labels[idx]+1}")

        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(color=[zone_colors[l] for l in labels], size=[12 if labels[j] == i else 5 for j in range(n)]),
            text=zones, hoverinfo="text"
        ))

        
        cluster_pts = np.array([pos[j] for j in range(n) if labels[j] == i])
        if len(cluster_pts) >= 3:
            hull = ConvexHull(cluster_pts)
            hull_pts = cluster_pts[hull.vertices]
            center = hull_pts.mean(axis=0)
            inflated = center + 1.15 * (hull_pts - center)
            inflated = np.append(inflated, [inflated[0]], axis=0)
            fig_net.add_trace(go.Scatter(
                x=inflated[:, 0], y=inflated[:, 1], fill='toself',
                fillcolor=zone_colors[i], opacity=0.3, line=dict(color="black"),
                mode='lines', showlegend=False
            ))

        fig_net.update_layout(title="IEEE 123 Bus Visualization", showlegend=False, height=500, margin=dict(l=0, r=0, t=30, b=0))

        
        st.markdown(f"###  {zone_name} Overview")
        col1, col2, col3 = st.columns([1.1, 1, 1.5])
        col1.plotly_chart(fig_pie, use_container_width=True)
        col2.plotly_chart(fig_bar, use_container_width=True)
        col3.plotly_chart(fig_net, use_container_width=True)


st.markdown("---")
st.subheader(" Zone-wise Summary")
summary_chart = px.bar(df, x="Zone", y=["Fault Nodes", "Total Nodes", "Fault %"],
                       barmode="group", title="Zone-wise Fault Overview",
                       color_discrete_sequence=["red", "green", "orange"])
st.plotly_chart(summary_chart, use_container_width=True)


 