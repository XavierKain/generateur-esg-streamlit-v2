# MODIFICATIONS APPORTÉES AU GÉNÉRATEUR ESG

## 📋 Résumé des changements

Ce document décrit les modifications apportées au dossier `streamlit_deployment` du générateur ESG pour répondre aux demandes suivantes :

### 🎯 Objectifs réalisés

1. **Nouveau format de nommage des questionnaires**
   - Format demandé : `AAAA MM JJ – Questionnaire ESG – Rue, n° - locataire - #id`
   - Date provient de la colonne L de la BDD (au lieu de la date de génération)

2. **Sélection des questionnaires à générer**
   - Interface permettant de choisir quels questionnaires générer
   - Évite la regénération complète à chaque fois

---

## 🔧 Modifications techniques

### Fichier : `generateur_2025_streamlit.py`

#### 1. Lecture de la colonne L (Date)
```python
# Ajout de la lecture de la colonne L (colonne 12)
date_questionnaire = ws.cell(row=row, column=12).value

# Ajout dans la structure de données
row_data = {
    # ... autres champs
    'date_questionnaire': date_questionnaire  # NOUVELLE DONNÉE
}
```

#### 2. Nouveau système de nommage
```python
def create_filename_with_folder(data, year, folder_structure):
    # Récupération de la date depuis la colonne L
    date_questionnaire = data.get('date_questionnaire')
    if date_questionnaire and hasattr(date_questionnaire, 'strftime'):
        date_formatted = date_questionnaire.strftime("%Y %m %d")
    # ... gestion des cas d'erreur avec fallback date actuelle
    
    # Nouveau format
    filename = f"{date_formatted} – Questionnaire ESG – {rue_numero} - {locataire} - #{numero}.xlsx"
```

#### 3. Nouvelles fonctions ajoutées
- `get_questionnaires_preview()` : Obtient la liste des questionnaires avec prévisualisation
- `generate_selected_questionnaires_to_zip()` : Génère uniquement les questionnaires sélectionnés

### Fichier : `app.py`

#### 1. Nouvelles variables de session
```python
if 'selected_questionnaire_indices' not in st.session_state:
    st.session_state.selected_questionnaire_indices = []
if 'questionnaires_preview' not in st.session_state:
    st.session_state.questionnaires_preview = []
```

#### 2. Interface de sélection
- Expandeur avec prévisualisation des questionnaires
- Checkboxes pour sélection individuelle
- Boutons "Tout sélectionner", "Tout désélectionner", "Inverser"
- Pagination pour gérer de nombreux questionnaires
- Affichage du futur nom de fichier

#### 3. Génération sélective
- Modification de `generate_questionnaires()` pour utiliser la sélection
- Mise à jour des résultats pour afficher les statistiques de sélection

---

## 🎨 Interface utilisateur

### Étape 2 : Configuration
1. **Sélection de l'année** (inchangé)
2. **Prévisualisation et sélection** (nouveau) :
   - Liste de tous les questionnaires disponibles
   - Aperçu du nom de fichier qui sera généré
   - Sélection via checkboxes
   - Boutons de sélection rapide
   - Pagination si nombreux questionnaires

### Étape 3 : Génération
- Affichage du nombre de questionnaires sélectionnés
- Génération uniquement des questionnaires choisis
- Statistiques détaillées (générés/échecs/total disponible)

---

## 📊 Exemples de noms de fichiers

### Avant (ancien format)
```
#123 - 2025 09 11 - Questionnaire ESG - Paris - Rue de la Paix - Locataire.xlsx
```

### Après (nouveau format)
```
2024 10 07 – Questionnaire ESG – Rue de la Paix, 15 - Locataire - #123.xlsx
```

### Gestion des cas particuliers
- **Date manquante** : Utilise la date actuelle
- **Caractères spéciaux** : Nettoyage automatique
- **Noms trop longs** : Troncature intelligente

---

## 🧪 Tests effectués

Le script `test_modifications.py` valide :

1. ✅ **Lecture des données** : Colonne L correctement lue (172 entrées)
2. ✅ **Prévisualisation** : 172 questionnaires détectés avec aperçu
3. ✅ **Format de nommage** : Nouveau format correct

---

## 🚀 Utilisation

1. **Lancer l'application** :
   ```bash
   cd streamlit_deployment
   python3 -m streamlit run app.py
   ```

2. **Workflow** :
   - Étape 1 : Upload fichiers BDD et template
   - Étape 2 : Sélectionner année + choisir questionnaires
   - Étape 3 : Générer et télécharger ZIP

3. **Fonctionnalités** :
   - Sélection fine des questionnaires
   - Prévisualisation des noms de fichiers
   - Téléchargement ZIP optimisé
   - Interface responsive et intuitive

---

## 🔄 Compatibilité

- ✅ Compatible avec les anciens fichiers BDD
- ✅ Gestion des dates manquantes
- ✅ Fallback vers génération complète si erreur
- ✅ Interface progressive maintenue
- ✅ Fonctionnalités existantes préservées

---

## 📝 Notes importantes

1. **Format de date** : La colonne L doit contenir des dates Excel valides
2. **Performance** : Génération uniquement des questionnaires sélectionnés
3. **Fichiers** : Structure de dossiers maintenue dans le ZIP
4. **Interface** : Pagination automatique pour les grandes listes

Les modifications sont entièrement fonctionnelles et prêtes à l'utilisation ! 🎉
