#!/usr/bin/env python3
"""
Launcher automatique simple - Mode console uniquement
Démarre automatiquement l'application sans interface graphique
"""

import subprocess
import sys
import os
import socket
import webbrowser
import time
import signal
from pathlib import Path

class ConsoleAutoLauncher:
    def __init__(self):
        self.process = None
        self.port = 8501
        self.url = f"http://localhost:{self.port}"
        
        # Détecter Python
        self.python_executable = self.detect_python_executable()
        
        # Gérer Ctrl+C proprement
        signal.signal(signal.SIGINT, self.signal_handler)
        
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
        
    def print_banner(self):
        """Afficher la bannière de démarrage"""
        print("="*60)
        print("🚀 GÉNÉRATEUR ESG - STREAMLIT")
        print("🔄 DÉMARRAGE AUTOMATIQUE")
        print("="*60)
        
    def print_status(self, emoji, message):
        """Afficher un message de statut"""
        print(f"{emoji} {message}")
        
    def find_free_port(self):
        """Trouver un port libre"""
        for port in range(8501, 8510):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.port = port
                    self.url = f"http://localhost:{port}"
                    return True
            except OSError:
                continue
        return False
        
    def check_dependencies(self):
        """Vérifier et installer les dépendances"""
        self.print_status("🔍", "Vérification des dépendances...")
        
        result = subprocess.run([self.python_executable, "-c", "import streamlit"], 
                              capture_output=True, timeout=10)
        
        if result.returncode != 0:
            self.print_status("📦", "Installation des dépendances (cela peut prendre quelques secondes)...")
            try:
                subprocess.check_call([
                    self.python_executable, "-m", "pip", "install", 
                    "streamlit", "openpyxl", "xlwings", "pandas", "--quiet"
                ])
                self.print_status("✅", "Dépendances installées avec succès")
            except subprocess.CalledProcessError as e:
                self.print_status("❌", f"Erreur lors de l'installation: {e}")
                return False
        else:
            self.print_status("✅", "Streamlit détecté")
            
        return True
        
    def start_streamlit(self):
        """Démarrer Streamlit"""
        # Vérifier app.py
        if not Path("app.py").exists():
            self.print_status("❌", "Fichier app.py introuvable!")
            return False
            
        # Trouver un port libre
        if not self.find_free_port():
            self.print_status("❌", "Aucun port disponible")
            return False
            
        self.print_status("🔧", f"Préparation du serveur sur le port {self.port}...")
        
        # Changer vers le répertoire du script
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Lancer Streamlit
        self.print_status("🚀", "Démarrage de Streamlit...")
        
        try:
            self.process = subprocess.Popen([
                self.python_executable, "-m", "streamlit", "run", "app.py",
                f"--server.port={self.port}",
                "--server.address=localhost",
                "--browser.gatherUsageStats=false",
                "--server.headless=true",
                "--logger.level=error"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Attendre que le serveur démarre
            self.print_status("⏳", "Démarrage en cours...")
            time.sleep(3)
            
            # Vérifier que le processus fonctionne
            if self.process.poll() is None:
                self.print_status("✅", f"Application démarrée avec succès sur le port {self.port}")
                self.print_status("🌐", "Ouverture du navigateur...")
                
                # Ouvrir le navigateur
                webbrowser.open(self.url)
                
                return True
            else:
                # Récupérer les erreurs
                stdout, stderr = self.process.communicate()
                error_msg = stderr.decode() if stderr else "Erreur inconnue"
                self.print_status("❌", f"Échec du démarrage: {error_msg}")
                return False
                
        except Exception as e:
            self.print_status("❌", f"Erreur: {e}")
            return False
            
    def print_success_info(self):
        """Afficher les informations de succès"""
        print()
        print("="*60)
        print("🎉 APPLICATION DÉMARRÉE AVEC SUCCÈS !")
        print("="*60)
        print(f"📱 URL: {self.url}")
        print("🌐 Le navigateur va s'ouvrir automatiquement")
        print("🔧 Pour arrêter: Appuyez sur Ctrl+C")
        print("="*60)
        print()
        
    def wait_for_exit(self):
        """Attendre que l'utilisateur arrête l'application"""
        try:
            self.print_status("ℹ️", "Application en cours d'exécution... (Ctrl+C pour arrêter)")
            while True:
                if self.process.poll() is not None:
                    self.print_status("⚠️", "Le processus Streamlit s'est arrêté")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            pass
            
    def signal_handler(self, signum, frame):
        """Gestionnaire pour Ctrl+C"""
        print()
        self.print_status("🛑", "Arrêt de l'application...")
        self.cleanup()
        sys.exit(0)
        
    def cleanup(self):
        """Nettoyer les processus"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None
            
    def run(self):
        """Lancer l'application"""
        try:
            self.print_banner()
            
            # Info Python
            python_name = os.path.basename(self.python_executable)
            if "venv" in self.python_executable:
                self.print_status("🐍", f"Python: {python_name} (Environnement virtuel ✅)")
            else:
                self.print_status("🐍", f"Python: {python_name} (Système)")
            
            print()
            self.print_status("⏰", "Démarrage automatique dans 1 seconde...")
            time.sleep(1)
            print()
            
            # Vérifier les dépendances
            if not self.check_dependencies():
                return False
                
            # Démarrer Streamlit
            if self.start_streamlit():
                self.print_success_info()
                self.wait_for_exit()
            else:
                self.print_status("❌", "Impossible de démarrer l'application")
                return False
                
        except Exception as e:
            self.print_status("❌", f"Erreur inattendue: {e}")
            return False
        finally:
            self.cleanup()
            
        return True

if __name__ == "__main__":
    launcher = ConsoleAutoLauncher()
    launcher.run()