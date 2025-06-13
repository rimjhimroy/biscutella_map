import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("🧬 Biscutella Sample Map (Switzerland)")

# Load CSV data
data = pd.read_csv("biscutella_samples.csv")

# Compute color based on sequencing data
def get_color(row):
    if row["WGS"] == 1 and row["RADseq"] == 1:
        return [255, 255, 0, 160]  # Yellow = both
    elif row["WGS"] == 1:
        return [255, 0, 0, 160]  # Red = WGS only
    elif row["RADseq"] == 1:
        return [0, 255, 0, 160]  # Green = RADseq only
    else:
        return [120, 120, 120, 100]  # Gray = no sequencing info

def get_line_color(row):
    return [0, 0, 0, 255] if row["Assembly"] == 1 else [0, 0, 0, 0]

data["color"] = data.apply(get_color, axis=1)
data["line_color"] = data.apply(get_line_color, axis=1)

# Show data table
st.write("### 📋 Sample Metadata")
st.dataframe(data)

# Tooltip
tooltip = {
    "html": """
    <b>{sample_id}</b><br/>
    Population: {population}<br/>
    WGS: {WGS}<br/>
    RADseq: {RADseq}<br/>
    Genome Assembly: {Assembly}
    """,
    "style": {
        "backgroundColor": "black",
        "color": "white"
    }
}

# Map
st.write("### 🗺️ Sample Map")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=46.8,
        longitude=8.3,
        zoom=7,
        pitch=40,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=data,
            get_position='[lon, lat]',
            get_fill_color="color",
            get_line_color="line_color",
            get_radius=3000,
            line_width_min_pixels=2,
            pickable=True,
        )
    ],
    tooltip=tooltip
))
