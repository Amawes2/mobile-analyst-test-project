import os
import pandas as pd
import plotly.express as px


ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, "data", "mobile_money_transactions.csv")
OUT_DIR = os.path.join(ROOT, "artifacts", "visuals")
os.makedirs(OUT_DIR, exist_ok=True)


def charger():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"]) 
    df["mois"] = df["date"].dt.to_period("M").astype(str)
    return df


def formater_fcfa(valeur: float) -> str:
    if valeur >= 1_000_000_000:
        return f"{valeur / 1_000_000_000:,.2f} Md FCFA".replace(",", " ")
    if valeur >= 1_000_000:
        return f"{valeur / 1_000_000:,.1f} M FCFA".replace(",", " ")
    if valeur >= 1_000:
        return f"{valeur / 1_000:,.0f} k FCFA".replace(",", " ")
    return f"{valeur:,.0f} FCFA".replace(",", " ")


def main():
    df = charger()

    par_provider = df.groupby("provider", as_index=False).agg(
        volume_fcfa=("montant_fcfa", "sum"),
        nb_transactions=("transaction_id", "count"),
        taux_reussite=("statut", lambda s: (s == "Réussi").mean() * 100),
    ).sort_values("volume_fcfa", ascending=False)

    # Volume par opérateur
    fig = px.bar(par_provider, x="provider", y="volume_fcfa", color="provider",
                 labels={"volume_fcfa": "Volume (FCFA)", "provider": ""})
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10))
    fig.write_image(os.path.join(OUT_DIR, "volume_par_operateur.png"), width=1200, height=600)

    # Taux de réussite
    fig2 = px.bar(par_provider.sort_values("taux_reussite"), x="taux_reussite", y="provider",
                  orientation="h", color="provider", labels={"taux_reussite": "Taux de réussite (%)", "provider": ""})
    fig2.update_layout(showlegend=False, margin=dict(t=10, b=10))
    fig2.write_image(os.path.join(OUT_DIR, "taux_reussite_operateur.png"), width=1200, height=600)

    # Évolution mensuelle totale (toutes providers)
    evo = df.groupby("mois", as_index=False)["montant_fcfa"].sum()
    fig3 = px.area(evo, x="mois", y="montant_fcfa", labels={"mois": "Mois", "montant_fcfa": "Volume (FCFA)"})
    fig3.update_layout(margin=dict(t=10, b=10))
    fig3.write_image(os.path.join(OUT_DIR, "evolution_mensuelle.png"), width=1400, height=600)

    # Table CSV et HTML
    out_table_csv = os.path.join(OUT_DIR, "tableau_comparatif.csv")
    par_provider["volume_fcfa"] = par_provider["volume_fcfa"].apply(formater_fcfa)
    par_provider.to_csv(out_table_csv, index=False)

    print("Visuels générés dans:", OUT_DIR)


if __name__ == "__main__":
    main()
