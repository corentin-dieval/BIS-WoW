import streamlit as st
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import json
import random


# Connexion à la base de données (optionnel)
# engine = create_engine('postgresql://user:password@localhost:5432/yourdb')
# df = pd.read_sql('select * from items', engine)

# Chargement des données depuis un CSV
df = pd.read_csv(Path('resources/Items WoW - Items.csv'))

with open(Path("resources/call_spec.json")) as file:
    class_data = json.load(file)

# # UI: Character creation
# st.title("WoW Best in Slot (BIS) Manager")
#
# st.header("Create a Character")
# character_name = st.text_input("Character Name")
character_class = st.selectbox("Choose Class", list(class_data.keys()))

if character_class:
    character_spec = st.selectbox("Choose Specialization", class_data[character_class]['spec'])

character_level = st.slider("Level", 1, 80, 70)
primary_profession = st.selectbox("Primary Profession",
                                  ["Alchemy", "Blacksmithing", "Enchanting", "Engineering", "Herbalism", "Tailoring",
                                   "Mining", "Skinner", "Fishing", "First Aid"])
secondary_profession = st.selectbox("Secondary Profession", [m for m in
                                                             ["Alchemy", "Blacksmithing", "Enchanting", "Engineering",
                                                              "Herbalism", "Tailoring",
                                                              "Mining", "Skinner", "Fishing", "First Aid"] if m != primary_profession])

# UI: BIS selection
st.header("Select Your Best in Slot (BIS) Gear")

slots = ["Head", "Shoulders", "Chest", "Legs", "Hands", "Feet", "Waist", "Wrist", "Neck", "Ring 1", "Ring 2",
         "Trinket 1", "Trinket 2", "Back",
         "Weapon 1", "Weapon 2"]
bis_selection = {}

df

for slot in slots:
    st.subheader(f"Select {slot} Slot Item")

    # Get armor type for the selected class
    armor_type = class_data[character_class]['armor_type']

    # Filter items based on class, armor type, and slot
    filtered_items = df[
        (df['Slot'] == slot)
        &
        (df['Armor Type'].str.lower().str.contains(armor_type.lower()) |
         df['Armor Type'].str.lower().isin(['accessories drops', 'trinket drops', 'weapons'])
         )
        ]

    item_choice = st.selectbox(f"Choose an item for {slot}", filtered_items['Item'])

    bis_selection[slot] = item_choice

# Display farming locations for selected BIS items
st.header("Where to Farm Your BIS Gear")
for slot, item in bis_selection.items():
    location = df[df['Item'] == item]['Dungeon'].values[0]
    st.write(f"{item} (Slot: {slot}) can be found in: {location}")


