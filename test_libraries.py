try:
    import streamlit as st
    print("✓ Streamlit installed")
    import folium
    print("✓ Folium installed")
    import geopandas as gpd
    print("✓ Geopandas installed")
    import pandas as pd
    print("✓ Pandas installed")
except ImportError as e:
    print(f"Error: {e}")