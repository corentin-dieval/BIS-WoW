import streamlit as st
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import json

# Connexion à la base de données (optionnel)
# engine = create_engine('postgresql://user:password@localhost:5432/yourdb')
# df = pd.read_sql('select * from items', engine)

# Chargement des données depuis un CSV
df = pd.read_csv(Path('resources/Items WoW - Items.csv'))

with open(Path("resources/call_spec.json")) as file:
    classes = json.load(file)

metiers = ["Alchimie", "Forgeron", "Enchantement", "Ingénieur", "Herboristerie", "Couture", "Mineur", "Peche", "Secourisme"]

# Interface utilisateur
st.title("Gestion des BIS pour WoW")

# Création d'un personnage
st.header("Créer un personnage")
nom_personnage = st.text_input("Nom du personnage")
classe_personnage = st.selectbox("Choisir la classe", list(classes.keys()))

if classe_personnage:
    specialisation_personnage = st.selectbox("Choisir la spécialisation", classes[classe_personnage])

niveau_personnage = st.slider("Niveau", 1, 80, 70)
metier_1 = st.selectbox("Premier métier", metiers)
metier_2 = st.selectbox("Second métier", [m for m in metiers if m != metier_1])

# Sélection de l'équipement BIS
st.header("Sélection de l'équipement BIS")

slots = ["Tête", "Épaules", "Torse", "Jambes", "Mains", "Pieds", "Ceinture", "Poignets", "Collier", "Anneau", "Bijou", "Cape", "Arme"]
bis_selection = {}

for slot in slots:
    st.subheader(f"Sélectionner {slot}")
    # Filtrer les items en fonction de la classe, spé, et slot
    filtered_items = df[(df['Class'] == classe_personnage) & (df['Spec'] == specialisation_personnage) & (df['Slot'] == slot)]
    item_choice = st.selectbox(f"Choisir un objet pour {slot}", filtered_items['ItemName'])
    bis_selection[slot] = item_choice

# Affichage des endroits où farmer les BIS sélectionnés
st.header("Où farmer vos BIS")
for slot, item in bis_selection.items():
    location = df[df['ItemName'] == item]['Dungeon'].values[0]
    st.write(f"{item} (Slot: {slot}) se trouve dans : {location}")

