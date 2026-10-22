import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from pathlib import Path


from analysis_data import load_analysis_data

BASE_COUVERTURE = "https://data.corsica/data-fair/api/v1/datasets/dispositif-de-couverture-ciblee-en-corse-points-dinteret/"

LOGO_PATH = Path(__file__).parent / "assets" / "logo-tete-maure.svg"
st.set_page_config(page_title="Soldats corses", page_icon=LOGO_PATH, layout="wide")

if LOGO_PATH.exists():
	st.logo(str(LOGO_PATH))

data = load_analysis_data()
viz = data["viz"]
resume_conflits = data["resume_conflits"]
resume_departements = data["resume_departements"]
synthese = data["synthese"]

st.title("Soldats corses morts pour la France")
st.caption("Synthèse des données présentes dans soldats_corse.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Soldats recensés", f"{len(viz):,}")
col2.metric("Conflits", int(viz["conflit"].nunique()))
col3.metric("Dates manquantes", f"{viz['date_deces'].isna().sum():,}")

st.subheader("Répartition par conflit")
st.bar_chart(resume_conflits.set_index("conflit")["soldats"])




left, right = st.columns(2)
with left:
	st.subheader("Principaux départements")
	st.bar_chart(
		resume_departements.head(10).set_index("departement")["soldats"]
	)
with right:
	st.subheader("Tableau de synthèse")
	st.dataframe(synthese, hide_index=True, use_container_width=True)


@st.cache_data(show_spinner="Récupération des données de couverture...")
def load_couverture_data():
	"""Récupère toutes les lignes du dataset utilisé dans le notebook."""
	url = f"{BASE_COUVERTURE}/lines"
	params = {"format": "json", "size": 10000}
	lignes = []

	while url:
		response = requests.get(url, params=params, timeout=60)
		response.raise_for_status()
		data = response.json()
		lignes.extend(data.get("results", []))
		url = data.get("next")
		params = None

	return pd.DataFrame(lignes)


st.divider()
st.title("Couverture réseau en Corse")
st.caption("Données récupérées depuis le dataset utilisé dans couverture-reseau.ipynb")

try:
	couverture = load_couverture_data()
	st.metric("Points recensés", f"{len(couverture):,}")
	st.dataframe(couverture, use_container_width=True, hide_index=True)

	colonnes_numeriques = couverture.select_dtypes(include="number").columns.tolist()
	if colonnes_numeriques:
		st.subheader("Répartition des points")
		colonne = st.selectbox("Variable numérique", colonnes_numeriques)
		st.bar_chart(couverture[colonne].value_counts().sort_index())
except requests.RequestException as erreur:
	st.error(f"Impossible de récupérer les données de couverture : {erreur}")