import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px

from utils.data_loader import charger_donnees, sidebar_filtres, formater_fcfa

st.set_page_config(page_title="Analyse par pays", page_icon="🌍", layout="wide")
st.title("🌍 Analyse par pays")

df = charger_donnees()
df_f = sidebar_filtres(df)

if df_f.empty:
    st.warning("Aucune transaction ne correspond aux filtres sélectionnés.")
    st.stop()

par_pays = df_f.groupby("pays", as_index=False).agg(
    volume_fcfa=("montant_fcfa", "sum"),
    nb_transactions=("transaction_id", "count"),
    montant_moyen=("montant_fcfa", "mean"),
    taux_reussite=("statut", lambda s: (s == "Réussi").mean() * 100),
).sort_values("volume_fcfa", ascending=False)

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Volume échangé par pays")
    fig = px.bar(par_pays, x="pays", y="volume_fcfa", color="pays",
                 labels={"volume_fcfa": "Volume (FCFA)", "pays": ""})
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Nombre de transactions")
    fig2 = px.pie(par_pays, names="pays", values="nb_transactions", hole=0.45)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Zone urbaine vs rurale par pays")
zone = df_f.groupby(["pays", "zone"], as_index=False)["montant_fcfa"].sum()
fig3 = px.bar(zone, x="pays", y="montant_fcfa", color="zone", barmode="group",
              labels={"montant_fcfa": "Volume (FCFA)", "pays": ""})
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Détail chiffré par pays")
tableau = par_pays.copy()
tableau["volume_fcfa"] = tableau["volume_fcfa"].apply(formater_fcfa)
tableau["montant_moyen"] = tableau["montant_moyen"].apply(formater_fcfa)
tableau["taux_reussite"] = tableau["taux_reussite"].round(1).astype(str) + " %"
tableau.columns = ["Pays", "Volume total", "Nb transactions", "Montant moyen", "Taux de réussite"]
st.dataframe(tableau, use_container_width=True, hide_index=True)
