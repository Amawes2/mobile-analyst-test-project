import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px

from utils.data_loader import charger_donnees, sidebar_filtres

st.set_page_config(page_title="Segmentation clients", page_icon="👥", layout="wide")
st.title("👥 Segmentation des clients")

df = charger_donnees()
df_f = sidebar_filtres(df)

if df_f.empty:
    st.warning("Aucune transaction ne correspond aux filtres sélectionnés.")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Par genre")
    rep = df_f["genre_client"].value_counts().reset_index()
    rep.columns = ["genre", "nombre"]
    fig = px.pie(rep, names="genre", values="nombre", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Par tranche d'âge")
    rep2 = df_f["tranche_age"].value_counts().reset_index()
    rep2.columns = ["tranche_age", "nombre"]
    ordre = ["18-25", "26-35", "36-45", "46-60", "60+"]
    rep2["ordre"] = rep2["tranche_age"].map({v: i for i, v in enumerate(ordre)})
    rep2 = rep2.sort_values("ordre")
    fig2 = px.bar(rep2, x="tranche_age", y="nombre", labels={"tranche_age": "", "nombre": "Transactions"})
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.subheader("Par zone")
    rep3 = df_f["zone"].value_counts().reset_index()
    rep3.columns = ["zone", "nombre"]
    fig3 = px.pie(rep3, names="zone", values="nombre", hole=0.45)
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Canal utilisé selon la zone (urbain / rural)")
canal_zone = df_f.groupby(["zone", "canal"], as_index=False)["transaction_id"].count()
canal_zone.columns = ["zone", "canal", "nombre"]
fig4 = px.bar(canal_zone, x="zone", y="nombre", color="canal", barmode="group",
              labels={"zone": "", "nombre": "Transactions"})
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Type de transaction selon la tranche d'âge")
type_age = df_f.groupby(["tranche_age", "type_transaction"], as_index=False)["transaction_id"].count()
type_age.columns = ["tranche_age", "type_transaction", "nombre"]
fig5 = px.bar(type_age, x="tranche_age", y="nombre", color="type_transaction", barmode="stack",
              labels={"tranche_age": "", "nombre": "Transactions"},
              category_orders={"tranche_age": ["18-25", "26-35", "36-45", "46-60", "60+"]})
st.plotly_chart(fig5, use_container_width=True)

st.caption(
    "💡 Insight : le canal USSD reste dominant en zone rurale (accès limité aux smartphones/internet), "
    "tandis que l'application mobile progresse fortement en zone urbaine."
)
