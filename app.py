from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the dataset
csv_file = "demography_all_possible_combinations.csv"
df = pd.read_csv(csv_file)

@app.route('/')
def home():
    return render_template("index.html")  # This will load the frontend form

@app.route('/get_style', methods=['POST'])
def get_style():
    data = request.json

    # Get user input
    skin_tone = data.get("skin_tone", "").strip().lower()
    skin_color = data.get("skin_color", "").strip().lower()
    hair_color = data.get("hair_color", "").strip().lower()
    eye_color = data.get("eye_color", "").strip().lower()
    personality = data.get("personality", "").strip().lower()
    color_group = data.get("color_group", "").strip().lower()
    style_word = data.get("style_word", "").strip().lower()

    # Filter dataset
    filtered_df = df[
        (df["Skin Tone"].str.lower() == skin_tone) &
        (df["Skin Color"].str.lower() == skin_color) &
        (df["Hair Color"].str.lower() == hair_color) &
        (df["Eye Color"].str.lower() == eye_color) &
        (df["Personality"].str.lower() == personality) &
        (df["Exclusive Color Group Name"].str.lower() == color_group) &
        (df["Style in One Word"].str.lower() == style_word)
    ]

    if not filtered_df.empty:
        result = filtered_df.iloc[0][[
            "Style Persona", "Best Occasions for This Color", "Power Statement",
            "Suggested Shirt Colors", "Suggested Pant Colors", "Top Clothing Priority",
            "Celebrity Wardrobe Inspiration"
        ]].to_dict()
        return jsonify(result)
    else:
        return jsonify({"error": "No exact match found! Try different input values."})

if __name__ == '__main__':
    app.run(debug=True)
