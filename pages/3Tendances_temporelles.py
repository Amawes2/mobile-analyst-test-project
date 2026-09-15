import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px

from utils.data_loader import charger_donnees, sidebar_filtres

st.set_page_config(page_title="Tendances temporelles", page_icon="📈", layout="wide")
st.title("📈 Tendances temporelles")

df = charger_donnees()
df_f = sidebar_filtres(df)

if df_f.empty:
    st.warning("Aucune transaction ne correspond aux filtres sélectionnés.")
    st.stop()

st.subheader("Volume quotidien échangé")
quotidien = df_f.groupby("date", as_index=False)["montant_fcfa"].sum()
fig = px.line(quotidien, x="date", y="montant_fcfa", labels={"montant_fcfa": "Volume (FCFA)", "date": "Date"})
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Activité par heure de la journée")
    par_heure = df_f.groupby("heure", as_index=False)["transaction_id"].count()
    par_heure.columns = ["heure", "nombre"]
    fig2 = px.bar(par_heure, x="heure", y="nombre", labels={"heure": "Heure", "nombre": "Transactions"})
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Activité par jour de la semaine")
    ordre_jours = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    noms_fr = {"Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi", "Thursday": "Jeudi",
               "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"}
    par_jour = df_f.groupby("jour_semaine", as_index=False)["transaction_id"].count()
    par_jour.columns = ["jour_semaine", "nombre"]
    par_jour["jour_semaine"] = par_jour["jour_semaine"].map(noms_fr)
    par_jour["ordre"] = par_jour["jour_semaine"].map({v: i for i, v in enumerate(
        [noms_fr[j] for j in ordre_jours])})
    par_jour = par_jour.sort_values("ordre")
    fig3 = px.bar(par_jour, x="jour_semaine", y="nombre", labels={"jour_semaine": "", "nombre": "Transactions"})
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Saisonnalité mensuelle (toutes années confondues)")
df_f["mois_num"] = df_f["date"].dt.month
noms_mois = {1: "Jan", 2: "Fév", 3: "Mars", 4: "Avr", 5: "Mai", 6: "Juin",
             7: "Juil", 8: "Août", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc"}
par_mois = df_f.groupby("mois_num", as_index=False)["montant_fcfa"].sum()
par_mois["mois_nom"] = par_mois["mois_num"].map(noms_mois)
fig4 = px.bar(par_mois.sort_values("mois_num"), x="mois_nom", y="montant_fcfa",
              labels={"mois_nom": "", "montant_fcfa": "Volume (FCFA)"})
st.plotly_chart(fig4, use_container_width=True)

st.caption(
    "💡 Insight : les données simulent un pic d'activité en décembre (fêtes de fin d'année) "
    "et à la rentrée scolaire en septembre, avec un creux en août."
)
