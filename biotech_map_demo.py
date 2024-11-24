import streamlit as st
    import folium
    import pandas as pd
    from streamlit_folium import folium_static
    st.write("All imports successful!")
except Exception as e:
    st.write(f"Error importing: {str(e)}")

# Set page configuration
st.set_page_config(page_title="Biotech Innovation Map", layout="wide")

# Title and description
st.title("Biotech Innovation Map")
st.write("Interactive map showing biotech innovation centers across the US")

# Define regions
regions = {
    "Pacific Coast": ["WA", "OR", "CA"],
    "Mountain West": ["MT", "ID", "WY", "NV", "UT", "CO", "AZ", "NM"],
    "Midwest": ["ND", "SD", "NE", "KS", "MN", "IA", "MO", "WI", "IL", "IN", "MI", "OH"],
    "Mid-Atlantic": ["NY", "PA", "NJ", "DE", "MD", "DC", "VA", "WV"],
}

# Sample university data
universities = {
    "Stanford University": {
        "lat": 37.4275, 
        "lon": -122.1697,
        "state": "CA",
        "startups": ["Startup A", "Startup B"]
    },
    "MIT": {
        "lat": 42.3601, 
        "lon": -71.0942,
        "state": "MA",
        "startups": ["Startup C", "Startup D"]
    },
}

# Create sidebar
st.sidebar.title("Controls")
selected_region = st.sidebar.selectbox("Choose a region", list(regions.keys()))

# Create the map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

# Add university markers to the map
for univ_name, univ_data in universities.items():
    folium.Marker(
        location=[univ_data["lat"], univ_data["lon"]],
        popup=univ_name,
        tooltip=univ_name
    ).add_to(m)

# Display the map
st.write("### Interactive Map")
folium_static(m)

# Display region information
st.write(f"### Selected Region: {selected_region}")
st.write(f"States in this region: {', '.join(regions[selected_region])}")

# Display university information
st.write("### Universities and Startups")
for univ_name, univ_data in universities.items():
    st.write(f"**{univ_name}**")
    st.write(f"Location: {univ_data['lat']}, {univ_data['lon']}")
    st.write("Startups:", ", ".join(univ_data["startups"]))
    st.write("---")
