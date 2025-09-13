#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GÉNÉRATEUR ESG - LANCEUR AUTOMATIQUE
Application standalone pour lancer Streamlit en local
Double-cliquez sur ce fichier pour démarrer l'application
"""

import os
import sys
import subprocess
import webbrowser
import time
import platform

# Supprimer le warning de dépréciation Tkinter sur macOS
if platform.system() == "Darwin":
    os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
import threading
import socket

class StreamlitLauncher:
    def __init__(self):
        self.process = None
        self.port = 8501
        self.url = f"http://localhost:{self.port}"
        
        # Déterminer l'exécutable Python à utiliser
        self.python_executable = self.find_python_executable()
        
        # Interface graphique
        self.root = tk.Tk()
        self.root.title("Générateur ESG - Streamlit")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Variables
        self.status_var = tk.StringVar(value="Prêt à démarrer")
        self.progress_var = tk.DoubleVar()
        
        self.setup_ui()
    
    def find_python_executable(self):
        """Trouver le bon exécutable Python à utiliser"""
        # D'abord essayer l'environnement virtuel local
        script_dir = Path(__file__).parent
        possible_venvs = [
            script_dir.parent / ".venv" / "bin" / "python",  # Environnement virtuel un niveau au-dessus
            script_dir / ".venv" / "bin" / "python",        # Environnement virtuel local
            script_dir / "venv" / "bin" / "python",         # Autre nom d'environnement virtuel
        ]
        
        for venv_python in possible_venvs:
            if venv_python.exists():
                return str(venv_python)
        
        # Sinon utiliser l'exécutable Python actuel
        return sys.executable
        
    def center_window(self):
        """Centrer la fenêtre sur l'écran"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
        
    def setup_ui(self):
        """Créer l'interface utilisateur"""
        # Titre
        title_frame = tk.Frame(self.root, bg="#2E86AB", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🚀 Générateur ESG",
            font=("Arial", 18, "bold"),
            bg="#2E86AB",
            fg="white"
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Application Streamlit Locale",
            font=("Arial", 10),
            bg="#2E86AB",
            fg="white"
        )
        subtitle_label.pack()
        
        # Corps principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Informations système
        info_frame = tk.LabelFrame(main_frame, text="Informations Système", padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        system_info = f"💻 Système: {platform.system()} {platform.release()}\n"
        system_info += f"🐍 Python: {sys.version.split()[0]}\n"
        system_info += f"📁 Dossier: {Path(__file__).parent.name}\n"
        system_info += f"⚙️ Exécutable: {Path(self.python_executable).name}"
        
        info_label = tk.Label(info_frame, text=system_info, justify=tk.LEFT, font=("Courier", 9))
        info_label.pack(anchor=tk.W)
        
        # Status
        status_frame = tk.LabelFrame(main_frame, text="Status", padx=10, pady=10)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, font=("Arial", 10))
        self.status_label.pack()
        
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Boutons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Démarrer l'Application",
            command=self.start_application,
            bg="#28A745",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.start_button.pack(fill=tk.X, pady=(0, 10))
        
        self.stop_button = tk.Button(
            button_frame,
            text="🛑 Arrêter l'Application",
            command=self.stop_application,
            bg="#DC3545",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(fill=tk.X, pady=(0, 10))
        
        self.browser_button = tk.Button(
            button_frame,
            text="🌐 Ouvrir dans le Navigateur",
            command=self.open_browser,
            bg="#007BFF",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            state=tk.DISABLED
        )
        self.browser_button.pack(fill=tk.X)
        
        # URL
        url_frame = tk.Frame(main_frame)
        url_frame.pack(fill=tk.X)
        
        url_label = tk.Label(url_frame, text="URL de l'application:", font=("Arial", 10, "bold"))
        url_label.pack(anchor=tk.W)
        
        self.url_entry = tk.Entry(url_frame, font=("Courier", 10), state="readonly")
        self.url_entry.pack(fill=tk.X)
        self.url_entry.insert(0, self.url)
        
        # Gestion de la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def check_dependencies(self):
        """Vérifier et installer les dépendances"""
        self.update_status("🔍 Vérification des dépendances...")
        self.update_progress(20)
        
        try:
            # Vérifier Streamlit
            import streamlit
            self.update_status("✅ Streamlit détecté")
        except ImportError:
            self.update_status("📦 Installation de Streamlit...")
            self.install_requirements()
            
        self.update_progress(50)
        
    def install_requirements(self):
        """Installer les dépendances depuis requirements.txt"""
        try:
            requirements_path = Path(__file__).parent / "requirements.txt"
            if requirements_path.exists():
                subprocess.check_call([
                    self.python_executable, "-m", "pip", "install", "-r", str(requirements_path), "--quiet"
                ])
                self.update_status("✅ Dépendances installées")
            else:
                # Installation manuelle des packages essentiels
                packages = ["streamlit", "openpyxl", "xlwings", "pandas"]
                for package in packages:
                    subprocess.check_call([
                        self.python_executable, "-m", "pip", "install", package, "--quiet"
                    ])
                self.update_status("✅ Packages essentiels installés")
        except Exception as e:
            self.update_status(f"❌ Erreur installation: {e}")
            return False
        return True
        
    def find_free_port(self):
        """Trouver un port libre pour Streamlit"""
        for port in range(8501, 8510):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.port = port
                    self.url = f"http://localhost:{port}"
                    self.url_entry.delete(0, tk.END)
                    self.url_entry.insert(0, self.url)
                    return True
            except OSError:
                continue
        return False
        
    def start_streamlit(self):
        """Démarrer le serveur Streamlit"""
        self.update_status("🚀 Démarrage de Streamlit...")
        self.update_progress(70)
        
        # Changer vers le répertoire du script
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Trouver un port libre
        if not self.find_free_port():
            self.update_status("❌ Aucun port disponible")
            return False
            
        try:
            # Lancer Streamlit
            self.process = subprocess.Popen([
                self.python_executable, "-m", "streamlit", "run", "app.py",
                f"--server.port={self.port}",
                "--server.address=localhost",
                "--browser.gatherUsageStats=false",
                "--server.headless=true",
                "--logger.level=error"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Attendre que le serveur démarre
            self.update_progress(90)
            time.sleep(3)
            
            # Vérifier que le processus fonctionne
            if self.process.poll() is None:
                self.update_status(f"✅ Application démarrée sur le port {self.port}")
                self.update_progress(100)
                return True
            else:
                # Récupérer les erreurs
                stdout, stderr = self.process.communicate()
                error_msg = stderr.strip() if stderr else "Erreur inconnue"
                self.update_status(f"❌ Échec du démarrage: {error_msg}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Erreur: {e}")
            return False
            
    def start_application(self):
        """Démarrer l'application (thread séparé)"""
        self.start_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self._start_application_thread)
        thread.daemon = True
        thread.start()
        
    def _start_application_thread(self):
        """Thread de démarrage de l'application"""
        self.update_progress(0)
        
        # Vérifier les dépendances
        if not self.check_dependencies():
            self.start_button.config(state=tk.NORMAL)
            return
            
        # Démarrer Streamlit
        if self.start_streamlit():
            # Activer les boutons
            self.root.after(0, lambda: self.stop_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.browser_button.config(state=tk.NORMAL))
            
            # Ouvrir automatiquement le navigateur
            time.sleep(1)
            self.open_browser()
        else:
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            
    def stop_application(self):
        """Arrêter l'application Streamlit"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None
            
        self.update_status("⏹️ Application arrêtée")
        self.update_progress(0)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.browser_button.config(state=tk.DISABLED)
        
    def open_browser(self):
        """Ouvrir l'application dans le navigateur"""
        try:
            webbrowser.open(self.url)
            self.update_status(f"🌐 Navigateur ouvert sur {self.url}")
        except Exception as e:
            self.update_status(f"❌ Erreur ouverture navigateur: {e}")
            
    def update_status(self, message):
        """Mettre à jour le status"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def update_progress(self, value):
        """Mettre à jour la barre de progression"""
        self.progress_var.set(value)
        self.root.update_idletasks()
        
    def on_closing(self):
        """Gestion de la fermeture de l'application"""
        if self.process:
            result = messagebox.askyesno(
                "Fermeture",
                "L'application Streamlit est en cours d'exécution.\nVoulez-vous vraiment quitter ?"
            )
            if result:
                self.stop_application()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Lancer l'interface graphique"""
        self.root.mainloop()

def main():
    """Fonction principale"""
    try:
        # Créer et lancer l'application
        launcher = StreamlitLauncher()
        launcher.run()
    except Exception as e:
        # Fallback en mode console si l'interface graphique échoue
        print("="*50)
        print("🚀 GÉNÉRATEUR ESG - STREAMLIT")
        print("="*50)
        print(f"❌ Erreur interface graphique: {e}")
        print("🔄 Lancement en mode console...")
        launch_console_mode()

def launch_console_mode():
    """Mode console de fallback"""
    import os
    import sys
    import subprocess
    import webbrowser
    import time
    from pathlib import Path
    
    print(f"💻 Système: {platform.system()}")
    print(f"🐍 Python: {sys.version}")
    
    # Changer vers le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🔧 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        print("✅ Dépendances installées")
    except:
        print("⚠️ Erreur installation, tentative de démarrage...")
    
    print("🚀 Lancement de Streamlit...")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
        
        print("⏳ Démarrage en cours...")
        time.sleep(3)
        
        print("🌐 Ouverture du navigateur...")
        webbrowser.open("http://localhost:8501")
        
        print("\n" + "="*50)
        print("🎉 APPLICATION DÉMARRÉE AVEC SUCCÈS !")
        print("="*50)
        print("📱 URL: http://localhost:8501")
        print("🔧 Pour arrêter: Ctrl+C dans cette fenêtre")
        print("="*50)
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt de l'application...")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        input("Appuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()