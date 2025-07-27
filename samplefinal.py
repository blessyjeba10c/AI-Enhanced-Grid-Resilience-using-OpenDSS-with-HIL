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
import time
import random
from datetime import datetime

st.set_page_config(page_title="IEEE 123 Bus Dashboard", layout="wide")
st.title("IEEE 123 Bus Fault Visualization Dashboard")

folder_path = r"D:\GridGuard\Codes\IEEE123Bus"  
dss_path = os.path.join(folder_path, "IEEE123Master.dss")
coords_path = os.path.join(folder_path, "BusCoords.dat")

if not os.path.exists(dss_path) or not os.path.exists(coords_path):
    st.error("Required files not found in C:\\IEEE123Bus.")
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
        for i in range(len(bus_map)):
            if i not in pos:
                pos[i] = fallback[i]

    return bus_map, edges, labels, pos

# Load everything
bus_map, edges, labels, pos = load_data()
n = len(bus_map)
k = 7
fault_zones = {4, 5, 6}
zone_colors = {
    0: "#1f77b4", 1: "#ff7f0e", 2: "#2ca02c",
    3: "#9467bd", 4: "#7f0000", 5: "#7f0000", 6: "#7f0000"
}

cities = ["New York", "Chicago", "Los Angeles", "Houston", "Phoenix"]
fault_time = "2025-07-26 12:00:06"
selected_city = st.sidebar.selectbox("\U0001F4CD Select City", ["All"] + cities)

zone_data = []
zone_blackout_times = {4: 75, 5: 120, 6: 95}
zone_recovery_times = {4: 45, 5: 60, 6: 55}
resilience_scores = {
    z: round((1 - (zone_recovery_times[z] / zone_blackout_times[z])) * 10, 2)
    for z in fault_zones
}
overall_score = round(np.mean(list(resilience_scores.values())), 2)

fault_zones_detected = []
for z in fault_zones:
    label = f"Zone {z+1}"
    if z == 6:
        label += " (island)"
    fault_zones_detected.append(label)

st.markdown(f"""<div style="background-color:#ffe6e6;padding:10px;border-left:6px solid red;">
    ⚠ <strong>Faults detected in:</strong> {', '.join(fault_zones_detected)} at {fault_time}</div>""",
    unsafe_allow_html=True)

st.markdown(f"""<div style="background-color:#e6f7ff;padding:10px;border-left:6px solid #007acc;">
    💡 <strong>Average Grid Resilience Score:</strong> {overall_score} / 10</div>""", unsafe_allow_html=True)

for z in range(k):
    nodes = [i for i in range(n) if labels[i] == z]
    faults = len(nodes) if z in fault_zones else 0
    zone_data.append({
        "Zone": f"Zone {z+1}",
        "Total Nodes": len(nodes),
        "Fault Nodes": faults,
        "Fault %": round((faults / len(nodes)) * 100 if nodes else 0, 2),
        "Blackout Time (s)": zone_blackout_times.get(z, 0),
        "Recovery Time (s)": zone_recovery_times.get(z, 0),
        "Resilience Score (/10)": resilience_scores.get(z, 0),
        "City": random.choice(cities),
        "Fault Time": fault_time if z in fault_zones else "-"
    })
df = pd.DataFrame(zone_data)
zone_df = df.set_index("Zone")

recovery_steps_realistic = {
    4: ["⚡ Surge from lightning", "🔌 Breakers tripped", "🔋 PV/battery restored", "🧠 Adaptive balancing", "🔁 Manual sync"],
    5: ["⚠ Lateral overload", "⛔ Auto-isolation", "🌞 PV reroute", "📉 Load shed", "✅ Recloser active"],
    6: ["📉 Voltage sag", "🧯 Breaker isolation", "🔋 Virtual grid", "🔃 Load rebalancing", "🔗 Grid sync"]
}
islanded_plan_zone7 = [
    "⚠ Zone islanded due to multiple faults",
    "🧱 Grid-forming inverters activated",
    "🔋 Critical loads served by batteries",
    "🔄 Energy rerouted from nearby zones",
    "✅ Zone reintegrated post-synchronization"
]

if selected_city != "All":
    df = df[df["City"] == selected_city]

summary_tab, *zone_tabs = st.tabs(["Summary"] + [f"Zone {i+1}" for i in range(k)])

with summary_tab:
    st.subheader("\U0001F4CA Summary of Zones")
    st.dataframe(df, use_container_width=True)

    st.subheader("\U0001F4C9 Fault Recovery Metrics")
    fig = px.bar(df[df["Fault Nodes"] > 0], x="Zone", y="Recovery Time (s)", color="Zone", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

for i, tab in enumerate(zone_tabs):
    with tab:
        zone_name = f"Zone {i+1}"
        st.markdown(f"### {zone_name} Overview")

        zdata = zone_df.loc[zone_name]

        pie_data = pd.DataFrame({
            "Status": ["Fault", "Healthy"],
            "Count": [zdata["Fault Nodes"], zdata["Total Nodes"] - zdata["Fault Nodes"]]
        })

        pie_chart = px.pie(pie_data, names="Status", values="Count",
                           color="Status", color_discrete_map={"Fault": "red", "Healthy": "green"},
                           title="Fault vs Healthy Nodes")

        metrics = zdata.drop(["City", "Fault Time"]).to_frame().T.melt()
        bar_chart = px.bar(metrics, x="variable", y="value", color="variable", title="Zone Metrics")

        x_vals, y_vals, zone_labels = [], [], []
        for idx in range(n):
            x, y = pos[idx]
            x_vals.append(x)
            y_vals.append(y)
            zone_labels.append(f"Zone {labels[idx]+1}")

        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(
                color=[zone_colors[l] for l in labels],
                size=[12 if labels[j] == i else 5 for j in range(n)]
            ),
            text=zone_labels, hoverinfo="text"
        ))

        cluster_pts = np.array([pos[j] for j in range(n) if labels[j] == i])
        if len(cluster_pts) >= 3:
            hull = ConvexHull(cluster_pts)
            hull_pts = cluster_pts[hull.vertices]
            center = hull_pts.mean(axis=0)
            inflated = center + 1.15 * (hull_pts - center)
            inflated = np.append(inflated, [inflated[0]], axis=0)
            fig_net.add_trace(go.Scatter(
                x=inflated[:, 0], y=inflated[:, 1],
                fill='toself', fillcolor=zone_colors[i], opacity=0.3,
                line=dict(color="black"), mode='lines', showlegend=False
            ))

        fig_net.update_layout(title="Zone Topology", height=500, margin=dict(l=0, r=0, t=30, b=0))

        col1, col2, col3 = st.columns([1.1, 1, 1.5])
        col1.plotly_chart(pie_chart, use_container_width=True)
        col2.plotly_chart(bar_chart, use_container_width=True)
        col3.plotly_chart(fig_net, use_container_width=True)

        if i in fault_zones:
            st.markdown("#### 🛠 Recovery Plan")
            for step in recovery_steps_realistic[i]:
                st.markdown(f"- {step}")
            st.info(f"🕒 Blackout Time: {zone_blackout_times[i]} sec")
            st.success(f"📈 Resilience Score: {resilience_scores[i]} / 10")

        if i == 6:
            st.markdown("#### 🌐 Islanded Condition Recovery (Zone 7)")
            for step in islanded_plan_zone7:
                st.markdown(f"- {step}")
            st.info(f"🕒 Blackout Time: {zone_blackout_times[6]} sec")
            st.success(f"📈 Resilience Score: {resilience_scores[6]} / 10")