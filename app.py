import streamlit as st
import pydeck as pdk
import pandas as pd
from geopy.geocoders import Nominatim

# 1. Page Configuration
st.set_page_config(page_title="Eco-Sentinel 3D", layout="wide")
st.title("🛰️ Eco-Sentinel: Global Health Monitor")

# 2. Sidebar Controls
st.sidebar.header("Command Center")
target_city = st.sidebar.text_input("Enter City Name", "New Delhi")
pollution_level = st.sidebar.slider("Pollution Pulse", 0, 1000, 400)

# 3. GPS Logic
geolocator = Nominatim(user_agent="eco_sentinel_app")
location = geolocator.geocode(target_city)

if location:
    lat, lon = location.latitude, location.longitude
    st.sidebar.success(f"Tracking: {target_city}")

    # 4. 3D Map Data
    data = pd.DataFrame({
        'lat': [lat, lat + 0.005, lat - 0.005, lat + 0.002],
        'lon': [lon, lon + 0.005, lon - 0.005, lon - 0.002],
        'h': [pollution_level, pollution_level * 1.2, pollution_level * 0.8, pollution_level * 1.5]
    })

    # 5. The 3D Map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=13, pitch=45),
        layers=[pdk.Layer('ColumnLayer', data, get_position='[lon, lat]', get_elevation='h', 
                          elevation_scale=10, radius=200, get_fill_color=[255, 165, 0, 180])],
    ))

    # 6. BIOLOGICAL IMPACT REPORTS
    st.markdown("---")
    st.header(f"🍃 Environmental Impact: {target_city}")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌲 Flora (Plants)")
        if pollution_level > 500:
            st.error("🚨 **CRITICAL**: Stomata closing. Growth stunted due to Nitrogen saturation.")
        else:
            st.success("✅ **HEALTHY**: Urban canopy is performing optimal Carbon capture.")

    with col2:
        st.subheader("🐾 Fauna (Wildlife)")
        if pollution_level > 500:
            st.error("🚨 **DANGER**: Avian respiratory distress. Pollinator migration disrupted.")
        else:
            st.success("✅ **STABLE**: Wildlife activity is normal. No chemical threats.")

    # 7. NEW: REASON AND PREVENTION (The "Scientist" Section)
    st.markdown("---")
    st.header("🔬 Sentinel Strategy: Root Cause & Cure")
    
    cause_col, cure_col = st.columns(2)

    with cause_col:
        st.info("### 🔍 The Reason")
        if pollution_level > 600:
            st.write(f"**Primary Cause:** Excessive Nitrogen runoff from nearby agriculture and high PM2.5 from urban traffic in {target_city}.")
            st.write("**Mechanism:** Particulate matter is coating leaf surfaces, blocking sunlight and heating the local micro-climate.")
        else:
            st.write("**Primary Status:** Low industrial discharge and balanced green-cover ratio.")

    with cure_col:
        st.warning("### 🛠️ The Cure (Prevention)")
        if pollution_level > 600:
            st.write("1. **Buffer Zones:** Plant 'Green Belts' around industrial zones to filter air.")
            st.write("2. **Precision Ag:** Use IoT sensors to reduce fertilizer runoff by 30%.")
            st.write("3. **Vertical Forests:** Integrate moss-walls to absorb heavy metals from the air.")
        else:
            st.write("1. **Maintenance:** Continue current 'Protected Area' status.")
            st.write("2. **Monitoring:** Keep Sentinel sensors active for early detection.")

else:
    st.error("Searching for city coordinates...")
