# 🚀 Générateur ESG - Application Locale

## 📋 Guide d'installation et d'utilisation

### 🎯 Lancement rapide

#### Windows 🪟
1. **Double-cliquez** sur `Générateur_ESG.bat`
2. L'interface graphique s'ouvre automatiquement
3. Cliquez sur "🚀 Démarrer l'Application"
4. L'application s'ouvre dans votre navigateur

#### macOS 🍎
1. **Double-cliquez** sur `Générateur_ESG.command`
2. Si demandé, autorisez l'exécution du script
3. L'interface graphique s'ouvre automatiquement
4. Cliquez sur "🚀 Démarrer l'Application"

#### Application macOS (.app) 🍎
1. Exécutez `python3 build_app.py` pour créer l'application
2. **Double-cliquez** sur `Générateur ESG.app`
3. L'application démarre comme une application native

### 🖥️ Interface Graphique

L'application dispose d'une interface moderne avec :

- **📊 Informations système** : Version Python, système d'exploitation
- **🎛️ Contrôles** : Démarrer, arrêter, ouvrir le navigateur
- **📈 Barre de progression** : Suivi du démarrage
- **🌐 URL automatique** : Lien direct vers l'application

### 🔧 Fonctionnalités

#### ✅ **Avantages de cette version :**
- **🖱️ Interface utilisateur intuitive** (graphique + console fallback)
- **🔄 Installation automatique** des dépendances
- **🚀 Démarrage automatique** de Streamlit
- **🌐 Ouverture automatique** du navigateur
- **🔍 Détection intelligente** des ports libres
- **🛡️ Gestion robuste** des erreurs
- **⏹️ Arrêt propre** des processus

#### 🎨 **Formatage conditionnel :**
- **✅ xlwings** : Formatage parfait quand Excel est installé
- **🔄 openpyxl** : Fallback automatique si Excel indisponible
- **📊 Affichage du statut** : Interface claire des moteurs disponibles

### 📱 Utilisation de l'application web

Une fois l'application démarrée :

1. **📁 Upload des fichiers** :
   - Fichier BDD Excel (avec onglets par année)
   - Template de questionnaire Excel

2. **⚙️ Configuration** :
   - Sélection de l'année
   - Choix des questionnaires à générer

3. **🚀 Génération** :
   - Traitement automatique avec xlwings ou openpyxl
   - Affichage de la progression en temps réel

4. **📥 Téléchargement** :
   - Fichier ZIP avec tous les questionnaires
   - Structure de dossiers organisée

### 🛠️ Résolution de problèmes

#### ❌ **"Python n'est pas installé"**
- Téléchargez Python depuis [python.org](https://python.org)
- **⚠️ IMPORTANT** : Cochez "Add to PATH" lors de l'installation Windows

#### ❌ **"Erreur de dépendances"**
- L'application installe automatiquement les packages requis
- Si échec : ouvrez un terminal et exécutez `pip install -r requirements.txt`

#### ❌ **"Port déjà utilisé"**
- L'application trouve automatiquement un port libre (8501-8510)
- Si tous occupés, fermez d'autres applications Streamlit

#### ❌ **"Interface graphique ne s'ouvre pas"**
- L'application passe automatiquement en mode console
- Toutes les fonctionnalités restent disponibles

### 💡 Conseils d'utilisation

- **🔧 Fermez Excel** avant la génération pour de meilleures performances
- **🌐 Utilisez Chrome/Firefox** pour une expérience optimale
- **💾 Sauvegardez vos templates** avant modification
- **📂 Organisez vos fichiers BDD** par année dans des onglets séparés

### 🆘 Support

- **📧 Contact** : Votre administrateur système
- **📝 Documentation** : Ce fichier README
- **🐛 Problèmes** : Contactez le support technique

---

### 🔒 Sécurité et Confidentialité

- **💻 Traitement local** : Toutes vos données restent sur votre ordinateur
- **🚫 Aucune transmission** : Pas d'envoi de données vers des serveurs externes
- **🔐 Confidentialité garantie** : Vos questionnaires restent privés

---

**Version :** 1.0  
**Date :** 2025  
**Compatibilité :** Windows 10+, macOS 10.9+, Python 3.7+