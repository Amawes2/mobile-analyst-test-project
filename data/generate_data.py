"""
Génère un dataset synthétique mais réaliste de transactions mobile money
en Afrique de l'Ouest (2023-2025), avec des patterns crédibles :
- Wave moins chère (frais bas), forte croissance
- Orange Money / MTN MoMo dominants en volume historique
- Zones urbaines plus actives, plus de paiements marchands
- Saisonnalité (fêtes de fin d'année, rentrée scolaire)
- Taux d'échec plus élevé en zone rurale (réseau) et sur USSD

Usage : python generate_data.py
Sortie : mobile_money_transactions.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_ROWS = 60000

PAYS_INFO = {
    "Côte d'Ivoire":   {"poids": 0.28, "providers": ["Orange Money", "MTN MoMo", "Wave", "Moov Money"]},
    "Sénégal":         {"poids": 0.22, "providers": ["Orange Money", "Wave", "Free Money"]},
    "Mali":            {"poids": 0.14, "providers": ["Orange Money", "Moov Money"]},
    "Burkina Faso":    {"poids": 0.13, "providers": ["Orange Money", "Moov Money"]},
    "Bénin":           {"poids": 0.10, "providers": ["MTN MoMo", "Moov Money"]},
    "Togo":            {"poids": 0.07, "providers": ["MTN MoMo", "Moov Money"]},
    "Guinée":          {"poids": 0.06, "providers": ["Orange Money", "MTN MoMo"]},
}

TYPES_TRANSACTION = {
    "Dépôt":               0.20,
    "Retrait":             0.22,
    "Transfert P2P":       0.30,
    "Paiement marchand":   0.18,
    "Paiement facture":    0.10,
}

CANAUX = {"USSD": 0.45, "Application mobile": 0.40, "Agent physique": 0.15}
GENRES = {"Homme": 0.54, "Femme": 0.46}
TRANCHES_AGE = {"18-25": 0.22, "26-35": 0.34, "36-45": 0.23, "46-60": 0.15, "60+": 0.06}
ZONES = {"Urbain": 0.62, "Rural": 0.38}

# Frais moyens (%) par provider - Wave nettement moins cher (son positionnement réel)
FRAIS_PAR_PROVIDER = {
    "Wave": 0.01,
    "Orange Money": 0.025,
    "MTN MoMo": 0.025,
    "Moov Money": 0.022,
    "Free Money": 0.015,
}

date_debut = datetime(2023, 1, 1)
date_fin = datetime(2025, 12, 31)
total_jours = (date_fin - date_debut).days


def tirage_pondere(dico):
    cles = list(dico.keys())
    poids = np.array(list(dico.values()), dtype=float)
    poids /= poids.sum()
    return np.random.choice(cles, p=poids)


def facteur_saisonnier(date):
    """Pic décembre (fêtes) et rentrée scolaire (sept), creux en aout."""
    mois = date.month
    if mois == 12:
        return 1.35
    if mois == 9:
        return 1.20
    if mois == 8:
        return 0.85
    return 1.0


def facteur_croissance(date):
    """Croissance globale du secteur + montée en puissance de Wave dans le temps."""
    jours_ecoules = (date - date_debut).days
    return 1.0 + 0.35 * (jours_ecoules / total_jours)


rows = []
for i in range(N_ROWS):
    jour_offset = np.random.randint(0, total_jours)
    date = date_debut + timedelta(days=int(jour_offset))
    # légère pondération saisonnière/croissance via rejet simple
    if np.random.random() > (facteur_saisonnier(date) * facteur_croissance(date)) / 1.6:
        jour_offset = np.random.randint(0, total_jours)
        date = date_debut + timedelta(days=int(jour_offset))

    pays = tirage_pondere({p: v["poids"] for p, v in PAYS_INFO.items()})
    provider = np.random.choice(PAYS_INFO[pays]["providers"])
    type_transaction = tirage_pondere(TYPES_TRANSACTION)
    canal = tirage_pondere(CANAUX)
    genre = tirage_pondere(GENRES)
    tranche_age = tirage_pondere(TRANCHES_AGE)
    zone = tirage_pondere(ZONES)

    # Montant selon le type de transaction (FCFA)
    if type_transaction == "Paiement marchand":
        montant = np.random.gamma(shape=2.0, scale=6000)
    elif type_transaction == "Paiement facture":
        montant = np.random.gamma(shape=3.0, scale=8000)
    elif type_transaction == "Transfert P2P":
        montant = np.random.gamma(shape=2.2, scale=9000)
    else:
        montant = np.random.gamma(shape=2.5, scale=11000)
    montant = float(np.clip(montant, 500, 500000))
    montant = round(montant / 5) * 5  # arrondi FCFA réaliste

    frais = round(montant * FRAIS_PAR_PROVIDER[provider] * np.random.uniform(0.8, 1.2))
    frais = max(frais, 25) if type_transaction != "Dépôt" else 0

    # Taux d'échec : plus élevé en rural et sur USSD
    proba_echec = 0.03
    if zone == "Rural":
        proba_echec += 0.05
    if canal == "USSD":
        proba_echec += 0.03
    proba_attente = 0.015
    r = np.random.random()
    if r < proba_echec:
        statut = "Échoué"
    elif r < proba_echec + proba_attente:
        statut = "En attente"
    else:
        statut = "Réussi"

    heure = int(np.clip(np.random.normal(14, 4.5), 6, 23))

    rows.append({
        "transaction_id": f"TXN{100000 + i}",
        "date": date.strftime("%Y-%m-%d"),
        "heure": heure,
        "pays": pays,
        "provider": provider,
        "type_transaction": type_transaction,
        "canal": canal,
        "montant_fcfa": montant,
        "frais_fcfa": frais,
        "statut": statut,
        "genre_client": genre,
        "tranche_age": tranche_age,
        "zone": zone,
    })

df = pd.DataFrame(rows)
df.sort_values("date", inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv("mobile_money_transactions.csv", index=False, encoding="utf-8")
print(f"Dataset généré : {len(df)} lignes -> mobile_money_transactions.csv")
print(df.head())
