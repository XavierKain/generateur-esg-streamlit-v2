#!/usr/bin/env python3
"""
Script de packaging pour créer la distribution finale
"""

import os
import shutil
import zipfile
from pathlib import Path
import datetime

def create_distribution():
    """Créer un package de distribution complet"""
    
    # Nom du package
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    package_name = f"Generateur_ESG_Local_{timestamp}"
    
    # Créer le dossier de distribution
    dist_dir = Path("distribution") / package_name
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Fichiers à inclure
    files_to_include = [
        "app.py",
        "generateur_2025_streamlit.py", 
        "xlwings_generator.py",
        "requirements.txt",
        "launch_app.py",
        "Générateur_ESG.bat",
        "Générateur_ESG.command",
        "build_app.py",
        "README_UTILISATEUR.md"
    ]
    
    # Copier les fichiers
    print("📦 Création du package de distribution...")
    for file_name in files_to_include:
        src = Path(file_name)
        if src.exists():
            dst = dist_dir / file_name
            shutil.copy2(src, dst)
            print(f"✅ {file_name}")
        else:
            print(f"⚠️  {file_name} non trouvé")
    
    # Copier l'application macOS si elle existe
    app_dir = Path("Générateur ESG.app")
    if app_dir.exists():
        shutil.copytree(app_dir, dist_dir / "Générateur ESG.app")
        print(f"✅ Générateur ESG.app")
    
    # Créer un ZIP
    zip_path = Path("distribution") / f"{package_name}.zip"
    print(f"🗜️  Création du ZIP: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(dist_dir.parent)
                zipf.write(file_path, arcname)
    
    # Créer un fichier d'instructions
    instructions = f"""
# 📦 Générateur ESG - Package de Distribution

**Package créé le :** {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}

## 🚀 Installation et Utilisation

### Windows 🪟
1. Extraire le fichier ZIP
2. Double-cliquer sur `Générateur_ESG.bat`
3. L'interface graphique s'ouvre automatiquement

### macOS 🍎
1. Extraire le fichier ZIP
2. Double-cliquer sur `Générateur_ESG.command`
3. Ou utiliser `Générateur ESG.app` pour une expérience native

## 📋 Prérequis
- Python 3.7+ installé sur le système
- Excel (optionnel, pour le formatage conditionnel optimal)

## 🔧 Fonctionnalités
- Interface graphique intuitive
- Installation automatique des dépendances
- xlwings pour formatage conditionnel (quand Excel disponible)
- Fallback openpyxl automatique
- Traitement 100% local et confidentiel

## 📚 Documentation
Consultez `README_UTILISATEUR.md` pour le guide complet.

---
**Version :** 1.0 - Distribution autonome
    """
    
    instructions_path = dist_dir / "LIRE_MOI.txt"
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions.strip())
    
    print(f"\n✅ Package créé avec succès !")
    print(f"📁 Dossier: {dist_dir}")
    print(f"🗜️  Archive: {zip_path}")
    print(f"📄 Instructions: {instructions_path}")
    
    return zip_path

if __name__ == "__main__":
    create_distribution()