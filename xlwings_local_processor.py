#!/usr/bin/env python3
"""
Script local pour traiter les questionnaires ESG avec xlwings et Excel local.
Ce script doit être exécuté sur une machine où Excel est installé.
"""

import os
import sys
import json
import zipfile
from pathlib import Path
import tempfile
import argparse
from datetime import datetime

try:
    import xlwings as xw
    import pandas as pd
    import openpyxl
    XLWINGS_AVAILABLE = True
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Veuillez installer les dépendances: pip install xlwings pandas openpyxl")
    sys.exit(1)


class LocalXLWingsProcessor:
    """Processeur local utilisant xlwings avec Excel local."""
    
    def __init__(self):
        self.app = None
        
    def __enter__(self):
        """Initialise l'application Excel."""
        try:
            # Démarrer Excel en mode visible=False pour les opérations en batch
            self.app = xw.App(visible=False, add_book=False)
            return self
        except Exception as e:
            print(f"Erreur lors de l'initialisation d'Excel: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme l'application Excel."""
        if self.app:
            try:
                self.app.quit()
            except:
                pass
    
    def process_questionnaire_data(self, data_file, template_file, output_dir):
        """
        Traite les données de questionnaire avec xlwings.
        
        Args:
            data_file: Fichier JSON avec les données
            template_file: Fichier Excel template
            output_dir: Dossier de sortie
        """
        with open(data_file, 'r', encoding='utf-8') as f:
            questionnaire_data = json.load(f)
        
        results = []
        
        for item in questionnaire_data:
            entreprise = item['entreprise']
            year = item['year']
            data = item['data']
            
            output_filename = f"Questionnaire_ESG_{entreprise}_{year}.xlsx"
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                self._generate_single_questionnaire(
                    template_file, data, output_path, entreprise, year
                )
                results.append({
                    'entreprise': entreprise,
                    'filename': output_filename,
                    'status': 'success'
                })
                print(f"✓ Généré: {output_filename}")
                
            except Exception as e:
                results.append({
                    'entreprise': entreprise,
                    'filename': output_filename,
                    'status': 'error',
                    'error': str(e)
                })
                print(f"✗ Erreur pour {entreprise}: {e}")
        
        return results
    
    def _generate_single_questionnaire(self, template_file, data, output_path, entreprise, year):
        """Génère un questionnaire individuel avec xlwings."""
        # Ouvrir le template
        wb = self.app.books.open(template_file)
        
        try:
            # Identifier la feuille de travail
            if 'Questionnaire' in [sheet.name for sheet in wb.sheets]:
                ws = wb.sheets['Questionnaire']
            else:
                ws = wb.sheets[0]  # Première feuille par défaut
            
            # Mise à jour des métadonnées
            ws.range('B2').value = entreprise  # Supposons que B2 contient le nom de l'entreprise
            ws.range('B3').value = year        # Supposons que B3 contient l'année
            
            # Remplir les données du questionnaire
            for row_data in data:
                if isinstance(row_data, dict) and 'row' in row_data:
                    row_num = row_data['row']
                    
                    # Remplir les colonnes selon le mapping
                    if 'valeur_realisee' in row_data:
                        ws.range(f'E{row_num}').value = row_data['valeur_realisee']
                    if 'valeur_cible' in row_data:
                        ws.range(f'F{row_num}').value = row_data['valeur_cible']
                    if 'commentaire' in row_data:
                        ws.range(f'G{row_num}').value = row_data['commentaire']
            
            # Recalculer les formules
            wb.app.calculate()
            
            # Sauvegarder avec le formatage conditionnel préservé
            wb.save(output_path)
            
        finally:
            wb.close()
    
    def create_batch_zip(self, output_dir, zip_filename):
        """Crée un fichier ZIP avec tous les questionnaires générés."""
        zip_path = os.path.join(output_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(output_dir):
                if file.endswith('.xlsx') and file != zip_filename:
                    file_path = os.path.join(output_dir, file)
                    zipf.write(file_path, file)
        
        return zip_path


def main():
    """Fonction principale du script."""
    parser = argparse.ArgumentParser(description='Processeur local xlwings pour questionnaires ESG')
    parser.add_argument('--data', required=True, help='Fichier JSON avec les données')
    parser.add_argument('--template', required=True, help='Fichier Excel template')
    parser.add_argument('--output', default='output', help='Dossier de sortie')
    parser.add_argument('--zip', help='Nom du fichier ZIP final')
    
    args = parser.parse_args()
    
    # Vérifier que les fichiers existent
    if not os.path.exists(args.data):
        print(f"Erreur: Fichier de données introuvable: {args.data}")
        sys.exit(1)
    
    if not os.path.exists(args.template):
        print(f"Erreur: Template introuvable: {args.template}")
        sys.exit(1)
    
    # Créer le dossier de sortie
    os.makedirs(args.output, exist_ok=True)
    
    print(f"Début du traitement avec xlwings...")
    print(f"Données: {args.data}")
    print(f"Template: {args.template}")
    print(f"Sortie: {args.output}")
    
    try:
        with LocalXLWingsProcessor() as processor:
            results = processor.process_questionnaire_data(
                args.data, args.template, args.output
            )
            
            # Créer le ZIP si demandé
            if args.zip:
                zip_path = processor.create_batch_zip(args.output, args.zip)
                print(f"✓ Archive créée: {zip_path}")
            
            # Afficher le résumé
            success_count = len([r for r in results if r['status'] == 'success'])
            error_count = len([r for r in results if r['status'] == 'error'])
            
            print(f"\n=== RÉSUMÉ ===")
            print(f"Questionnaires générés avec succès: {success_count}")
            print(f"Erreurs: {error_count}")
            
            if error_count > 0:
                print("\nErreurs détaillées:")
                for result in results:
                    if result['status'] == 'error':
                        print(f"- {result['entreprise']}: {result['error']}")
    
    except Exception as e:
        print(f"Erreur fatale: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()