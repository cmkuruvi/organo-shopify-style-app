import streamlit as st
import pandas as pd

# ---------------------------
# Custom CSS for Montserrat font and styling
# ---------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
    }
    .output {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .swatch {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #ccc;
        margin: 5px;
        display: inline-block;
        cursor: pointer;
    }
    .swatch-label {
        text-align: center;
        font-size: 0.8em;
    }
    .swatch-container {
        display: flex;
        flex-wrap: wrap;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Predefined Skin Color Options with HEX codes (update as needed)
# ---------------------------
skin_colors = {
    "Fair": "#FCE2C6",
    "Light": "#F7D4B4",
    "Light Beige": "#EAD2B0",
    "Medium": "#D3A179",
    "Olive": "#8F9779",
    "Tan": "#D2B48C",
    "Brown": "#8B4513",
    "Dark Brown": "#654321",
    "Ebony": "#555D50",
    "Deep Black": "#000000"
}

# Function to render a swatch-based selector for Skin Color.
def skin_color_selector():
    st.markdown("### Select Your Skin Color")
    chosen_color = st.session_state.get("skin_color", list(skin_colors.keys())[0])
    cols = st.columns(len(skin_colors))
    for idx, (color_name, hex_code) in enumerate(skin_colors.items()):
        with cols[idx]:
            # Use an empty button for selection with the swatch displayed above it.
            if st.button("", key=f"skin_{idx}", help=color_name):
                st.session_state.skin_color = color_name
                chosen_color = color_name
            st.markdown(f"<div class='swatch' style='background-color: {hex_code};'></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='swatch-label'>{color_name}</div>", unsafe_allow_html=True)
    # Default selection if none chosen yet
    if "skin_color" not in st.session_state:
        st.session_state.skin_color = list(skin_colors.keys())[0]
    return st.session_state.skin_color

# ---------------------------
# Mapping for Exclusive Color Group images (replace URLs with actual image links)
# ---------------------------
color_group_images = {
    "Velvet Ember": "https://via.placeholder.com/150?text=Velvet+Ember",
    "Earthy Espresso": "https://via.placeholder.com/150?text=Earthy+Espresso",
    "Indigo Nomad": "https://via.placeholder.com/150?text=Indigo+Nomad",
    "Midnight Commander": "https://via.placeholder.com/150?text=Midnight+Commander",
    "Evergreen Chic": "https://via.placeholder.com/150?text=Evergreen+Chic",
    "Sun-Kissed Bliss": "https://via.placeholder.com/150?text=Sun-Kissed+Bliss",
    "Peachy Whimsy": "https://via.placeholder.com/150?text=Peachy+Whimsy",
    "Golden Zest": "https://via.placeholder.com/150?text=Golden+Zest",
    "Celestial Sapphire": "https://via.placeholder.com/150?text=Celestial+Sapphire",
    "Frosted Elegance": "https://via.placeholder.com/150?text=Frosted+Elegance"
}

# ---------------------------
# Load Data: Mapping and Product URL mapping
# ---------------------------
mapping_file = "demography_shirt.csv"
df = pd.read_csv(mapping_file)

product_mapping_file = "Fabric Crosswalk_ColorQuiz_URL.csv"
product_df = pd.read_csv(product_mapping_file)

# ---------------------------
# App Header and Sidebar
# ---------------------------
st.image("2.png", width=200)
st.title("Discover Your Color Psyche")

with st.sidebar:
    st.header("Customize Your Experience")
    st.markdown("Adjust settings or view UI feedback questions.")

# ---------------------------
# Collecting User Inputs
# ---------------------------
st.header("Tell us about yourself:")

col1, col2 = st.columns(2)

with col1:
    # Gender input updated to the provided options
    gender = st.radio("Gender:", ["Male", "Female", "Unisex"])
    selected_skin_color = skin_color_selector()
    # Hair Color options updated per the table
    hair_color = st.radio("Hair Color:", ["Blonde", "Black", "Dark Brown", "Red", "Other"])

with col2:
    st.markdown("### Exclusive Color Group Name")
    # Dropdown for color group selection (with image display)
    selected_color_group = st.selectbox("Choose your Color Group:", list(color_group_images.keys()))
    st.image(color_group_images[selected_color_group], width=150)
    
    # Style Word updated with additional options
    style_word = st.radio("Style Word:", ["Classic", "Minimalist", "Bold & Expressive", "Relaxed & Effortless", "Timeless", "Fashion-Forward"])
    
    # Clothing Occasion updated with provided options
    clothing_occasion = st.radio("Clothing Occasion:", [
        "Work Attire", "Special Occasions", "Vacations", "Formal Events", 
        "Everyday Wear", "Gifts", "Travel", "Seasonal Changes"
    ])

# ---------------------------
# Process and Display the Recommendation
# ---------------------------
if st.button("Get My Color Psyche"):
    # Filter the dataframe based on user inputs using the updated column names
    filtered_df = df[
        (df["Skin Color"] == selected_skin_color) &
        (df["Gender"] == gender) &
        (df["Hair Color"] == hair_color) &
        (df["Exclusive Color Group Name"] == selected_color_group) &
        (df["Style Word"] == style_word) &
        (df["Clothing Occasion"] == clothing_occasion)
    ]
    
    if not filtered_df.empty:
        result = filtered_df.iloc[0][[
            "Style Persona", "Celebrity Wardrobe Inspiration", "Top Clothing Priority", 
            "Color Statement", "Suggested Shirt Colors", "Suggested Suit Colors", "Suggested Pant Colors"
        ]]
        st.success("Here’s your personalized style recommendation!")
        
        # Function to convert suggested color names into clickable Shopify product links.
        def create_link(color):
            url = product_df.loc[product_df["Color Name"] == color, "Product URL"]
            if not url.empty:
                return f"[{color}]({url.values[0]})"
            else:
                return color
        
        st.markdown("<div class='output'>", unsafe_allow_html=True)
        for key, value in result.items():
            if key in ["Suggested Shirt Colors", "Suggested Suit Colors", "Suggested Pant Colors"]:
                colors = [c.strip() for c in str(value).split(",")]
                linked_colors = [create_link(c) for c in colors]
                st.markdown(f"**{key}:** " + ", ".join(linked_colors))
            else:
                st.markdown(f"**{key}:** {value}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No exact match found! Please try different input values.")

# ---------------------------
# UI Improvement Feedback Section
# ---------------------------
st.markdown("### UI Improvement Feedback")
st.markdown("1. Does the swatch layout for Skin Color clearly display each option?")
st.markdown("2. Is the image display for the Exclusive Color Group helpful for your selection?")
st.markdown("3. Are the clickable product links correctly directing to your Shopify store?")
