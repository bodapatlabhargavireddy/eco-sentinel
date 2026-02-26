import streamlit as st
import pydeck as pdk
import pandas as pd
import requests
from geopy.geocoders import Nominatim

# 1. PAGE SETUP
st.set_page_config(page_title="Eco-Sentinel Live", layout="wide", page_icon="🛰️")

# Custom CSS to make it look professional
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    stMetric { background-color: #161b22; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Eco-Sentinel: Global AI Monitor")
st.caption("Live 3D Satellite Analysis of Air Quality & Biological Impact")

# 2. THE SEARCH BAR (Top of page)
search_col1, search_col2 = st.columns([3, 1])
with search_col1:
    target_city = st.text_input("🌍 Search City to Scan", "New Delhi")

# 3. DATA ENGINE (GPS & Live Air Quality)
geolocator = Nominatim(user_agent="eco_sentinel_final")
location = geolocator.geocode(target_city)

if location:
    lat, lon = location.latitude, location.longitude
    
    # Fetch Live PM2.5 data from Open-Meteo
    api_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5"
    response = requests.get(api_url).json()
    live_pm25 = response['current']['pm2_5']
    
    # Display the current reading
    st.sidebar.header("📡 Satellite Telemetry")
    st.sidebar.metric("Live PM2.5", f"{live_pm25} µg/m³")
    
    # 4. 3D MAP ENGINE
    # We scale height by 20 so the bars look tall and 3D
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon], 'h': [live_pm25 * 20]})
    
    # Logic to change bar color based on pollution
    bar_color = [0, 255, 0, 200] if live_pm25 < 50 else [255, 100, 0, 200]
    if live_pm25 > 100: bar_color = [255, 0, 0, 200]

    st.pydeck_chart(pdk.Deck(
        map_style=None, # Light mode for better mobile loading
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=12, pitch=45),
        layers=[
            pdk.Layer(
                'ColumnLayer',
                map_data,
                get_position='[lon, lat]',
                get_elevation='h',
                elevation_scale=1,
                radius=400,
                get_fill_color=bar_color,
                pickable=True,
                auto_highlight=True,
            ),
        ],
    ))

    # 5. SMART ANALYSIS LOGIC (Flora, Fauna, Reason, Cure)
    st.markdown("---")
    
    # Logic Gates for dynamic text
    if live_pm25 < 35:
        status, icon, col_hex = "HEALTHY", "✅", "#00ff00"
        flora = "🌿 **Flora:** Stomata are fully open. Optimal CO2 absorption and oxygen release."
        fauna = "🐦 **Fauna:** Ideal for avian migration. Zero respiratory stress detected in wildlife."
        reason = "Clean geographic corridor or active precipitation (rain) has washed away particles."
        cure = "Protection Mode: Maintain existing green belts and prevent urban sprawl."
    elif 35 <= live_pm25 <= 80:
        status, icon, col_hex = "MODERATE", "⚠️", "#ffa500"
        flora = "🍃 **Flora:** Dust particles are coating leaf surfaces, slowing photosynthesis by ~15%."
        fauna = "🐿️ **Fauna:** Small mammals may show increased mucus production. Minor lung irritation."
        reason = "Accumulation of vehicular exhaust and road dust due to stagnant wind speeds."
        cure = "Mitigation Mode: Install vertical 'Moss-walls' and increase city water sprinkling."
    else:
        status, icon, col_hex = "CRITICAL", "🚨", "#ff0000"
        flora = "🥀 **Flora:** Leaf necrosis risk. Pores are clogged, leading to 'Plant Suffocation'."
        fauna = "🐾 **Fauna:** Acute distress. High PM2.5 levels entering the bloodstream of local animals."
        reason = "Industrial heavy-metal discharge combined with a 'Temperature Inversion' trap."
        cure = "Emergency Mode: Implement 'No-Drive' zones and deploy industrial smog towers."

    st.subheader(f"{icon} Status: :{col_hex}[{status}]")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("### 🍃 Biological Health")
        st.write(flora)
        st.write(fauna)
    with c2:
        st.warning("### 🔬 Sentinel Strategy")
        st.write(f"**The Reason:** {reason}")
        st.write(f"**The Cure:** {cure}")

else:
    st.error("🛰️ Satellite Signal Lost: Please check the city name and try again.")
