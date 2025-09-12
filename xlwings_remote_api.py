#!/usr/bin/env python3
"""
API pour gérer les jobs de traitement xlwings distant.
Ce module s'intègre dans l'app Streamlit pour orchestrer le traitement distant.
"""

import json
import uuid
import time
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st
from typing import Dict, List, Optional
import base64

class XLWingsJobManager:
    """Gestionnaire des jobs de traitement xlwings distant."""
    
    def __init__(self):
        self.jobs = {}  # En production, utiliser une base de données
        self.job_timeout = timedelta(hours=2)
    
    def create_job(self, questionnaires_data: List[Dict], template_content: bytes, 
                   template_filename: str) -> str:
        """Crée un nouveau job de traitement."""
        job_id = str(uuid.uuid4())
        
        # Sauvegarder le template temporairement
        temp_dir = tempfile.mkdtemp()
        template_path = os.path.join(temp_dir, template_filename)
        
        with open(template_path, 'wb') as f:
            f.write(template_content)
        
        # Créer le job
        job = {
            'id': job_id,
            'created_at': datetime.now(),
            'status': 'pending',  # pending, processing, completed, failed, expired
            'questionnaires': questionnaires_data,
            'template_path': template_path,
            'template_filename': template_filename,
            'results': None,
            'result_file': None,
            'error_message': None
        }
        
        self.jobs[job_id] = job
        return job_id
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Récupère un job par son ID."""
        job = self.jobs.get(job_id)
        if not job:
            return None
        
        # Vérifier l'expiration
        if datetime.now() - job['created_at'] > self.job_timeout:
            job['status'] = 'expired'
        
        return job
    
    def get_job_for_client(self, job_id: str) -> Optional[Dict]:
        """Récupère un job formaté pour le client distant."""
        job = self.get_job(job_id)
        if not job or job['status'] != 'pending':
            return None
        
        # Marquer comme en cours de traitement
        job['status'] = 'processing'
        job['processing_started_at'] = datetime.now()
        
        # Retourner les données nécessaires au client
        return {
            'job_id': job_id,
            'questionnaires': job['questionnaires'],
            'template_url': f"/api/download_template/{job_id}",
            'created_at': job['created_at'].isoformat()
        }
    
    def complete_job(self, job_id: str, results: List[Dict], result_file_content: bytes) -> bool:
        """Marque un job comme terminé avec les résultats."""
        job = self.jobs.get(job_id)
        if not job:
            return False
        
        # Sauvegarder le fichier résultat
        temp_dir = tempfile.mkdtemp()
        result_path = os.path.join(temp_dir, f"results_{job_id}.zip")
        
        with open(result_path, 'wb') as f:
            f.write(result_file_content)
        
        job['status'] = 'completed'
        job['completed_at'] = datetime.now()
        job['results'] = results
        job['result_file'] = result_path
        
        return True
    
    def fail_job(self, job_id: str, error_message: str) -> bool:
        """Marque un job comme échoué."""
        job = self.jobs.get(job_id)
        if not job:
            return False
        
        job['status'] = 'failed'
        job['failed_at'] = datetime.now()
        job['error_message'] = error_message
        
        return True
    
    def cleanup_expired_jobs(self):
        """Nettoie les jobs expirés."""
        expired_jobs = []
        for job_id, job in self.jobs.items():
            if datetime.now() - job['created_at'] > self.job_timeout:
                expired_jobs.append(job_id)
                # Nettoyer les fichiers temporaires
                try:
                    if job.get('template_path'):
                        os.unlink(job['template_path'])
                    if job.get('result_file'):
                        os.unlink(job['result_file'])
                except:
                    pass
        
        for job_id in expired_jobs:
            del self.jobs[job_id]


# Instance globale du gestionnaire de jobs
if 'job_manager' not in st.session_state:
    st.session_state.job_manager = XLWingsJobManager()

def create_xlwings_remote_interface(questionnaires_data, template_content, template_filename):
    """Interface Streamlit pour le traitement xlwings distant."""
    st.markdown("---")
    st.subheader("🔗 Traitement xlwings distant")
    
    st.info("""
    **Mode xlwings distant** : Cette solution permet d'utiliser Excel installé sur votre machine locale 
    même quand l'application fonctionne sur Streamlit Cloud.
    """)
    
    job_manager = st.session_state.job_manager
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Créer un job de traitement", type="primary"):
            job_id = job_manager.create_job(questionnaires_data, template_content, template_filename)
            st.session_state['current_job_id'] = job_id
            st.success(f"Job créé ! ID: `{job_id}`")
    
    with col2:
        if st.button("🔄 Vérifier le statut"):
            if 'current_job_id' in st.session_state:
                job = job_manager.get_job(st.session_state['current_job_id'])
                if job:
                    st.info(f"Statut: **{job['status']}**")
                else:
                    st.error("Job introuvable")
    
    # Afficher les instructions si un job est créé
    if 'current_job_id' in st.session_state:
        job_id = st.session_state['current_job_id']
        job = job_manager.get_job(job_id)
        
        if job and job['status'] in ['pending', 'processing']:
            st.markdown("### 📋 Instructions pour le client local")
            
            # Générer le script de téléchargement
            client_script = generate_client_download_script()
            
            st.markdown("**1. Téléchargez le client xlwings :**")
            st.download_button(
                label="📥 Télécharger xlwings_remote_client.py",
                data=client_script,
                file_name="xlwings_remote_client.py",
                mime="text/python"
            )
            
            st.markdown("**2. Installez les dépendances (si nécessaire) :**")
            st.code("pip install xlwings pandas openpyxl requests")
            
            st.markdown("**3. Exécutez le client sur votre machine :**")
            app_url = get_streamlit_app_url()
            command = f'python xlwings_remote_client.py --url "{app_url}" --job-id "{job_id}"'
            st.code(command)
            
            st.markdown("**4. Attendez la fin du traitement et rafraîchissez cette page**")
            
            # Bouton de rafraîchissement automatique
            if st.button("🔄 Actualiser le statut"):
                st.rerun()
        
        elif job and job['status'] == 'completed':
            st.success("✅ Traitement terminé avec succès !")
            
            # Afficher les résultats
            if job['results']:
                success_count = len([r for r in job['results'] if r['status'] == 'success'])
                error_count = len([r for r in job['results'] if r['status'] == 'error'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Questionnaires générés", success_count)
                with col2:
                    st.metric("Erreurs", error_count)
                
                # Télécharger le résultat
                if job['result_file'] and os.path.exists(job['result_file']):
                    with open(job['result_file'], 'rb') as f:
                        st.download_button(
                            label="📥 Télécharger les questionnaires",
                            data=f.read(),
                            file_name="questionnaires_xlwings.zip",
                            mime="application/zip"
                        )
        
        elif job and job['status'] == 'failed':
            st.error(f"❌ Erreur lors du traitement: {job.get('error_message', 'Erreur inconnue')}")
        
        elif job and job['status'] == 'expired':
            st.warning("⏰ Job expiré. Veuillez créer un nouveau job.")


def generate_client_download_script():
    """Génère le script client à télécharger."""
    # Lire le contenu du fichier xlwings_remote_client.py
    script_path = os.path.join(os.path.dirname(__file__), "xlwings_remote_client.py")
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Script de fallback simplifié
        return '''#!/usr/bin/env python3
"""
Client xlwings distant - Version simplifiée
Pour télécharger la version complète, utilisez l'interface web.
"""
import requests
import json
import sys

def main():
    print("Client xlwings distant - Version simplifiée")
    print("Veuillez télécharger la version complète depuis l'interface web.")
    print("Dépendances requises: pip install xlwings pandas openpyxl requests")

if __name__ == "__main__":
    main()
'''


def get_streamlit_app_url():
    """Obtient l'URL de l'application Streamlit."""
    # En production, récupérer l'URL réelle
    # Pour le développement local
    return "http://localhost:8501"


# Fonctions API pour les endpoints
def api_get_job(job_id: str):
    """Endpoint API pour récupérer un job."""
    job_manager = st.session_state.job_manager
    return job_manager.get_job_for_client(job_id)


def api_download_template(job_id: str):
    """Endpoint API pour télécharger le template."""
    job_manager = st.session_state.job_manager
    job = job_manager.get_job(job_id)
    
    if not job or not job.get('template_path'):
        return None
    
    try:
        with open(job['template_path'], 'rb') as f:
            return f.read()
    except:
        return None


def api_upload_results(job_id: str, results: List[Dict], file_content: bytes):
    """Endpoint API pour uploader les résultats."""
    job_manager = st.session_state.job_manager
    return job_manager.complete_job(job_id, results, file_content)