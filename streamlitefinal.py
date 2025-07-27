import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import networkx as nx
from sklearn.cluster import SpectralClustering
from opendssdirect import dss
import os
import plotly.express as px


st.set_page_config(
    page_title="grid_dashboard",  
    page_icon="",                 
    layout="wide"                
)
st.set_page_config(layout="wide")
st.title(" IEEE 123 Bus Fault Visualization Dashboard")
folder_path = r"C:\IEEE123Bus"
dss_path = os.path.join(folder_path, "IEEE123Master.dss")
coords_path = os.path.join(folder_path, "BusCoords.dat")
if not os.path.exists(dss_path) or not os.path.exists(coords_path):
    st.error("Required files not found. Ensure IEEE123Master.dss and BusCoords.dat are under C:\\IEEE123Bus")
else:
    try:
        dss.Basic.ClearAll()
        dss.Text.Command(f'Redirect "{dss_path}"')
        dss.Text.Command("Solve")
        coords = pd.read_csv(coords_path, sep=r"[,\s]+", names=["Bus", "X", "Y"], index_col="Bus", engine="python")
        bus_map, edges, idx = {}, [], 0
        ptr = dss.Lines.First()
        while ptr:
            b1 = dss.Lines.Bus1().split('.')[0]
            b2 = dss.Lines.Bus2().split('.')[0]
            for b in (b1, b2):
                if b not in bus_map:
                    bus_map[b] = idx; idx += 1
            r = dss.Lines.R1()
            if r > 0:
                edges.append((bus_map[b1], bus_map[b2], 1.0 / r))
            ptr = dss.Lines.Next()
        n = len(bus_map)
        W = np.zeros((n, n))
        for u, v, w in edges:
            W[u, v] = W[v, u] = w

        k = 7
        clustering = SpectralClustering(n_clusters=k, affinity='precomputed', random_state=42)
        labels = clustering.fit_predict(W)
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
        fault_zones = {4, 5, 6}
        zone_data = []
        zone_metrics = {}
        for z in range(k):
            nodes = [i for i in range(n) if labels[i] == z]
            fault_count = len(nodes) if z in fault_zones else 0
            zone_name = f"Zone {z+1}"
            zone_data.append({
                "Zone": zone_name,
                "Total Nodes": len(nodes),
                "Fault Nodes": fault_count,
                "Fault %": round((fault_count / len(nodes)) * 100 if nodes else 0, 2)
            })
            zone_metrics[zone_name] = {
                "Total Nodes": len(nodes),
                "Fault Nodes": fault_count,
                "Fault %": round((fault_count / len(nodes)) * 100 if nodes else 0, 2)
            }

        df = pd.DataFrame(zone_data)
        st.subheader(" Zone Summary Table")
        st.dataframe(df, use_container_width=True)
        st.subheader(" Fault Overview by Zone")
        fig_bar = px.bar(df, x="Zone", y=["Fault Nodes", "Total Nodes", "Fault %"],
                 barmode="group", title="Zone-wise Fault Summary",
                 height=400, width=700,  # Adjust as needed
                 color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_bar)
        selected_zone = st.selectbox("Select Zone to View Detailed Metrics", df["Zone"])
        zone_info = df[df["Zone"] == selected_zone].iloc[0]
        st.subheader(f" {selected_zone} Fault Distribution")
        pie_data = pd.DataFrame({
            "Status": ["Fault", "Healthy"],
            "Count": [zone_info["Fault Nodes"], zone_info["Total Nodes"] - zone_info["Fault Nodes"]]
        })
        fig_pie = px.pie(pie_data, names="Status", values="Count",
                         color="Status", color_discrete_map={"Fault": "red", "Healthy": "green"},
                         title=f"{selected_zone} - Fault vs Healthy Nodes")
        st.plotly_chart(fig_pie, use_container_width=True)
        st.subheader(f" {selected_zone} Metrics Bar Chart")
        fig, ax = plt.subplots()
        metric_vals = zone_metrics[selected_zone]
        ax.bar(metric_vals.keys(), metric_vals.values(), color='orange')
        ax.set_ylabel("Value")
        ax.set_title(f"{selected_zone} Metrics")
        st.pyplot(fig)
        st.subheader(" Full Network Visualization")
        fig, ax = plt.subplots(figsize=(10, 7))
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_weighted_edges_from(edges)

        zone_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd',
                       '#d62728', '#e377c2', '#8c564b']
        selected_index = int(selected_zone.split()[-1]) - 1
        for z in range(k):
            nds = [i for i in range(n) if labels[i] == z]
            size = 100 if z == selected_index else 30
            nx.draw_networkx_nodes(G, pos, nodelist=nds, node_color=zone_colors[z], node_size=size, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#ccc", alpha=0.4, ax=ax)
        ax.set_title("IEEE 123 Bus Grid with Fault Zones", fontsize=14)
        ax.axis("off")
        st.pyplot(fig)

    except Exception as e:
        st.error(f" Error during processing: {e}")


