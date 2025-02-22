import streamlit as st
import pandas as pd

# Load the dataset
csv_file = "demography_all_possible_combinations.csv"
df = pd.read_csv(csv_file)

st.title("Find Your Perfect Style")

# Collecting user inputs
skin_tone = st.radio("Skin Tone (Undertone):", ["Warm", "Cool", "Neutral"])
skin_color = st.radio("Skin Color:", ["Fair", "Golden", "Porcelain", "Olive", "Honey"])
hair_color = st.radio("Hair Color:", ["Blonde", "Dark Brown", "Black", "Red"])
eye_color = st.radio("Eye Color:", ["Blue", "Green", "Dark Brown", "Hazel"])
personality = st.radio("Personality:", ["Bold", "Classic", "Earthy", "Soft/Romantic"])
color_group = st.radio("Exclusive Color Group Name:", ["Velvet Ember", "Earthy Espresso", "Indigo Nomad", "Midnight Commander", "Evergreen Chic", "Sun-Kissed Bliss", "Peachy Whimsy", "Golden Zest", "Celestial Sapphire", "Frosted Elegance"])
style_word = st.radio("Style in One Word:", ["Classic", "Minimalist", "Bold & Expressive", "Relaxed & Effortless"])

if st.button("Get My Style"):
    filtered_df = df[
        (df["Skin Tone"] == skin_tone) &
        (df["Skin Color"] == skin_color) &
        (df["Hair Color"] == hair_color) &
        (df["Eye Color"] == eye_color) &
        (df["Personality"] == personality) &
        (df["Exclusive Color Group Name"] == color_group) &
        (df["Style in One Word"] == style_word)
    ]

    if not filtered_df.empty:
        result = filtered_df.iloc[0][[
            "Style Persona", "Best Occasions for This Color", "Power Statement",
            "Suggested Shirt Colors", "Top Clothing Priority",
            "Celebrity Wardrobe Inspiration"
        ]]
        st.success("Here’s your personalized style recommendation!")
        for key, value in result.items():
            st.write(f"**{key}:** {value}")
    else:
        st.warning("No exact match found! Try different input values.")
