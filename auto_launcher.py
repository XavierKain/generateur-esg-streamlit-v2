#!/usr/bin/env python3
"""
Launcher automatique - Démarre l'application automatiquement après 1 seconde
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import socket
import webbrowser
import time
from pathlib import Path

class AutoLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Générateur ESG - Démarrage automatique")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Variables
        self.process = None
        self.port = 8501
        self.url = f"http://localhost:{self.port}"
        self.startup_timer = None
        
        # Détecter Python
        self.python_executable = self.detect_python_executable()
        
        self.setup_ui()
        
        # Démarrer automatiquement après 1 seconde
        self.schedule_auto_start()
        
    def detect_python_executable(self):
        """Détecter le bon exécutable Python (venv prioritaire)"""
        venv_paths = [
            "../.venv/bin/python",
            ".venv/bin/python", 
            "venv/bin/python"
        ]
        
        # Tester les environnements virtuels
        for venv_path in venv_paths:
            full_path = Path(venv_path)
            if full_path.exists():
                return str(full_path.absolute())
        
        # Fallback sur le Python système
        return sys.executable
        
    def setup_ui(self):
        # Style
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 18, "bold"))
        style.configure("Status.TLabel", font=("Helvetica", 12))
        style.configure("Info.TLabel", font=("Helvetica", 10))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Titre avec icône
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(0, 20))
        
        ttk.Label(title_frame, text="🏢 Générateur ESG", style="Title.TLabel").pack()
        ttk.Label(title_frame, text="Démarrage automatique", style="Info.TLabel").pack()
        
        # Info Python
        python_info = f"Python: {os.path.basename(self.python_executable)}"
        if "venv" in self.python_executable:
            python_info += " (Environnement virtuel ✅)"
        else:
            python_info += " (Système)"
            
        ttk.Label(main_frame, text=python_info, style="Info.TLabel").pack(pady=(0, 15))
        
        # Statut principal
        self.status_label = ttk.Label(main_frame, text="🔄 Démarrage dans 1 seconde...", 
                                     style="Status.TLabel", foreground="blue")
        self.status_label.pack(pady=(0, 20))
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 20))
        
        # Informations détaillées
        self.detail_label = ttk.Label(main_frame, text="Initialisation...", 
                                     style="Info.TLabel", foreground="gray")
        self.detail_label.pack(pady=(0, 15))
        
        # URL de l'application
        url_frame = ttk.LabelFrame(main_frame, text="URL de l'application", padding=10)
        url_frame.pack(fill='x', pady=(0, 15))
        
        self.url_label = ttk.Label(url_frame, text="En attente...", style="Info.TLabel")
        self.url_label.pack()
        
        # Instructions
        instructions_frame = ttk.LabelFrame(main_frame, text="Instructions", padding=10)
        instructions_frame.pack(fill='x')
        
        instructions_text = """• L'application démarre automatiquement
• Le navigateur s'ouvrira dans quelques secondes
• Fermez cette fenêtre pour arrêter l'application"""
        
        ttk.Label(instructions_frame, text=instructions_text, style="Info.TLabel", 
                 justify='left').pack(anchor='w')
        
    def schedule_auto_start(self):
        """Programmer le démarrage automatique"""
        self.startup_timer = self.root.after(1000, self.auto_start_application)
        
    def auto_start_application(self):
        """Démarrer l'application automatiquement"""
        try:
            self.progress.start()
            
            # Étape 1: Vérification des dépendances
            self.update_status("🔍 Vérification des dépendances...", "Vérification de Streamlit...")
            self.root.update()
            
            result = subprocess.run([self.python_executable, "-c", "import streamlit"], 
                                  capture_output=True, timeout=10)
            
            if result.returncode != 0:
                self.update_status("📦 Installation des dépendances...", "Installation de Streamlit et des packages...")
                self.root.update()
                
                subprocess.check_call([
                    self.python_executable, "-m", "pip", "install", 
                    "streamlit", "openpyxl", "xlwings", "pandas", "--quiet"
                ])
            
            # Étape 2: Préparation du serveur
            self.update_status("🔧 Préparation du serveur...", "Recherche d'un port disponible...")
            self.root.update()
            
            self.find_free_port()
            
            # Étape 3: Vérification des fichiers
            self.update_status("📁 Vérification des fichiers...", "Vérification d'app.py...")
            self.root.update()
            
            if not Path("app.py").exists():
                self.update_status("❌ Erreur: Fichier manquant", "app.py introuvable", "red")
                self.progress.stop()
                return
                
            # Étape 4: Démarrage de Streamlit
            self.update_status("🚀 Démarrage de Streamlit...", f"Lancement sur le port {self.port}...")
            self.root.update()
            
            # Changer vers le répertoire du script
            script_dir = Path(__file__).parent
            os.chdir(script_dir)
            
            self.process = subprocess.Popen([
                self.python_executable, "-m", "streamlit", "run", "app.py",
                f"--server.port={self.port}",
                "--server.address=localhost",
                "--browser.gatherUsageStats=false",
                "--server.headless=true",
                "--logger.level=error"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Étape 5: Attente du démarrage
            self.update_status("⏳ Démarrage en cours...", "Attente de la disponibilité du serveur...")
            self.root.update()
            
            time.sleep(3)
            
            # Étape 6: Vérification et ouverture
            if self.process.poll() is None:
                self.progress.stop()
                self.update_status("✅ Application démarrée avec succès!", 
                                 "Ouverture du navigateur...", "green")
                self.url_label.config(text=self.url)
                self.root.update()
                
                # Ouvrir le navigateur
                webbrowser.open(self.url)
                
                # Mise à jour finale
                time.sleep(1)
                self.update_status("🎉 Application prête!", 
                                 "Fermez cette fenêtre pour arrêter l'application", "green")
            else:
                self.progress.stop()
                # Récupérer les erreurs
                stdout, stderr = self.process.communicate()
                error_msg = stderr.strip() if stderr else "Erreur inconnue"
                self.update_status("❌ Échec du démarrage", f"Erreur: {error_msg}", "red")
                
        except Exception as e:
            self.progress.stop()
            self.update_status("❌ Erreur inattendue", f"Erreur: {str(e)}", "red")
            
    def update_status(self, main_text, detail_text, color="blue"):
        """Mettre à jour les textes de statut"""
        self.status_label.config(text=main_text, foreground=color)
        self.detail_label.config(text=detail_text)
        
    def find_free_port(self):
        """Trouver un port libre"""
        for port in range(8501, 8510):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.port = port
                    self.url = f"http://localhost:{port}"
                    return
            except OSError:
                continue
                
    def run(self):
        """Lancer l'interface"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Gestionnaire de fermeture"""
        if self.startup_timer:
            self.root.after_cancel(self.startup_timer)
            
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except:
                self.process.kill()
                
        self.root.destroy()

if __name__ == "__main__":
    print("Démarrage du launcher automatique...")
    launcher = AutoLauncher()
    launcher.run()