import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px

from utils.data_loader import charger_donnees, sidebar_filtres, formater_fcfa

st.set_page_config(page_title="Comparatif opérateurs", page_icon="📊", layout="wide")
st.title("📊 Comparatif des opérateurs")

df = charger_donnees()
df_f = sidebar_filtres(df)

if df_f.empty:
    st.warning("Aucune transaction ne correspond aux filtres sélectionnés.")
    st.stop()

par_provider = df_f.groupby("provider", as_index=False).agg(
    volume_fcfa=("montant_fcfa", "sum"),
    nb_transactions=("transaction_id", "count"),
    frais_moyen_pct=("frais_fcfa", lambda s: (s / df_f.loc[s.index, "montant_fcfa"]).replace([float("inf")], 0).mean() * 100),
    taux_reussite=("statut", lambda s: (s == "Réussi").mean() * 100),
).sort_values("volume_fcfa", ascending=False)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Volume échangé par opérateur")
    fig = px.bar(par_provider, x="provider", y="volume_fcfa", color="provider",
                 labels={"volume_fcfa": "Volume (FCFA)", "provider": ""})
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Frais moyen appliqué (% du montant)")
    fig2 = px.bar(par_provider.sort_values("frais_moyen_pct"), x="frais_moyen_pct", y="provider",
                  orientation="h", color="provider",
                  labels={"frais_moyen_pct": "Frais moyen (%)", "provider": ""})
    fig2.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Évolution mensuelle du volume par opérateur")
evo = df_f.groupby(["mois", "provider"], as_index=False)["montant_fcfa"].sum()
fig3 = px.line(evo, x="mois", y="montant_fcfa", color="provider", markers=True,
               labels={"montant_fcfa": "Volume (FCFA)", "mois": "Mois"})
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Fiabilité par opérateur")
fig4 = px.bar(par_provider.sort_values("taux_reussite"), x="taux_reussite", y="provider", orientation="h",
              color="provider", labels={"taux_reussite": "Taux de réussite (%)", "provider": ""})
fig4.update_layout(showlegend=False, margin=dict(t=10, b=10))
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Tableau comparatif")
tableau = par_provider.copy()
tableau["volume_fcfa"] = tableau["volume_fcfa"].apply(formater_fcfa)
tableau["frais_moyen_pct"] = tableau["frais_moyen_pct"].round(2).astype(str) + " %"
tableau["taux_reussite"] = tableau["taux_reussite"].round(1).astype(str) + " %"
tableau.columns = ["Opérateur", "Volume total", "Nb transactions", "Frais moyen", "Taux de réussite"]
st.dataframe(tableau, use_container_width=True, hide_index=True)

st.caption(
    "💡 Insight : Wave se distingue historiquement par des frais nettement inférieurs à la moyenne du marché, "
    "un positionnement qui explique sa croissance rapide dans les données simulées."
)
