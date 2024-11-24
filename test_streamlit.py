import streamlit as st
import pandas as pd

# Basic title and text
st.title("Test Streamlit App")
st.write("Hello! This is a test to see if Streamlit is working.")

# Add a simple interactive element
if st.button("Click me!"):
    st.write("Button was clicked!")

# Add a simple number input
number = st.number_input("Enter a number", value=0)
st.write(f"You entered: {number}")