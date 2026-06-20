import streamlit as st
import pandas as pd

st.set_page_config(page_title="Exploration du Dataset", layout="wide")

# --- Background CSS ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1350&q=80");
    background-size: cover;
    background-attachment: fixed;
}
.stDataFrame, .stTable {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 10px;
}
h1, h2, h3 {
    color: #4B0082;
}
</style>
""", unsafe_allow_html=True)

st.title("Exploration du Dataset")

# --- Chargement du dataset ---
df = pd.read_csv("data/global_climate_events_economic_impact_2020_2025.csv", sep=';')

# --- Filtres dynamiques ---
years = sorted(df['year'].unique())
selected_year = st.selectbox("Sélectionner une année :", years)
df_filtered = df[df['year'] == selected_year]

# --- Aperçu des données ---
st.header(f"Aperçu des données pour {selected_year}")
st.write("5 premières lignes (qui correspondent aux 5 premières dates) :")
st.dataframe(df_filtered.head()) # par defaut on donne 5 lignes , on peut specifer le nombre qu'on veut . exemple : df.head(4)

st.write("5 dernières lignes (qui correspondent aux 5 dernières dates) :")
st.dataframe(df_filtered.tail())

st.write("5 lignes aléatoires :")
st.dataframe(df_filtered.sample(5))

# --- Caractéristiques globales ---
st.header("Caractéristiques du dataset")
st.write("Taille du dataset (lignes, colonnes) :", df.shape)

# --- Tableau récapitulatif combiné ---
summary = []

for col in df.columns:
    summary.append({
        "Colonne": col,
        "Type de variable": df[col].dtype,
        "Valeurs non nulles": df[col].notnull().sum(),
        "Valeurs uniques": df[col].nunique(),
        "Valeurs manquantes": df[col].isnull().sum()
    })

summary_df = pd.DataFrame(summary)

# --- Affichage dans Streamlit ---
st.write("Liste des colonnes, de leur type et du nombre des valeurs non mulles, uniques et manquantes :")
st.dataframe(summary_df)

# --- Optionnel : statistiques globales ---
st.write("**Nombre total de valeurs manquantes :**", df.isnull().sum().sum())

# Nombre de doublons
num_duplicates = df.duplicated().sum()
st.write("**Nombre de doublons :**", num_duplicates)

# Aperçu des doublons
st.write("Aperçu des doublons (s’il y en a) :")
if num_duplicates > 0:
    st.dataframe(df[df.duplicated()])
else:
    st.info("Aucun doublon détecté ✅")

st.write("Répartition des types d'événements climatiques :")
st.dataframe(df['event_type'].value_counts())

# --- Statistiques descriptives détaillées ---
st.header("Statistiques descriptives")
num = df.select_dtypes(include='number')

st.subheader("Statistiques globales pour les colonnes numériques")
st.dataframe(df.describe())

