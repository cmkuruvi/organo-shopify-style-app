import streamlit as st
import pandas as pd

# ---------------------------
# Custom CSS: Use Montserrat font & style output messaging
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
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Load the mapping data
# ---------------------------
mapping_file = "demography_shirt.csv"  # Replace with your actual file name
df = pd.read_csv(mapping_file)

# Optional: Load product URL mapping for suggested colors
# Assumes a CSV with columns "Color Name" and "Product URL"
product_mapping_file = "Fabric Crosswalk_ColorQuiz_URL.csv"  # Replace with your actual file name
product_df = pd.read_csv(product_mapping_file)

# ---------------------------
# App Header and Image
# ---------------------------
st.image("2.png", width=200)
st.title("Discover Your Color Psyche")

# Sidebar for additional customization (if needed)
with st.sidebar:
    st.header("Customize Your Experience")
    st.markdown("Adjust any settings or view UI feedback questions below.")

# ---------------------------
# Collecting User Inputs
# ---------------------------
st.header("Tell us about yourself:")

# Use two columns for a balanced layout
col1, col2 = st.columns(2)

with col1:
    gender = st.radio("Gender:", ["Male", "Female", "Other"])  # Adjust options as needed
    # Use a color picker for skin color input
    skin_color = st.color_picker("Select Your Skin Color (HEX):", "#ffffff")
    hair_color = st.radio("Hair Color:", ["Blonde", "Brown", "Black", "Red", "Other"])

with col2:
    # Exclusive Color Group with a note for swatch-based selection.
    st.markdown("**Exclusive Color Group Name:**")
    st.info("For a swatch selection, you can upload your palette image to GitHub and link it here.")
    color_group = st.selectbox("Choose your Color Group:", 
                               ["Velvet Ember", "Earthy Espresso", "Indigo Nomad", "Midnight Commander",
                                "Evergreen Chic", "Sun-Kissed Bliss", "Peachy Whimsy", "Golden Zest",
                                "Celestial Sapphire", "Frosted Elegance"])
    style_word = st.radio("Style Word:", ["Classic", "Minimalist", "Bold & Expressive", "Relaxed & Effortless"])
    clothing_occasion = st.radio("Clothing Occasion:", ["Casual", "Formal", "Party", "Work", "Other"])

# ---------------------------
# Process and Display the Recommendation
# ---------------------------
if st.button("Get My Color Psyche"):
    # Filter the dataframe based on user inputs using your new column names
    filtered_df = df[
        (df["Gender"] == gender) &
        (df["Skin Color"] == skin_color) &
        (df["Hair Color"] == hair_color) &
        (df["Exclusive Color Group Name"] == color_group) &
        (df["Style Word"] == style_word) &
        (df["Clothing Occasion"] == clothing_occasion)
    ]
    
    if not filtered_df.empty:
        result = filtered_df.iloc[0][[
            "Style Persona", "Celebrity Wardrobe Inspiration", "Top Clothing Priority", 
            "Color Statement", "Suggested Shirt Colors", "Suggested Suit Colors", "Suggested Pant Colors"
        ]]
        st.success("Here’s your personalized style recommendation!")
        
        # Function to convert suggested colors to clickable Shopify links if mapping is found
        def create_link(color):
            url = product_df.loc[product_df["Item Name ORGANO"] == color, "URL"]
            if not url.empty:
                return f"[{color}]({url.values[0]})"
            else:
                return color
        
        st.markdown("<div class='output'>", unsafe_allow_html=True)
        for key, value in result.items():
            # For product suggestions, assume comma-separated color names
            if key in ["Suggested Shirt Colors", "Suggested Suit Colors", "Suggested Pant Colors"]:
                colors = [c.strip() for c in str(value).split(",")]
                linked_colors = [create_link(c) for c in colors]
                st.markdown(f"**{key}:** " + ", ".join(linked_colors))
            else:
                st.markdown(f"**{key}:** {value}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No exact match found! Please try different input values.")
