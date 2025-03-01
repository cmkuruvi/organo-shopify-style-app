import streamlit as st
import pandas as pd

# ---------------------------
# Predefined Skin Color Options with Updated HEX Codes & Images
# ---------------------------
skin_colors = {
    "Fair": "images/fair.jpg",
    "Light": "images/light.jpg",
    "Light Beige": "images/light_beige.jpg",
    "Medium": "images/medium.jpg",
    "Olive": "images/olive.jpg",
    "Tan": "images/tan.jpg",
    "Brown": "images/brown.jpg",
    "Dark Brown": "images/dark_brown.jpg",
    "Ebony": "images/ebony.jpg",
    "Deep Black": "images/deep_black.jpg"
}

# ---------------------------
# Function for Skin Color Selection with Radio Buttons & Images
# ---------------------------
def skin_color_selector():
    st.markdown("### Select Your Skin Color")
    
    selected_skin_color = st.radio(
        label="Choose a skin color:",
        options=list(skin_colors.keys()),
        format_func=lambda x: x,  # Display option name
        horizontal=False
    )

    # Display the selected image next to the radio button
    st.image(skin_colors[selected_skin_color], width=200, caption=selected_skin_color)

    return selected_skin_color
