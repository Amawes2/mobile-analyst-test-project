# 📱 Mobile Money Analytics — Afrique de l'Ouest

Dashboard interactif d'analyse de données sur le mobile money en Afrique de
l'Ouest (Côte d'Ivoire, Sénégal, Mali, Burkina Faso, Bénin, Togo, Guinée),
construit avec **Python, Pandas et Streamlit**.

> Projet portfolio conçu pour démontrer des compétences en **analyse de
> données, data storytelling et déploiement d'applications data**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Objectif

Analyser un jeu de données de transactions mobile money (Orange Money, MTN
MoMo, Wave, Moov Money, Free Money) pour en tirer des indicateurs business :
volumes échangés, revenus générés par les frais, fiabilité des opérateurs,
saisonnalité, et segmentation des utilisateurs par zone/âge/genre.

Les données sont **synthétiques mais construites avec des patterns
réalistes** (positionnement tarifaire de Wave, saisonnalité de fin d'année,
écarts urbain/rural, etc.), ce qui permet de partager librement le projet
sans contrainte de confidentialité.

## 🗂️ Structure du projet

```
mobile-money-dashboard/
├── app.py                          # Page d'accueil : vue d'ensemble & KPIs
├── pages/
│   ├── 1_🌍_Analyse_par_pays.py
│   ├── 2_📊_Comparatif_operateurs.py
│   ├── 3_📈_Tendances_temporelles.py
│   └── 4_👥_Segmentation_clients.py
├── utils/
│   └── data_loader.py              # Chargement, filtres, formatage FCFA
├── data/
│   ├── generate_data.py            # Génération du dataset synthétique
│   └── mobile_money_transactions.csv
├── .streamlit/config.toml          # Thème visuel
├── requirements.txt
└── README.md
```

## 📊 Pages du dashboard

| Page | Contenu |
|---|---|
| **Vue d'ensemble** | KPIs clés, évolution mensuelle, répartition par type de transaction |
| **Analyse par pays** | Volumes, taux de réussite et répartition urbain/rural par pays |
| **Comparatif opérateurs** | Volumes, frais moyens, fiabilité et évolution par opérateur |
| **Tendances temporelles** | Séries quotidiennes, activité par heure/jour, saisonnalité mensuelle |
| **Segmentation clients** | Répartition par genre, âge, zone, canal utilisé |

Tous les filtres (pays, opérateur, période, statut) sont partagés entre les
pages via la barre latérale.

## 🚀 Installation et exécution en local

```bash
git clone <url-de-ton-repo>
cd mobile-money-dashboard

python3 -m venv venv
source venv/bin/activate      # sous Windows : venv\Scripts\activate

pip install -r requirements.txt

# (optionnel) régénérer un nouveau jeu de données synthétique
python3 data/generate_data.py

streamlit run app.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`.

## ☁️ Déploiement (gratuit, en ligne) — Streamlit Community Cloud

1. Pousse ce dossier dans un dépôt GitHub public (ou privé).
2. Va sur [share.streamlit.io](https://share.streamlit.io) et connecte ton
   compte GitHub.
3. Clique sur **New app**, sélectionne le dépôt, la branche, et indique
   `app.py` comme fichier principal.
4. Clique sur **Deploy**. L'application est en ligne en 1 à 2 minutes,
   avec une URL du type `https://<nom>.streamlit.app` que tu peux mettre
   directement sur ton CV, LinkedIn ou GitHub.

Le fichier `.streamlit/config.toml` fixe déjà le thème visuel, aucune
configuration supplémentaire n'est nécessaire.

### Alternative : Render / Railway
Le projet fonctionne aussi tel quel sur Render ou Railway via la commande
de démarrage :
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## 🛠️ Stack technique

- **Python** — traitement et logique métier
- **Pandas / NumPy** — manipulation et agrégation des données
- **Streamlit** — interface web interactive multi-pages
- **Plotly Express** — visualisations interactives

## 📈 Pistes d'évolution

- Connecter une vraie source de données (API, base SQL) via
  `utils/data_loader.py`
- Ajouter une détection d'anomalies/fraude (transactions atypiques)
- Ajouter l'authentification pour un usage interne à une équipe
- Exporter des rapports PDF automatiques depuis le dashboard

## 👤 Auteur

Réalisé par **Amadou Kaba (AMSK Digital)** — étudiant en informatique
(spécialité bases de données) et développeur freelance, dans le cadre
d'un portfolio orienté Data Analyst / Data Scientist / Data Engineer.

## 📄 Licence

MIT — libre d'utilisation, de modification et de partage.
