import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import plotly.express as px

from utils.data_loader import charger_donnees, sidebar_filtres, formater_fcfa

st.set_page_config(
    page_title="Mobile Money Analytics — Afrique de l'Ouest",
    page_icon="",
    layout="wide",
)

st.title(" Mobile Money Analytics — Afrique de l'Ouest")
st.caption(
    "Dashboard d'analyse des transactions mobile money (Orange Money, MTN MoMo, Wave, Moov Money, Free Money) "
    "— données synthétiques à but de démonstration."
)

df = charger_donnees()
df_f = sidebar_filtres(df)

if df_f.empty:
    st.warning("Aucune transaction ne correspond aux filtres sélectionnés.")
    st.stop()

# ----- KPIs -----
nb_transactions = len(df_f)
volume_total = df_f["montant_fcfa"].sum()
frais_total = df_f["frais_fcfa"].sum()
taux_reussite = (df_f["statut"] == "Réussi").mean() * 100
panier_moyen = df_f["montant_fcfa"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Transactions", f"{nb_transactions:,}".replace(",", " "))
c2.metric("Volume total échangé", formater_fcfa(volume_total))
c3.metric("Revenus (frais) générés", formater_fcfa(frais_total))
c4.metric("Taux de réussite", f"{taux_reussite:.1f} %")
c5.metric("Montant moyen / transaction", formater_fcfa(panier_moyen))

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Évolution mensuelle du volume échangé")
    evo = df_f.groupby("mois", as_index=False)["montant_fcfa"].sum()
    fig = px.area(evo, x="mois", y="montant_fcfa", labels={"mois": "Mois", "montant_fcfa": "Volume (FCFA)"})
    fig.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Répartition par type de transaction")
    rep = df_f["type_transaction"].value_counts().reset_index()
    rep.columns = ["type_transaction", "nombre"]
    fig2 = px.pie(rep, names="type_transaction", values="nombre", hole=0.45)
    fig2.update_layout(margin=dict(t=10, b=10), showlegend=True)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Volume par pays")
    par_pays = df_f.groupby("pays", as_index=False)["montant_fcfa"].sum().sort_values("montant_fcfa")
    fig3 = px.bar(par_pays, x="montant_fcfa", y="pays", orientation="h",
                  labels={"montant_fcfa": "Volume (FCFA)", "pays": ""})
    fig3.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Part de marché par opérateur (nombre de transactions)")
    par_provider = df_f["provider"].value_counts().reset_index()
    par_provider.columns = ["provider", "nombre"]
    fig4 = px.bar(par_provider.sort_values("nombre"), x="nombre", y="provider", orientation="h",
                  labels={"nombre": "Transactions", "provider": ""}, color="provider")
    fig4.update_layout(margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Aperçu des données filtrées")
st.dataframe(df_f.head(200), use_container_width=True, height=300)

st.info(
    " Utilise le menu de gauche pour naviguer vers les analyses détaillées : "
    "comparatif des opérateurs, tendances temporelles et segmentation clients."
)
