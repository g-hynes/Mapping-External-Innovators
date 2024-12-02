import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import requests
import pandas as pd

# Set page config
st.set_page_config(layout="wide", page_title="Biotech Innovation Map")

# Title
st.markdown("""
    <h1 style='text-align: center; color: #2C3E50; margin-bottom: 1rem;'>
        US Biotech Innovation Map
    </h1>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_state' not in st.session_state:
    st.session_state.current_state = None

# Load US states data
@st.cache_data
def load_states_data():
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"
    response = requests.get(url)
    data = response.json()
    # Filter for continental US states
    data['features'] = [feature for feature in data['features'] 
                       if feature['properties']['name'] not in ['Alaska', 'Hawaii']]
    return data

# Load university data
df = pd.read_csv('mapping_data.csv')
df.columns = df.columns.str.strip()

# Load the states data
states_data = load_states_data()

# Main app logic
if st.session_state.current_state is None:
    # Create main map
    m = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=4,
        tiles=None,
        min_zoom=4,
        max_zoom=8
    )
    
    # Add state boundaries
    states = folium.GeoJson(
        states_data,
        name='States',
        style_function=lambda x: {
            'fillColor': '#A8C7DC',
            'color': '#2C3E50',
            'weight': 1.5,
            'fillOpacity': 0.7
        },
        highlight_function=lambda x: {
            'fillColor': '#3498DB',
            'color': '#2C3E50',
            'weight': 2,
            'fillOpacity': 0.9
        }
    ).add_to(m)
    
    # Display the map
    map_data = st_folium(
        m,
        width="100%",
        height=700,
        returned_objects=['last_active_drawing'],
        key="main_map"
    )
    
    # Add state selector in a less obtrusive way
    with st.sidebar:
        states_list = sorted([feature['properties']['name'] for feature in states_data['features']])
        selected_state = st.selectbox("Select a state:", [""] + states_list, key="state_selector")
        if selected_state:
            st.session_state.current_state = selected_state
            st.experimental_rerun()

else:
    # Show state detail view
    st.markdown(f"### {st.session_state.current_state}")
    
    # Add back button
    if st.button("← Back to US Map"):
        st.session_state.current_state = None
        st.experimental_rerun()
    
    # Filter universities for selected state
    state_unis = df[df['State'] == st.session_state.current_state]
    
    if len(state_unis) > 0:
        # Create state-level map with disabled zoom
        state_feature = next(f for f in states_data['features'] 
                           if f['properties']['name'] == st.session_state.current_state)
        
        # Calculate bounds for the state
        bounds = folium.features.get_bounds(state_feature)
        state_map = folium.Map(
            location=[state_unis['Latitude'].mean(), state_unis['Longitude'].mean()],
            zoom_start=7,
            tiles=None,
            zoom_control=False,
            dragging=False,
            scrollWheelZoom=False,
            doubleClickZoom=False
        )
        
        # Fit map to state bounds
        state_map.fit_bounds(bounds)
        
        # Add state boundary
        folium.GeoJson(
            state_feature,
            style_function=lambda x: {
                'fillColor': '#A8C7DC',
                'color': '#2C3E50',
                'weight': 1.5,
                'fillOpacity': 0.3
            }
        ).add_to(state_map)
        
        # Add university markers
        for idx, row in state_unis.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=8,
                color='#2C3E50',
                fill=True,
                fillOpacity=0.7,
                tooltip=row['University'].strip()
            ).add_to(state_map)
        
        # Display the state map
        st_folium(state_map, width="100%", height=500)
        
        # Add interactive table
        st.markdown("### Universities and Startups")
        
        # Prepare data for display
        display_df = state_unis[['University', 'Startup', 'Founder', 'Therapeutic Area']].copy()
        display_df.columns = ['University', 'Startup', 'Scientific Founder', 'Therapeutic Area']
        
        # Display the table
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        




