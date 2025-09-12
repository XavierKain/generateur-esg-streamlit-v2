#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des modifications apportées au générateur ESG
- Nouveau format de nommage avec date de la colonne L
- Sélection des questionnaires
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from generateur_2025_streamlit import read_year_data, get_questionnaires_preview

def test_lecture_donnees():
    """Tester la lecture des données avec la nouvelle colonne date"""
    print("=== Test de lecture des données ===")
    
    # Chemin vers le fichier BDD
    bdd_file = "../BDD-ESG-v2-20250801_1727.xlsx"
    
    if not os.path.exists(bdd_file):
        print(f"❌ Fichier BDD non trouvé: {bdd_file}")
        return False
    
    try:
        # Lire les données pour 2025
        data = read_year_data(bdd_file, "2025")
        print(f"✅ {len(data)} entrées lues pour l'année 2025")
        
        # Afficher les 3 premières entrées avec leurs dates
        for i, item in enumerate(data[:3]):
            print(f"\n--- Entrée {i+1} ---")
            print(f"ID: {item['numero_identification']}")
            print(f"Locataire: {item['locataire']}")
            print(f"Adresse: {item['adresse_complete']}")
            print(f"Date questionnaire: {item['date_questionnaire']}")
            print(f"Type de date: {type(item['date_questionnaire'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture: {e}")
        return False

def test_preview_questionnaires():
    """Tester la fonction de prévisualisation des questionnaires"""
    print("\n=== Test de prévisualisation ===")
    
    bdd_file = "../BDD-ESG-v2-20250801_1727.xlsx"
    
    if not os.path.exists(bdd_file):
        print(f"❌ Fichier BDD non trouvé: {bdd_file}")
        return False
    
    try:
        # Obtenir la prévisualisation
        preview = get_questionnaires_preview(bdd_file, "2025")
        print(f"✅ {len(preview)} questionnaires disponibles")
        
        # Afficher les 3 premiers
        for i, item in enumerate(preview[:3]):
            print(f"\n--- Questionnaire {i+1} ---")
            print(f"ID: {item['id']}")
            print(f"Locataire: {item['locataire']}")
            print(f"Date: {item['date']}")
            print(f"Nom fichier prévu: {item['filename_preview']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la prévisualisation: {e}")
        return False

def test_format_nommage():
    """Tester le nouveau format de nommage"""
    print("\n=== Test du format de nommage ===")
    
    from generateur_2025_streamlit import create_filename_with_folder
    import datetime
    
    # Données de test
    test_data = {
        'numero_identification': '123',
        'locataire': 'Test Locataire',
        'adresse_complete': 'Rue de la Paix, 15',
        'ville': 'Paris',
        'adresse': 'Rue de la Paix',
        'date_questionnaire': datetime.datetime(2024, 10, 7)  # Test avec une vraie date
    }
    
    folder_structure = f"{test_data['ville']} - {test_data['adresse']} - {test_data['locataire']}"
    
    try:
        filename = create_filename_with_folder(test_data, "2025", folder_structure)
        print(f"✅ Nom de fichier généré: {filename}")
        
        # Vérifier le format
        if "2024 10 07" in filename and "Questionnaire ESG" in filename and "#123" in filename:
            print("✅ Format correct détecté")
            return True
        else:
            print("❌ Format incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération du nom: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Tests des modifications du générateur ESG")
    print("=" * 50)
    
    tests = [
        test_lecture_donnees,
        test_preview_questionnaires,
        test_format_nommage
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Résultats des tests:")
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    passed = sum(results)
    total = len(results)
    print(f"\n🎯 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés !")
    else:
        print("⚠️ Certains tests ont échoué")
