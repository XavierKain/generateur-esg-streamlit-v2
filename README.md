# Générateur ESG - Streamlit Cloud

Application web Streamlit pour la génération automatique de questionnaires ESG.

## 🚀 Déploiement sur Streamlit Community Cloud

Cette application est configurée pour être déployée facilement sur [Streamlit Community Cloud](https://streamlit.io/cloud).

### Fonctionnalités

- ✅ Upload de fichiers BDD ESG et templates
- ✅ Détection automatique des années disponibles
- ✅ Prévisualisation des données
- ✅ Génération en masse des questionnaires
- ✅ Téléchargement des résultats en ZIP

### Structure des fichiers

```text
streamlit_deployment/
├── app.py                          # Application principale Streamlit
├── generateur_2025_streamlit.py    # Module de génération
├── requirements.txt                # Dépendances Python
└── README.md                       # Ce fichier
```

### Instructions de déploiement

1. **Créer un repository GitHub** avec ces fichiers
2. **Se connecter à Streamlit Cloud** avec GitHub
3. **Déployer l'application** en pointant vers ce repository
4. **L'app sera accessible** via une URL publique fournie par Streamlit

### Utilisation

1. Uploadez votre fichier BDD ESG (.xlsx ou .xlsm)
2. Uploadez votre template de questionnaire
3. Sélectionnez l'année à traiter
4. Lancez la génération
5. Téléchargez le ZIP contenant tous les questionnaires générés

### Configuration requise

- Fichier BDD avec des onglets nommés par année (ex: "2023", "2024", "2025")
- Template de questionnaire Excel compatible
- Connexion internet pour le déploiement

### Support

Cette application génère automatiquement des questionnaires ESG personnalisés à partir de votre base de données.
