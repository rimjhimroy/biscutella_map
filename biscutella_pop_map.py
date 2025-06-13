import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("🧬 Biscutella Population Map (Switzerland)")

# Load sample-level data
raw_data = pd.read_csv("biscutella_pops.csv")

# Aggregate by population
grouped = raw_data.groupby("population").agg({
    "lat": "mean",
    "lon": "mean",
    "WGS": "sum",
    "RADseq": "sum",
    "Assembly": "max"
}).reset_index()

# Compute color based on sequencing data
def get_color(row):
    if row["WGS"] == 1 and row["RADseq"] == 1:
        return [255, 255, 0, 160]  # Yellow = both
    elif row["WGS"] == 1:
        return [255, 0, 0, 160]  # Red = WGS only
    elif row["RADseq"] == 1:
        return [0, 255, 0, 160]  # Green = RADseq only
    else:
        return [120, 120, 120, 100]  # Gray = no data

def get_line_color(row):
    return [0, 0, 0, 255] if row["Assembly"] == 1 else [0, 0, 0, 0]

grouped_data = grouped
grouped["color"] = grouped.apply(get_color, axis=1)
grouped["line_color"] = grouped.apply(get_line_color, axis=1)


# Tooltip
tooltip = {
    "html": """
    <b>{population}</b><br/>
    WGS: {WGS}<br/>
    RADseq: {RADseq}<br/>
    Assembly: {Assembly}
    """,
    "style": {
        "backgroundColor": "black",
        "color": "white"
    }
}


# Map
st.write("### 🗺️ Population Map")
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
            data=grouped,
            get_position='[lon, lat]',
            get_fill_color="color",
            get_line_color="line_color",
            get_radius=4000,
            line_width_min_pixels=2,
            pickable=True,
        )
    ],
    tooltip=tooltip
))

# Show population-level table
st.write("### 📋 Population Summary")
st.dataframe(grouped_data)

# Selection dropdown
pop_options = grouped["population"].unique().tolist()
selected_pops = st.multiselect("🔍 Select population(s) to view:", pop_options, default=pop_options)

# Filter by selection
filtered = raw_data[raw_data["population"].isin(selected_pops)]

# Show table
st.write("### 📋 Filtered Population Summary")
st.dataframe(filtered)
