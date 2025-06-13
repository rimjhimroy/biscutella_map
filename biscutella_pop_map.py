import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("📍 Biscutella Population Genomics Map")

# Load your data
@st.cache_data
def load_data():
    return pd.read_csv("biscutella_pops.csv")  # Replace with your uploaded file name

data = load_data()

# Define a tooltip to show sequencing details
tooltip = {
    "html": """
    <b>{population}</b><br/>
    WGS: {WGS_count}<br/>
    RADseq: {RADseq_count}<br/>
    Genome Assembly: {Assembly}
    """,
    "style": {
        "backgroundColor": "navy",
        "color": "white",
        "fontSize": "12px"
    }
}

# Visual layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_radius=25000,
    get_fill_color='[WGS_count*60, RADseq_count*60, Assembly*255, 180]',
    pickable=True,
)

# Show map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=data['lat'].mean(),
        longitude=data['lon'].mean(),
        zoom=7,
        pitch=30,
    ),
    layers=[layer],
    tooltip=tooltip
))
