#!/bin/bash
# Script pour pousser le code vers le nouveau repository GitHub

echo "🚀 Poussée vers le nouveau repository GitHub..."

# Vérifier que le remote existe
git remote -v

# Pousser vers GitHub
git push -u origin main

echo "✅ Code poussé avec succès !"
echo "🌐 Repository disponible sur : https://github.com/XavierKain/generateur-esg-streamlit"
echo "🚀 Prêt pour le déploiement Streamlit Community Cloud !"
