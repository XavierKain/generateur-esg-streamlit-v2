# 🚀 INSTRUCTIONS GITHUB SETUP

## Étapes pour créer et configurer le repository GitHub

### 1. Créer le repository sur GitHub.com

1. **Aller sur GitHub.com** et se connecter
2. **Cliquer sur le bouton "+" en haut à droite** → "New repository"
3. **Configurer le repository :**
   - Repository name: `generateur-esg-streamlit`
   - Description: `Application Streamlit pour la génération automatique de questionnaires ESG`
   - Visibility: **Public** (obligatoire pour Streamlit Community Cloud gratuit)
   - ❌ **NE PAS** cocher "Add a README file" (nous en avons déjà un)
   - ❌ **NE PAS** ajouter .gitignore ou license
4. **Cliquer sur "Create repository"**

### 2. Connecter le repository local au repository GitHub

Une fois le repository créé sur GitHub, GitHub vous donnera des instructions.
Utilisez ces commandes dans le terminal (le repository local est déjà initialisé) :

```bash
cd "/Users/xavier/VS Code/FA interface/streamlit_deployment"
git remote add origin https://github.com/VOTRE_USERNAME/generateur-esg-streamlit.git
git push -u origin main
```

**Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub réel.**

### 3. Vérifier l'upload

Après le push, vérifiez que tous les fichiers sont présents sur GitHub :
- ✅ app.py
- ✅ generateur_2025_streamlit.py  
- ✅ requirements.txt
- ✅ README.md
- ✅ GUIDE_DEPLOIEMENT.md

### 4. Déployer sur Streamlit Cloud

Une fois le repository GitHub créé et les fichiers uploadés :

1. **Aller sur [share.streamlit.io](https://share.streamlit.io/)**
2. **Se connecter avec GitHub**
3. **Cliquer sur "New app"**
4. **Configurer :**
   - Repository: `VOTRE_USERNAME/generateur-esg-streamlit`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choisir un nom unique (ex: `xavier-generateur-esg`)
5. **Cliquer sur "Deploy!"**

### 5. L'application sera accessible

Votre application sera disponible à une URL comme :
`https://xavier-generateur-esg.streamlit.app/`

---

## ✅ Résumé des fichiers prêts pour le déploiement

Le repository local est prêt avec :
- 📁 Repository Git initialisé
- 📝 Tous les fichiers committé
- 🎯 Branche `main` configurée
- ⚡ Prêt pour le push vers GitHub

## 🔄 Si vous voulez modifier des fichiers plus tard

Pour mettre à jour l'application après modifications :

```bash
cd "/Users/xavier/VS Code/FA interface/streamlit_deployment"
git add .
git commit -m "Description des modifications"
git push origin main
```

L'application Streamlit se redéploiera automatiquement !
