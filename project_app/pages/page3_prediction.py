import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# --- Style de fond ---
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

st.title("🌍 Modélisation de la sévérité des événements climatiques")

# --- Chargement du dataset ---
data = pd.read_csv("data/global_climate_events_economic_impact_2020_2025.csv", sep=';')

# --- Variables explicatives et cible ---
st.subheader("⚙️ Préparation des données")

X = data[["total_casualties", "infrastructure_damage_score"]]
y = data["severity"]
# pour introduire une variable categorielle , on procede comme suit :
# X = pd.get_dummies(data[["total_casualties", "infrastructure_damage_score", "event_type"]], drop_first=True)
# y = pd.get_dummies(data["severity"]) # avec ceci la colonne contient 0 ou 1 si la valeur lui correspond


# --- Division des données ---
test_size = st.slider("Proportion de test (%) :", 10, 40)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size/100, random_state=42
)

# test_size=0.2 : 20% des données seront utilisées pour le test, 80% pour l'entraînement
# random_state=42 : aléatoire et fixe les donnees , pour prendre les memes donnees pour le train et test a chaque execution


# --- Modèle de régression linéaire ---
model = LinearRegression()
model.fit(X_train, y_train)
# entraîne le modèle sur les données d'entraînement
# Le modèle apprend les coefficients (coef_ , les beta_i) et l'intercept (intercept_ , le beta_0) qui minimisent l'erreur quadratique

y_pred = model.predict(X_test) # utilise les coefficients appris pour prédire les valeurs de y

# --- Évaluation ---
mse = mean_squared_error(y_test, y_pred) # la moyenne des carres : MSE = (1/n) * somme((y_exact - y_pred)^2), ici n = 3000
                                         # càd l'erreur moyenne des prédictions est d'environ ±√(MSE) = RMSE (rmse = np.sqrt(mse))

rmse = np.sqrt(mse) # racine carree mse
r2 = r2_score(y_test, y_pred) # coefficient de détermination
                              # Exemple : R² = 0.61 signifie que le modèle explique 61% de la variance des données


st.subheader("📊 Évaluation du modèle")
col1, col2, col3 = st.columns(3)
col1.metric("**Erreur quadratique moyenne (MSE)**", f"{mse:.2f}")
col2.metric("**Racine de l'erreur quadratique moyenne (RMSE)**", f"{rmse:.2f}")
col3.metric("**Coefficient de détermination (R²)**", f"{r2:.2f}")
# --- Interprétation des coefficients ---
coeffs = pd.DataFrame({
    "Variable": X.columns,
    "Coefficient": model.coef_ # coef_ : attribut du model, contient les coeff des features
})

st.subheader("🧩 Coefficients du modèle")
st.dataframe(coeffs)
st.write(f"Valeur de base (intercept) : **{model.intercept_:.2f}**")


st.subheader("📈 Prédictions vs Valeurs réelles (Plotly)")

fig = px.scatter(
    x=y_test,
    y=y_pred,
    labels={"x": "Valeurs réelles", "y": "Valeurs prédites"},
    title="Régression linéaire : Prédictions vs Réelles",
    opacity=0.6
)

# Ajouter la diagonale y=x
fig.add_shape(
    type="line",
    x0=min(y_test), y0=min(y_test),
    x1=max(y_test), y1=max(y_test),
    line=dict(color="red", dash="dash")
)

st.plotly_chart(fig, use_container_width=True)


# --- Explication ---
st.info("""
💡 **Interprétation :**
- Le MSE mesure l’erreur moyenne quadratique entre les valeurs prédites et réelles.
- Le R² indique la proportion de la variance de `severity` expliquée par les variables explicatives.
- Les coefficients représentent l’impact de chaque variable sur la sévérité.
- Un nuage de points proche de la diagonale rouge signifie de bonnes prédictions.
""")
