import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

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

def skin_color_selector():
    st.markdown("### Select Your Skin Color")
    chosen_color = st.session_state.get("skin_color", list(skin_colors.keys())[0])
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
# Mapping for Exclusive Color Group images (for outputs)
# ---------------------------
color_group_images = {
    "Velvet Ember": "images/Velvet Ember.jpg",
    "Earthy Espresso": "images/Earthy Espresso.jpg",
    "Indigo Nomad": "images/Indigo Nomad.jpg",
    "Midnight Commander": "images/Midnight Commander.jpg",
    "Evergreen Chic": "images/Evergreen Chic.jpg",
    "Sun-Kissed Bliss": "images/Sun-Kissed Bliss.jpg",
    "Peachy Whimsy": "images/Peachy Whimsy.jpg",
    "Golden Zest": "images/Golden Zest.jpg",
    "Celestial Sapphire": "images/Celestial Sapphire.jpg",
    "Frosted Elegance": "images/Frosted Elegance.jpg"
}

# ---------------------------
# Mapping for Favourite Season images (for input)
# ---------------------------
favourite_season_images = {
    "Spring": "images/Spring.jpg",
    "Summer": "images/Summer.jpg",
    "Autumn": "images/Autumn.jpg",
    "Winter": "images/Winter.jpg"
}

# ---------------------------
# Load Data: Mapping and Product URL mapping
# ---------------------------
mapping_file = "demography_shirt_optimized.csv"
df = pd.read_csv(mapping_file)

product_mapping_file = "Fabric Crosswalk_ColorQuiz_URL.csv"
product_df = pd.read_csv(product_mapping_file)

# ---------------------------
# Function to create clickable product link(s)
# ---------------------------
def create_link(color):
    url = product_df.loc[product_df["Item Name ORGANO"] == color, "URL"]
    if not url.empty:
        return f"[{color}]({url.values[0]})"
    else:
        return color

# ---------------------------
# Function to generate PDF from recommendation data using FPDF
# ---------------------------
def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Your Style Recommendation", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Style Persona: {result['Style Persona']}", ln=True)
    pdf.cell(0, 10, f"Celebrity Wardrobe Inspiration: {result['Celebrity Wardrobe Inspiration']}", ln=True)
    pdf.cell(0, 10, f"Top Clothing Priority: {result['Top Clothing Priority']}", ln=True)
    pdf.ln(5)
    for i in range(1, 4):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Color Group {i}: {result[f'Exclusive Color Group Name {i}']}", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Color Statement {i}: {result[f'Color Statement {i}']}", ln=True)
        pdf.cell(0, 10, f"Suggested Shirt Color {i}: {result[f'Suggested Shirt Color {i}']}", ln=True)
        pdf.cell(0, 10, f"Styling Tip {i}: {result[f'Styling Tip {i}']}", ln=True)
        pdf.ln(5)
    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output

# ---------------------------
# Function to save submission (name & email) to a local CSV file
# ---------------------------
def save_submission(name, email):
    submission = pd.DataFrame({"Name": [name], "Email": [email]})
    try:
        old_df = pd.read_csv("submissions.csv")
        new_df = pd.concat([old_df, submission], ignore_index=True)
    except FileNotFoundError:
        new_df = submission
    new_df.to_csv("submissions.csv", index=False)

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
    st.markdown("### Favourite Season")
    selected_favourite_season = st.selectbox("Choose your Favourite Season:", list(favourite_season_images.keys()),
                                               help="Select the season that best represents your style preference.")
    st.image(favourite_season_images[selected_favourite_season], width=400)
    
    style_word = st.radio("Style Word:", ["Classic", "Minimalist", "Bold & Expressive", "Relaxed & Effortless", "Timeless", "Fashion-Forward"],
                          help="Select the word that best describes your style.")
    clothing_occasion = st.radio("Clothing Occasion:", [
        "Work Attire", "Special Occasions", "Vacations", "Formal Events", 
        "Everyday Wear", "Gifts", "Travel", "Seasonal Changes"
    ], help="Select the occasion for which you need a style recommendation.")

# ---------------------------
# Process and Display the Recommendation
# ---------------------------
if st.button("Get My Color Psyche"):
    filtered_df = df[
        (df["Skin Color"] == selected_skin_color) &
        (df["Gender"] == gender) &
        (df["Hair Color"] == hair_color) &
        (df["Favourite Season"] == selected_favourite_season) &
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
        st.write(result["Celebrity Wardrobe Inspiration"])
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
                
                st.markdown(f"### {ecg}")
                if ecg in color_group_images:
                    st.image(color_group_images[ecg], width=200)
                st.markdown("**Color Statement:**")
                st.write(cs)
                st.markdown("**Suggested Shirt Color:**")
                colors = [c.strip() for c in str(ssc).split(",")]
                linked_colors = [create_link(c) for c in colors]
                st.write(", ".join(linked_colors))
                st.markdown("**Styling Tip:**")
                st.write(st_tip)
        
        # Save the recommendation result in session state for PDF generation
        st.session_state["recommendation_result"] = result
        
    else:
        st.warning("No exact match found! Please try different input values.")

# ---------------------------
# PDF Download & Submission Form
# ---------------------------
if "recommendation_result" in st.session_state:
    st.markdown("---")
    st.subheader("Receive Your Recommendation PDF")
    name_input = st.text_input("Enter your Name", help="Your name will be used in the PDF.")
    email_input = st.text_input("Enter your Email", help="Your email will be used to send you the PDF and record your submission.")
    
    if st.button("Download PDF & Submit"):
        if name_input and email_input:
            pdf_output = generate_pdf(st.session_state["recommendation_result"])
            save_submission(name_input, email_input)
            st.download_button(
                label="Download Your PDF",
                data=pdf_output,
                file_name="StyleRecommendation.pdf",
                mime="application/pdf"
            )
            st.success("Your submission has been saved and your PDF is ready for download!")
        else:
            st.error("Please enter both your name and email to proceed.")
