#!/usr/bin/env python3
"""
Launcher simplifié - sans threading pour éviter les problèmes macOS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import socket
import webbrowser
from pathlib import Path

class SimpleLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Générateur ESG - Launcher Simple")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Variables
        self.process = None
        self.port = 8501
        self.url = f"http://localhost:{self.port}"
        
        # Détecter Python
        self.python_executable = self.detect_python_executable()
        
        self.setup_ui()
        
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
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Big.TButton", font=("Helvetica", 12))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Titre
        ttk.Label(main_frame, text="🏢 Générateur ESG", style="Title.TLabel").pack(pady=(0, 20))
        
        # Info Python
        python_info = f"Python: {self.python_executable}"
        if "venv" in self.python_executable:
            python_info += " (Environnement virtuel ✅)"
        else:
            python_info += " (Système)"
            
        ttk.Label(main_frame, text=python_info, wraplength=450).pack(pady=(0, 20))
        
        # Statut
        self.status_label = ttk.Label(main_frame, text="Prêt à démarrer", font=("Helvetica", 10))
        self.status_label.pack(pady=(0, 20))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Démarrer l'application", 
                                     command=self.start_application, style="Big.TButton")
        self.start_button.pack(pady=5, fill='x')
        
        self.browser_button = ttk.Button(button_frame, text="🌐 Ouvrir dans le navigateur", 
                                       command=self.open_browser, state=tk.DISABLED)
        self.browser_button.pack(pady=5, fill='x')
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Arrêter l'application", 
                                    command=self.stop_application, state=tk.DISABLED)
        self.stop_button.pack(pady=5, fill='x')
        
        # URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(pady=20, fill='x')
        
        ttk.Label(url_frame, text="URL de l'application:").pack(anchor='w')
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill='x', pady=5)
        self.url_entry.insert(0, self.url)
        
        # Instructions
        instructions = """
Instructions:
1. Cliquez sur 'Démarrer l'application'
2. Attendez quelques secondes que le serveur démarre
3. L'application s'ouvrira automatiquement dans votre navigateur
4. Utilisez 'Arrêter l'application' quand vous avez terminé
        """
        ttk.Label(main_frame, text=instructions, justify='left', wraplength=450).pack(pady=20)
        
    def start_application(self):
        """Démarrer l'application SANS threading"""
        try:
            self.status_label.config(text="🔄 Vérification des dépendances...")
            self.root.update()
            
            # Vérifier Streamlit
            result = subprocess.run([self.python_executable, "-c", "import streamlit"], 
                                  capture_output=True, timeout=10)
            if result.returncode != 0:
                self.status_label.config(text="📦 Installation de Streamlit...")
                self.root.update()
                subprocess.check_call([self.python_executable, "-m", "pip", "install", "streamlit", "openpyxl", "xlwings", "pandas"])
            
            self.status_label.config(text="🚀 Démarrage de Streamlit...")
            self.root.update()
            
            # Trouver un port libre
            self.find_free_port()
            
            # Vérifier app.py
            if not Path("app.py").exists():
                messagebox.showerror("Erreur", "Fichier app.py introuvable!")
                return
                
            # Lancer Streamlit
            self.process = subprocess.Popen([
                self.python_executable, "-m", "streamlit", "run", "app.py",
                f"--server.port={self.port}",
                "--server.address=localhost",
                "--browser.gatherUsageStats=false",
                "--server.headless=true"
            ])
            
            # Attendre un peu
            import time
            time.sleep(3)
            
            # Vérifier que ça marche
            if self.process.poll() is None:
                self.status_label.config(text=f"✅ Application démarrée sur le port {self.port}")
                self.start_button.config(state=tk.DISABLED)
                self.browser_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                
                # Ouvrir le navigateur
                webbrowser.open(self.url)
            else:
                self.status_label.config(text="❌ Échec du démarrage")
                messagebox.showerror("Erreur", "Impossible de démarrer Streamlit")
                
        except Exception as e:
            self.status_label.config(text=f"❌ Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Erreur lors du démarrage: {str(e)}")
            
    def find_free_port(self):
        """Trouver un port libre"""
        for port in range(8501, 8510):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    self.port = port
                    self.url = f"http://localhost:{port}"
                    self.url_entry.delete(0, tk.END)
                    self.url_entry.insert(0, self.url)
                    return
            except OSError:
                continue
                
    def stop_application(self):
        """Arrêter l'application"""
        if self.process:
            self.process.terminate()
            self.process = None
            
        self.status_label.config(text="⏹️ Application arrêtée")
        self.start_button.config(state=tk.NORMAL)
        self.browser_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        
    def open_browser(self):
        """Ouvrir le navigateur"""
        webbrowser.open(self.url)
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Gestionnaire de fermeture"""
        if self.process:
            self.process.terminate()
        self.root.destroy()

if __name__ == "__main__":
    print("Démarrage du launcher simplifié...")
    launcher = SimpleLauncher()
    launcher.run()