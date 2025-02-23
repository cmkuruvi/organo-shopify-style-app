import streamlit as st
import pandas as pd

# ---------------------------
# Custom CSS with brand colors and improved layout
# ---------------------------
st.markdown("""
    <style>
    :root {
      --green: #0c4852;
      --mustard: #bb9236;
      --pistachio: #b1c7bb;
      --white: #ffffff;
      --black: #000000;
    }
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: var(--white);
        color: var(--black);
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--green);
    }
    .output {
        background-color: var(--pistachio);
        color: var(--black);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .swatch {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 2px solid #ccc;
        margin: 2px auto;
        display: block;
        cursor: pointer;
    }
    .swatch-label {
        text-align: center;
        font-size: 0.7em;
        margin-top: 2px;
    }
    .swatch-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Predefined Skin Color Options with updated HEX codes
# ---------------------------
skin_colors = {
    "Fair": "#FFE0BD",
    "Light": "#FFCD94",
    "Light Beige": "#EAC086",
    "Medium": "#D8A47F",
    "Olive": "#C68642",
    "Tan": "#8D5524",
    "Brown": "#7D4B20",
    "Dark Brown": "#5C3A21",
    "Ebony": "#3B2F2F",
    "Deep Black": "#1C1C1C"
}

def skin_color_selector():
    st.markdown("### Select Your Skin Color")
    chosen_color = st.session_state.get("skin_color", list(skin_colors.keys())[0])
    # Create swatches in a single row; each swatch with its label below it
    cols = st.columns(len(skin_colors))
    for idx, (color_name, hex_code) in enumerate(skin_colors.items()):
        with cols[idx]:
            if st.button("", key=f"skin_{idx}", help=color_name):
                st.session_state.skin_color = color_name
                chosen_color = color_name
            st.markdown(f"<div class='swatch' style='background-color: {hex_code};'></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='swatch-label'>{color_name}</div>", unsafe_allow_html=True)
    if "skin_color" not in st.session_state:
        st.session_state.skin_color = list(skin_colors.keys())[0]
    return st.session_state.skin_color

# ---------------------------
# Mapping for Exclusive Color Group images (replace placeholder URLs with actual image links)
# ---------------------------
color_group_images = {
    "Velvet Ember": "images/Velvet Ember.jpg",
    "Earthy Espresso": "images/Earthy Espresso.jpg",
    "Indigo Nomad": "images/Indigo Nomad.jpg",
    "Midnight Commander": "images/Midnight Commander.jpg",
    "Evergreen Chic": "images/Evergreen Chic.jpg",
    "Sun-Kissed Bliss": "images/Sun-Kissed Bliss.jpg",
    "Peachy Whimsy": "images/Peachy Whimsy.jpgy",
    "Golden Zest": "images/Golden Zest.jpg",
    "Celestial Sapphire": "images/Celestial Sapphire.jpg",
    "Frosted Elegance": "images/Frosted Elegance.jpg"
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
    gender = st.radio("Gender:", ["Male", "Female", "Unisex"])
    selected_skin_color = skin_color_selector()
    hair_color = st.radio("Hair Color:", ["Blonde", "Black", "Dark Brown", "Red", "Other"])

with col2:
    st.markdown("### Exclusive Color Group Name")
    selected_color_group = st.selectbox("Choose your Color Group:", list(color_group_images.keys()))
    st.image(color_group_images[selected_color_group], width=150)
    
    style_word = st.radio("Style Word:", ["Classic", "Minimalist", "Bold & Expressive", "Relaxed & Effortless", "Timeless", "Fashion-Forward"])
    clothing_occasion = st.radio("Clothing Occasion:", [
        "Work Attire", "Special Occasions", "Vacations", "Formal Events", 
        "Everyday Wear", "Gifts", "Travel", "Seasonal Changes"
    ])

# ---------------------------
# Process and Display the Recommendation (only Suggested Shirt Colors)
# ---------------------------
if st.button("Get My Color Psyche"):
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
            "Color Statement", "Suggested Shirt Colors"
        ]]
        st.success("Here’s your personalized style recommendation!")
        
        def create_link(color):
            url = product_df.loc[product_df["Item Name ORGANO"] == color, "URL"]
            if not url.empty:
                return f"[{color}]({url.values[0]})"
            else:
                return color
        
        # Improved output layout with subheadings and spacing
        with st.container():
            st.subheader("Your Style Recommendation")
            
            st.markdown("### Style Persona:")
            st.write(result["Style Persona"])
            
            st.markdown("***Celebrity Wardrobe Inspiration:***")
            st.write(result["Celebrity Wardrobe Inspiration"])
            
            st.markdown("**Top Clothing Priority:**")
            st.write(result["Top Clothing Priority"])
            
            st.markdown("**Color Statement:**")
            st.subheader(result["Color Statement"])
            
            st.markdown("**Suggested Shirt Colors:**")
            colors = [c.strip() for c in str(result["Suggested Shirt Colors"]).split(",")]
            linked_colors = [create_link(c) for c in colors]
            st.markdown(", ".join(linked_colors))
    else:
        st.warning("No exact match found! Please try different input values.")

# ---------------------------
# UI Improvement Feedback Section
# ---------------------------
#st.markdown("### UI Improvement Feedback")
#st.markdown("1. Does the swatch layout for Skin Color clearly display each option without overlapping?")
#st.markdown("2. Is the image display for the Exclusive Color Group helpful for your selection?")
#st.markdown("3. Are the clickable product links correctly directing to your Shopify store?")
