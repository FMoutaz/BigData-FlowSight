import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
st.set_page_config(page_title="FlowSight Dashboard", layout="wide")

st.title("🛣️ FlowSight Live Congestion Dashboard")

SENSOR_CHOICES = ["roadA", "roadB", "roadC"]

SENSOR_COORDS = {
    "roadA": {"lat": 40.7580, "lon": -73.9855},  # Times Square
    "roadB": {"lat": 40.730610, "lon": -73.935242},  # East Village
    "roadC": {"lat": 40.7527, "lon": -73.9772},  # Grand Central
}


# Sidebar controls
sensor = st.sidebar.selectbox("Choose sensor", SENSOR_CHOICES)
speed_input = st.sidebar.slider("Current speed", min_value=0, max_value=100, value=50)
timestamp = int(time.time())

if st.sidebar.button("Get Prediction"):
    payload = {
        "sensor": sensor,
        "speed": speed_input,
        "timestamp": timestamp
    }
    r = requests.post("http://127.0.0.1:8000/predict", json=payload)
    if r.status_code == 200:
        pred = r.json()["predicted_speed_next"]
        st.success(f"Predicted next speed: **{pred:.1f}**")
    else:
        st.error(f"API error {r.status_code}: {r.text}")

# Show a little history of your calls
if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button("Add to history"):
    # Log the current call
    st.session_state.history.append({
        "time": pd.to_datetime(timestamp, unit="s"),
        "sensor": sensor,
        "lat": SENSOR_COORDS[sensor]["lat"],
        "lon": SENSOR_COORDS[sensor]["lon"],
        "speed": speed_input,
        "predicted": pred if 'pred' in locals() else None
    })

# Display history table
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.subheader("🏷️ Query History")
    st.dataframe(df, use_container_width=True)



import pydeck as pdk

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    st.subheader("🌍 FlowSight Map View")
    # Center map roughly in the middle of your sensors
    midpoint = (
        df["lat"].mean(),
        df["lon"].mean()
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["lon", "lat"],
        get_fill_color=[
            # color coding: red for slow, green for fast
            "255 * (1 - (speed / 100))",
            "255 * (speed / 100)",
            50
        ],
        get_radius=100,
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        longitude=midpoint[1], latitude=midpoint[0], zoom=12, pitch=30
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Sensor: {sensor}\nSpeed: {speed}\nNext: {predicted}"}
    )

    st.pydeck_chart(deck)
