import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from pathlib import Path



from analysis_data import load_analysis_data

LOGO_PATH = Path(__file__).parent / "assets" / "logo-tete-maure.svg"
st.set_page_config(page_title="Soldats corses", page_icon=LOGO_PATH, layout="wide")

if LOGO_PATH.exists():
	st.logo(str(LOGO_PATH))

data = load_analysis_data()
viz = data["viz"]
resume_departements = data["resume_departements"]
par_annee = data["par_annee"].sort_values("annee_deces")
synthese = data["synthese"]

st.title("Soldats corses morts pour la France")
st.caption("Synthèse des données présentes dans soldats_corse.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Soldats recensés", f"{len(viz):,}")
col2.metric("Conflits", int(viz["conflit"].nunique()))
col3.metric("Dates manquantes", f"{viz['date_deces'].isna().sum():,}")

st.subheader("Nombre de morts par année")
st.line_chart(
	par_annee.set_index("annee_deces")["soldats"],
	x_label="Année",
	y_label="Nombre de morts",
)





left, right = st.columns(2)
with left:
	st.subheader("Répartition par appartement de naissance")
	st.bar_chart(
		resume_departements.head(10).set_index("departement")["soldats"])
	
with right:
	st.subheader("Tableau de synthèse")
	st.dataframe(synthese, hide_index=True, use_container_width=True)


