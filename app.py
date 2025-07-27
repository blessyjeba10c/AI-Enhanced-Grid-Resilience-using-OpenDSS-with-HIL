import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine, text
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=30000, key="datarefresh")


db_path = os.path.abspath("grid.db")
engine = create_engine(f"sqlite:///{db_path}", future=True)

API_KEY = "dd4d50aa723c21d190cd840f11a01efb"
CITY_LIST = ["Chennai", "Mumbai", "Delhi", "Kolkata", "Bangalore", "Hyderabad", "Ahmedabad"]

selected_city = st.selectbox("Select City", CITY_LIST, index=0)

weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}&units=metric"
weather = requests.get(weather_url).json()

if 'main' in weather:
    temp = weather['main']['temp']
    humidity = weather['main']['humidity']
    wind_speed = round(weather['wind']['speed'] * 3.6, 2)  # Convert to km/h
    rainfall_mm = weather.get("rain", {}).get("1h", 0.0)

    st.title(" Grid Resilience Dashboard")
    st.subheader(f"Weather in {selected_city}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(" Temperature", f"{temp} °C")
    col2.metric(" Humidity", f"{humidity}%")
    col3.metric(" Wind Speed", f"{wind_speed} km/h")
    col4.metric(" Rainfall", f"{rainfall_mm} mm")

    if wind_speed > 40:
        trigger_reason = " Fault Triggered: Wind speed exceeds 40 km/h"
    elif rainfall_mm > 10:
        trigger_reason = " Fault Triggered: Rainfall exceeds 10 mm"
    else:
        trigger_reason = " No fault: Weather is within safe range"

    st.markdown(f"<div style='color:{'red' if '' in trigger_reason else 'green'}; font-size:16px;'>{trigger_reason}</div>", unsafe_allow_html=True)
else:
    st.error("Failed to fetch weather data. Check API key or city name.")


query = "SELECT * FROM resilience_data"
try:
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
except Exception as e:
    st.error(f"Failed to load grid data: {e}")
    st.stop()

st.subheader(" Zone-Wise Resilience Summary")

# Show metrics for each zone
zones = df['zone'].unique()
for zone in zones:
    zdata = df[df['zone'] == zone].iloc[0]
    with st.container():
        st.markdown(f"### 🔹{zone}")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Fault", zdata['fault'])
        c2.metric("Resilience Score", zdata['resilience_score'])
        c3.metric("Blackout Time", f"{random.randint(10, 60) if zdata['fault'] == 'Yes' else 0} min")
        c4.metric("Recovery Time", f"{random.randint(20, 90) if zdata['fault'] == 'Yes' else 5} min")
        c5.metric("Load Lost", f"{random.uniform(20, 100) if zdata['fault'] == 'Yes' else random.uniform(5, 20):.2f} MW")
        c6.metric("Power Restored", f"{random.uniform(10, 90):.2f} MW")
        st.divider()

st.subheader(" Fault Distribution")
fault_counts = df['fault'].value_counts().reset_index()
fault_counts.columns = ['fault_status', 'count']
fig = px.pie(fault_counts, names='fault_status', values='count', title='Fault vs No Fault Zones')
st.plotly_chart(fig)
