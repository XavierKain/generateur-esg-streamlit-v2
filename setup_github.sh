#!/bin/bash

# Script pour connecter le repository local au repository GitHub
# À exécuter après avoir créé le repository sur GitHub.com

echo "🚀 Configuration du repository GitHub..."

# Ajouter l'origine remote (remplacez VOTRE_USERNAME par votre nom GitHub réel)
echo "Ajout du remote origin..."
git remote add origin https://github.com/VOTRE_USERNAME/generateur-esg-streamlit.git

echo "Push vers GitHub..."
git push -u origin main

echo "✅ Repository uploadé avec succès !"
echo "🌐 Votre repository est maintenant disponible sur GitHub"
echo "➡️  Prochaine étape : Déployer sur Streamlit Cloud"
echo "📖 Consultez INSTRUCTIONS_GITHUB.md pour les étapes Streamlit Cloud"
