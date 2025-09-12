#!/usr/bin/env python3
"""
Client xlwings distant pour traitement Excel local depuis Streamlit Cloud.
Ce script s'exécute localement et communique avec l'app Streamlit via HTTP.
"""

import requests
import json
import os
import tempfile
import zipfile
from pathlib import Path
import argparse
import time
from datetime import datetime
import xlwings as xw
import pandas as pd
from openpyxl import load_workbook

class XLWingsRemoteClient:
    """Client qui récupère les données depuis Streamlit et traite avec Excel local."""
    
    def __init__(self, streamlit_url="https://votre-app.streamlitapp.com"):
        self.streamlit_url = streamlit_url.rstrip('/')
        self.app = None
        
    def __enter__(self):
        """Initialise Excel."""
        try:
            self.app = xw.App(visible=False, add_book=False)
            return self
        except Exception as e:
            print(f"Erreur lors de l'initialisation d'Excel: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme Excel."""
        if self.app:
            try:
                self.app.quit()
            except:
                pass
    
    def get_processing_job(self, job_id):
        """Récupère un job de traitement depuis Streamlit."""
        try:
            response = requests.get(f"{self.streamlit_url}/api/get_job/{job_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erreur API: {response.status_code}")
                return None
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return None
    
    def download_template(self, template_url, local_path):
        """Télécharge le template Excel."""
        try:
            response = requests.get(template_url)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            print(f"Erreur téléchargement template: {e}")
            return False
    
    def process_questionnaires(self, job_data, output_dir):
        """Traite les questionnaires avec xlwings."""
        template_path = os.path.join(output_dir, "template.xlsx")
        
        # Télécharger le template
        if not self.download_template(job_data['template_url'], template_path):
            raise Exception("Impossible de télécharger le template")
        
        results = []
        questionnaires = job_data['questionnaires']
        
        for i, quest_data in enumerate(questionnaires):
            entreprise = quest_data['entreprise']
            year = quest_data['year']
            data = quest_data['data']
            
            print(f"Traitement {i+1}/{len(questionnaires)}: {entreprise}")
            
            output_filename = f"Questionnaire_ESG_{entreprise}_{year}.xlsx"
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                self._process_single_questionnaire(
                    template_path, data, output_path, entreprise, year
                )
                results.append({
                    'entreprise': entreprise,
                    'filename': output_filename,
                    'status': 'success'
                })
                print(f"✓ {entreprise} - Terminé")
                
            except Exception as e:
                results.append({
                    'entreprise': entreprise,
                    'filename': output_filename,
                    'status': 'error',
                    'error': str(e)
                })
                print(f"✗ {entreprise} - Erreur: {e}")
        
        return results
    
    def _process_single_questionnaire(self, template_path, data, output_path, entreprise, year):
        """Traite un questionnaire individuel."""
        # Ouvrir le template
        wb = self.app.books.open(template_path)
        
        try:
            # Trouver la feuille de travail
            ws = None
            for sheet in wb.sheets:
                if 'questionnaire' in sheet.name.lower():
                    ws = sheet
                    break
            if not ws:
                ws = wb.sheets[0]
            
            # Mise à jour des métadonnées
            try:
                ws.range('B2').value = entreprise
                ws.range('B3').value = year
            except:
                pass  # Les cellules peuvent ne pas exister
            
            # Remplir les données
            for row_data in data:
                if isinstance(row_data, dict) and 'row' in row_data:
                    row_num = row_data['row']
                    
                    try:
                        if 'valeur_realisee' in row_data and row_data['valeur_realisee'] is not None:
                            ws.range(f'E{row_num}').value = row_data['valeur_realisee']
                        if 'valeur_cible' in row_data and row_data['valeur_cible'] is not None:
                            ws.range(f'F{row_num}').value = row_data['valeur_cible']
                        if 'commentaire' in row_data and row_data['commentaire']:
                            ws.range(f'G{row_num}').value = row_data['commentaire']
                    except Exception as e:
                        print(f"Erreur ligne {row_num}: {e}")
            
            # Recalculer et sauvegarder
            wb.app.calculate()
            wb.save(output_path)
            
        finally:
            wb.close()
    
    def upload_results(self, job_id, results, zip_path):
        """Upload les résultats vers Streamlit."""
        try:
            files = {'file': open(zip_path, 'rb')}
            data = {
                'job_id': job_id,
                'results': json.dumps(results)
            }
            
            response = requests.post(
                f"{self.streamlit_url}/api/upload_results",
                files=files,
                data=data
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Erreur upload: {e}")
            return False
    
    def create_zip(self, output_dir, zip_filename="questionnaires_processed.zip"):
        """Crée un ZIP avec tous les fichiers générés."""
        zip_path = os.path.join(output_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(output_dir):
                if file.endswith('.xlsx') and file != 'template.xlsx':
                    file_path = os.path.join(output_dir, file)
                    zipf.write(file_path, file)
        
        return zip_path


def main():
    parser = argparse.ArgumentParser(description='Client xlwings distant')
    parser.add_argument('--url', required=True, help='URL de l\'app Streamlit')
    parser.add_argument('--job-id', required=True, help='ID du job à traiter')
    parser.add_argument('--output', default='output', help='Dossier de sortie')
    
    args = parser.parse_args()
    
    print(f"=== Client xlwings distant ===")
    print(f"URL Streamlit: {args.url}")
    print(f"Job ID: {args.job_id}")
    print(f"Dossier sortie: {args.output}")
    
    os.makedirs(args.output, exist_ok=True)
    
    client = XLWingsRemoteClient(args.url)
    
    # Récupérer le job
    print("Récupération du job...")
    job_data = client.get_processing_job(args.job_id)
    if not job_data:
        print("Impossible de récupérer le job")
        return
    
    print(f"Job trouvé: {len(job_data['questionnaires'])} questionnaires à traiter")
    
    # Traiter avec xlwings
    try:
        with client:
            print("Début du traitement...")
            results = client.process_questionnaires(job_data, args.output)
            
            # Créer le ZIP
            zip_path = client.create_zip(args.output)
            print(f"Archive créée: {zip_path}")
            
            # Upload les résultats
            print("Upload des résultats...")
            if client.upload_results(args.job_id, results, zip_path):
                print("✓ Résultats uploadés avec succès")
            else:
                print("✗ Erreur lors de l'upload")
            
            # Afficher le résumé
            success_count = len([r for r in results if r['status'] == 'success'])
            error_count = len([r for r in results if r['status'] == 'error'])
            
            print(f"\n=== RÉSUMÉ ===")
            print(f"Succès: {success_count}")
            print(f"Erreurs: {error_count}")
            
    except Exception as e:
        print(f"Erreur fatale: {e}")


if __name__ == "__main__":
    main()