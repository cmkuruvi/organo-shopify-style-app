import streamlit as st
import pandas as pd

# ---------------------------
# Custom CSS with brand colors, improved layout, and responsive design
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
    @media only screen and (max-width: 600px) {
       .swatch {
           width: 25px;
           height: 25px;
       }
       .swatch-label {
           font-size: 0.6em;
       }
       .output {
           padding: 10px;
       }
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

# Static image for the full skin color palette
skin_palette_image = "images/skin_palette.png"  # Update with actual image path

# ---------------------------
# Function for Skin Color Selection with HEX Preview & Reference Image
# ---------------------------
def skin_color_selector():
    st.markdown("### Select Your Skin Color")

    # Create radio button selection
    selected_skin_color = st.radio(
        label="Choose a skin color:",
        options=list(skin_colors.keys()),
        format_func=lambda x: x,  # Display option name
        horizontal=False
    )

    # Show a color preview box for the selected color
    st.markdown(
        f"<div style='width:50px; height:25px; background-color:{skin_colors[selected_skin_color]}; "
        f"border: 1px solid #000; display:inline-block; margin-left:10px;'></div>",
        unsafe_allow_html=True
    )

    # Display the static skin color palette image
    st.image(skin_palette_image, width=200, caption="Skin Color Palette")

    return selected_skin_color
# ---------------------------
# Mapping for Exclusive Color Group images (for outputs)
# ---------------------------
color_group_images = {
    "SUNNY RAY": "images/SUNNY RAY.jpg",
    "HARBOR TIDE": "images/HARBOR TIDE.jpg",
    "SUNNY SHINE": "images/SUNNY SHINE.jpg",
    "FORREST LAKE": "images/FORREST LAKE.jpg",
    "EMBER GLOW": "images/EMBER GLOW.jpg",
    "OBSIDIAN RAVEN": "images/OBSIDIAN RAVEN.jpg",
    "URBAN MYST": "images/URBAN MYST.jpg",
    "DUNE DUST": "images/DUNE DUST.jpg",
    "HARVEST AUTUMN": "images/HARVEST AUTUMN.jpg",
    "DUNE EARTH": "images/DUNE EARTH.jpg",
    "FROSTED SKY": "images/FROSTED SKY.jpg",
    "MOONLIT CLOUD": "images/MOONLIT CLOUD.jpg"
}

# ---------------------------
# Shopify Links Based on Gender Selection
# ---------------------------
shopify_links = {
    "SUNNY RAY": {
        "Male": "https://organolinen.com/products/mens-linen-shirt-yellow-sunny",
        "Female": "https://organolinen.com/products/sunny-women-linen-shirt-yellow"
    },
    "HARBOR TIDE": {
        "Male": "https://organolinen.com/products/mens-linen-shirt-blue-harbor",
        "Female": "https://organolinen.com/products/womens-linen-shirt-harbor-blue"
    },
    "SUNNY SHINE": {
        "Male": "https://organolinen.com/products/mens-linen-shirt-yellow-sunny",
        "Female": "https://organolinen.com/products/sunny-women-linen-shirt-yellow"
    },
    "FORREST LAKE": {
        "Male": "https://organolinen.com/products/mens-linen-shirt-green-forrest",
        "Female": "https://organolinen.com/products/mens-linen-shirt-green-forrest"
    },
    "EMBER GLOW": {
        "Male": "https://organolinen.com/products/mens-linen-shirt-ember-red",
        "Female": "https://organolinen.com/products/ladies-linen-shirt-ember"
    },
    "OBSIDIAN RAVEN": {
        "Male": "https://organolinen.com/products/mens-linen-heavy-shirt-raven",
        "Female": "https://organolinen.com/products/womens-heavy-linen-shirt-raven"
    },
    "URBAN MYST": {
        "Male": "https://organolinen.com/products/myst-pure-linen-shirt",
        "Female": "https://organolinen.com/products/myst-pure-linen-shirt"
    },
    "DUNE DUST": {
        "Male": "https://organolinen.com/products/dune-linen-shirt-men-tan",
        "Female": "https://organolinen.com/products/dune-linen-shirt-men-tan"
    },
    "HARVEST AUTUMN": {
        "Male": "https://organolinen.com/products/mens-pumpkin-harvest-linen-shirt",
        "Female": "https://organolinen.com/products/womens-pink-linen-shirt-harvest"
    },
    "DUNE EARTH": {
        "Male": "https://organolinen.com/products/dune-linen-shirt-men-tan",
        "Female": "https://organolinen.com/products/dune-linen-shirt-men-tan"
    },
    "FROSTED SKY": {
        "Male": "https://organolinen.com/products/mens-linen-shirt-blue-harbor",
        "Female": "https://organolinen.com/products/womens-linen-shirt-harbor-blue"
    },
    "MOONLIT CLOUD": {
        "Male": "https://organolinen.com/products/men-white-linen-shirt-cloud",
        "Female": "https://organolinen.com/products/womens-classic-white-linen-shirt"
    }
}

# ---------------------------
# Function to Get Correct Shopify Link
# ---------------------------
def get_shopify_link(color_group_name, gender):
    """Returns the correct Shopify link based on Gender and Color Group."""
    if color_group_name in shopify_links:
        if gender == "Female":
            return shopify_links[color_group_name]["Female"]
        else:  # Male & Unisex both use Male links
            return shopify_links[color_group_name]["Male"]
    return "#"  # Default link if color group is missing (shouldn't happen)
    
# ---------------------------
# Mapping for Favorite Season images (for input)
# ---------------------------
favorite_season_images = {
    "Spring": "images/Spring.jpg",
    "Summer": "images/Summer.jpg",
    "Autumn": "images/Autumn.jpg",
    "Winter": "images/Winter.jpg"
}

# ---------------------------
# Load Data: Mapping and Product URL mapping
# ---------------------------
mapping_file = "demography_shirt_final_updated.csv"
df = pd.read_csv(mapping_file)

product_mapping_file = "Fabric Crosswalk_ColorQuiz_URL.csv"
product_df = pd.read_csv(product_mapping_file)

# ---------------------------
# Function to create clickable product link(s) for a given color
# ---------------------------
def create_link(color):
    url = product_df.loc[product_df["Item Name ORGANO"] == color, "URL"]
    if not url.empty:
        return f"[{color}]({url.values[0]})"
    else:
        return color

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
    gender = st.radio("Gender:", ["Male", "Female", "Unisex"], help="Select your gender.")
    selected_skin_color = skin_color_selector()
    hair_color = st.radio("Hair Color:", ["Blonde", "Black", "Dark Brown", "Red", "Other"], help="Select your hair color.")

with col2:
    st.markdown("### Favorite Season")
    selected_favorite_season = st.selectbox("Choose your Favorite Season:", list(favorite_season_images.keys()),
                                              help="Select the season that best represents your style preference.")
    st.image(favorite_season_images[selected_favorite_season], width=400)
    
    style_word = st.radio("Style Word:", ["Classic", "Minimalist", "Bold & Expressive", "Relaxed & Effortless", "Timeless", "Fashion-Forward"],
                          help="Select the word that best describes your style.")
    clothing_occasion = st.radio("Clothing Occasion:", [
        "Boardroom to Brunch",
        "Big Moments, Big Style",
        "Wanderlust Wardrobe",
        "Wrapped with Love",
        "Weather-Ready Wear",
        "Effortlessly Chic"
    ], help="Select the occasion for which you need a style recommendation.")

# ---------------------------
# Process and Display the Recommendation
# ---------------------------
if st.button("Get My Color Psyche"):
    filtered_df = df[
        (df["Skin Color"] == selected_skin_color) &
        (df["Gender"] == gender) &
        (df["Hair Color"] == hair_color) &
        (df["Favorite Season"] == selected_favorite_season) &
        (df["Style Word"] == style_word) &
        (df["Clothing Occasion"] == clothing_occasion)
    ]
    
    if not filtered_df.empty:
        cols_to_extract = [
            "Style Persona", "Celebrity Wardrobe Inspiration", "Top Clothing Priority",
            "Exclusive Color Group Name 1", "Color Statement 1", "Suggested Shirt Color 1", "Styling Tip 1",
            "Exclusive Color Group Name 2", "Color Statement 2", "Suggested Shirt Color 2", "Styling Tip 2",
            "Exclusive Color Group Name 3", "Color Statement 3", "Suggested Shirt Color 3", "Styling Tip 3"
        ]
        result = filtered_df.iloc[0][cols_to_extract]
        st.success("Here’s your personalized style recommendation!")
        
        # Global recommendations
        st.subheader("Your Style Recommendation")
        st.markdown("***Style Persona:***")
        st.write(result["Style Persona"])
        st.markdown("***Celebrity Wardrobe Inspiration:***")
        st.subheader(result["Celebrity Wardrobe Inspiration"])
        st.markdown("***Top Clothing Priority:***")
        st.write(result["Top Clothing Priority"])
        
        st.markdown("---")
        st.subheader("Color Groups Recommendations")
        
        group_cols = st.columns(3)
        for i in range(1, 4):
            with group_cols[i-1]:
                ecg = result[f"Exclusive Color Group Name {i}"]
                cs = result[f"Color Statement {i}"]
                ssc = result[f"Suggested Shirt Color {i}"]
                st_tip = result[f"Styling Tip {i}"]

                # Get correct link based on Gender
                shopify_url = get_shopify_link(ecg, gender)

                # Display Exclusive Color Group Name as a clickable link
                st.markdown(f"### [{ecg}]({shopify_url})")
                
                    
                if ecg in color_group_images:
                    st.image(color_group_images[ecg], width=400)
                st.markdown("**Color Statement:**")
                st.write(cs)
                st.markdown("**Suggested Shirt Color:**")
                colors = [c.strip() for c in str(ssc).split(",")]
                linked_colors = [create_link(c) for c in colors]
                st.write(", ".join(linked_colors))
                st.markdown("**Styling Tip:**")
                st.write(st_tip)
    else:
        st.warning("No exact match found! Please try different input values.")
