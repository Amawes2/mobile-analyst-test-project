"""Chargement et préparation des données, mis en cache par Streamlit."""

import os
import pandas as pd
import streamlit as st

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mobile_money_transactions.csv")


@st.cache_data(show_spinner="Chargement des données...")
def charger_donnees() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["mois"] = df["date"].dt.to_period("M").astype(str)
    df["annee"] = df["date"].dt.year
    df["jour_semaine"] = df["date"].dt.day_name()
    df["montant_net_fcfa"] = df["montant_fcfa"] + df["frais_fcfa"]
    return df


def appliquer_filtres(df: pd.DataFrame, pays=None, providers=None, date_min=None, date_max=None,
                       statuts=None) -> pd.DataFrame:
    out = df.copy()
    if pays:
        out = out[out["pays"].isin(pays)]
    if providers:
        out = out[out["provider"].isin(providers)]
    if date_min is not None and date_max is not None:
        out = out[(out["date"] >= pd.Timestamp(date_min)) & (out["date"] <= pd.Timestamp(date_max))]
    if statuts:
        out = out[out["statut"].isin(statuts)]
    return out


def sidebar_filtres(df: pd.DataFrame) -> pd.DataFrame:
    """Filtres partagés (mêmes clés de session_state) affichés sur chaque page."""
    st.sidebar.header("🔎 Filtres")

    pays_options = sorted(df["pays"].unique())
    pays_sel = st.sidebar.multiselect("Pays", pays_options, default=pays_options, key="filtre_pays")

    provider_options = sorted(df["provider"].unique())
    provider_sel = st.sidebar.multiselect("Opérateur", provider_options, default=provider_options,
                                           key="filtre_providers")

    date_min, date_max = df["date"].min().date(), df["date"].max().date()
    plage = st.sidebar.date_input("Période", value=(date_min, date_max), min_value=date_min,
                                   max_value=date_max, key="filtre_dates")
    if isinstance(plage, tuple) and len(plage) == 2:
        d_min, d_max = plage
    else:
        d_min, d_max = date_min, date_max

    statut_options = sorted(df["statut"].unique())
    statut_sel = st.sidebar.multiselect("Statut", statut_options, default=statut_options, key="filtre_statuts")

    st.sidebar.caption("Les filtres s'appliquent à toutes les pages du tableau de bord.")

    return appliquer_filtres(df, pays=pays_sel, providers=provider_sel, date_min=d_min, date_max=d_max,
                              statuts=statut_sel)


def formater_fcfa(valeur: float) -> str:
    if valeur >= 1_000_000_000:
        return f"{valeur / 1_000_000_000:,.2f} Md FCFA".replace(",", " ")
    if valeur >= 1_000_000:
        return f"{valeur / 1_000_000:,.1f} M FCFA".replace(",", " ")
    if valeur >= 1_000:
        return f"{valeur / 1_000:,.0f} k FCFA".replace(",", " ")
    return f"{valeur:,.0f} FCFA".replace(",", " ")
