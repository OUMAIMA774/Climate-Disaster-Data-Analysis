import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualisation des données", layout="wide")

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
</style>
""", unsafe_allow_html=True)

st.title("Visualisation des données")

# --- Chargement du dataset ---
df = pd.read_csv("data/global_climate_events_economic_impact_2020_2025.csv", sep=';')

# --- Filtre par année ---
years = sorted(df['year'].unique())
selected_years = st.multiselect("Choisir les années à afficher :", years, default=years[:6])
df_filtered = df[df['year'].isin(selected_years)]

# --- 1. Nombre d'événements par année ---
events_per_year = df_filtered.groupby('year')['event_type'].count().reset_index()
fig1 = px.line(events_per_year, x='year', y='event_type', markers=True,
               title="Nombre d'événements climatiques par année")
st.plotly_chart(fig1, use_container_width=True)

# --- 2. Impact économique total par année ---
impact_per_year = df_filtered.groupby('year')['economic_impact_million_usd'].sum().reset_index()
fig2 = px.bar(impact_per_year, x='year', y='economic_impact_million_usd',
              title="Impact économique total par année (millions USD)")
st.plotly_chart(fig2, use_container_width=True)

# --- 4. Impact économique moyen par type d'événement ---
impact_by_event = df_filtered.groupby('event_type')['economic_impact_million_usd']\
                             .mean().sort_values(ascending=False).reset_index()
fig4 = px.bar(impact_by_event, x='event_type', y='economic_impact_million_usd',
              title="Impact économique moyen par type d'événement")
st.plotly_chart(fig4, use_container_width=True)

# --- 5. Boxplot impact par type d'événement ---
fig5 = px.box(df_filtered, x='event_type', y='economic_impact_million_usd',
              title="Répartition de l'impact économique par type d'événement")
st.plotly_chart(fig5, use_container_width=True)

# --- 6. Scatter plot population affectes vs impact ---
fig6 = px.scatter(df_filtered, x='affected_population', y='economic_impact_million_usd',
                  color='event_type', title="Impact économique vs la population affectée")
st.plotly_chart(fig6, use_container_width=True)

# --- 7. Heatmap corrélation avec valeurs ---
# corr = num.corr()
corr = df_filtered.corr(numeric_only=True)
fig7 = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale='RdBu_r',
    zmin=-1,
    zmax=1,
    labels=dict(x="Variables", y="Variables", color="Corrélation"),
    title="Matrice de corrélation des variables numériques",
    width=800,   # largeur
    height=800   # hauteur
)


st.plotly_chart(fig7, use_container_width=True)



# --- 8. Heatmap du temps de réponse moyen par pays et année ---
st.header("Heatmap du temps de réponse moyen par pays et année")
# Grouper les données filtrées par pays et année
response_by_country_year = (
    df_filtered.groupby(['country', 'year'])['response_time_hours']
    .mean()
    .reset_index()
)

# Créer la matrice pivot
pivot_data = response_by_country_year.pivot(
    index='country',
    columns='year',
    values='response_time_hours'
)
# ✅ Créer la Heatmap interactive avec valeurs visibles
fig = px.imshow(
    pivot_data,
    text_auto=".1f",  # afficher les valeurs arrondies à 1 décimale
    color_continuous_scale='YlOrRd',
    title='Heatmap du Temps de Réponse par Pays et Année'
)

# Personnaliser le style
fig.update_layout(
    title={
        'text': 'Heatmap du Temps de Réponse par Pays et Année',
        'x': 0.5,
        'xanchor': 'center',
        'font': dict(size=18, color='black', family='Arial Black')
    },
    xaxis_title='Année',
    yaxis_title='Pays',
    xaxis=dict(tickangle=0),
    yaxis=dict(tickangle=0),
    height=700,
    margin=dict(l=100, r=100, t=100, b=100)
)

# Afficher la figure dans Streamlit
st.plotly_chart(fig, use_container_width=True)


