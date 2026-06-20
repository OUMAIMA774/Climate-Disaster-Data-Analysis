import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Climate Events Dashboard", layout="wide")

# --- CSS Global et background image ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-attachment: fixed;
}
.overlay {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 50px;
    border-radius: 15px;
    text-align: center;
    margin: 30px;
}
h1, h2, h3 {
    color: #4B0082;
}
.stButton>button {
    background-color: #4B0082;
    color: white;
}
.metric-box {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- Chargement du dataset ---
df = pd.read_csv("data/global_climate_events_economic_impact_2020_2025.csv", sep=';')

# --- Texte de bienvenue dynamique ---
st.markdown("""
<div class="overlay">
    <h1>Bienvenue sur Climate Events Dashboard 🌍</h1>
    <p>Explorez les données sur les événements climatiques mondiaux et leur impact économique de 2020 à 2025.</p>
</div>
""", unsafe_allow_html=True)

# --- Cartes métriques ---
total_events = df.shape[0] # 0 : pour dire combien de ligne et 1 : pour dire combien de colonnes
total_victime = int(df['total_casualties'].sum())
total_impact = int(df['economic_impact_million_usd'].sum())

col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='metric-box'><h3>Nombre total d'événements</h3><h2>{total_events}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'><h3>Nombre total de victimes</h3><h2>{total_victime}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'><h3>Impact économique</h3><h3>{total_impact} (M $ USD)</h3></div>", unsafe_allow_html=True)

img1 = Image.open("images/feux.jpeg").resize((500, 350))
img2 = Image.open("images/secheresse.jpg").resize((500, 350))

col1, col2 = st.columns(2)
with col1:
    st.image(img1, caption="Impact climatique mondial")
with col2:
    st.image(img2, caption="Événements climatiques")

st.markdown("""
<div class="overlay">
    <h1>Chaque événement compte – Découvrez leur impact</h1>
</div>
""", unsafe_allow_html=True)
