#!/usr/bin/env python3
"""
Test simple du launcher - Version de débogage
"""

import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import time
import sys
import os
from pathlib import Path

class SimpleLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test Launcher - Debug")
        self.root.geometry("400x200")
        
        # Trouver le bon Python
        venv_paths = [
            "../.venv/bin/python",
            ".venv/bin/python", 
            "venv/bin/python"
        ]
        
        self.python_executable = sys.executable  # fallback
        
        for venv_path in venv_paths:
            full_path = Path(venv_path)
            print(f"Test du chemin: {full_path} (existe: {full_path.exists()})")
            if full_path.exists():
                # Ne pas utiliser resolve() car ça suit les liens symboliques
                self.python_executable = str(full_path.absolute())
                print(f"✅ Venv trouvé: {self.python_executable}")
                break
        else:
            print(f"⚠️ Pas de venv trouvé, utilisation du système: {self.python_executable}")
            
        print(f"Python final utilisé: {self.python_executable}")
        
        self.setup_ui()
        
    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Test simple du launcher").grid(row=0, column=0, pady=10)
        
        self.status_label = ttk.Label(frame, text="Prêt")
        self.status_label.grid(row=1, column=0, pady=10)
        
        self.start_button = ttk.Button(frame, text="Test Démarrage", command=self.test_start)
        self.start_button.grid(row=2, column=0, pady=10)
        
    def test_start(self):
        print("DEBUT: test_start appelée")
        self.status_label.config(text="Test en cours...")
        self.start_button.config(state=tk.DISABLED)
        
        # Lancer dans un thread
        thread = threading.Thread(target=self.test_thread)
        thread.daemon = True
        thread.start()
        print("FIN: test_start - thread lancé")
        
    def test_thread(self):
        print("DEBUT: test_thread")
        try:
            # Test simple
            result = subprocess.run([self.python_executable, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            print(f"Python version: {result.stdout.strip()}")
            
            # Test import streamlit
            result = subprocess.run([self.python_executable, "-c", "import streamlit; print('OK')"], 
                                  capture_output=True, text=True, timeout=10)
            print(f"Streamlit test: {result.stdout.strip()}")
            
            # Mettre à jour l'interface depuis le thread principal
            self.root.after(0, lambda: self.status_label.config(text="✅ Test réussi"))
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            
        except Exception as e:
            print(f"ERREUR dans test_thread: {e}")
            self.root.after(0, lambda: self.status_label.config(text=f"❌ Erreur: {e}"))
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        
        print("FIN: test_thread")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Démarrage du test launcher...")
    launcher = SimpleLauncher()
    launcher.run()